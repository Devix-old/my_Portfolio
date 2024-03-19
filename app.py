#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from random_recipes import randomrecipes
from get_recipe import search_recipe, get_recipe_by_id, recipe_info, search_by_ingredients

recipes = ""

app = Flask(__name__)

app.secret_key = 'secret_key1995'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'recipes_db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/recipes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


mysql = MySQL(app)
login_manage = LoginManager()
login_manage.init_app(app)
bcrypt = Bcrypt(app)


@login_manage.user_loader
def load_user(user_email):
    return User.query.filter_by(email=user_email).first()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    saved_recipes = db.Column(db.String(255))

    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.saved_recipes = ""
        self.searched_recipes = ""
    def save_recipe(self, recipe_id):
        if self.saved_recipes:
            self.saved_recipes += f',{recipe_id}'
        else:
            self.saved_recipes = str(recipe_id)
        db.session.commit()

    def get_saved_recipes(self):
        if self.saved_recipes:
            return list(map(int, self.saved_recipes.split(',')))
        else:
            return []
    
    def delete_recipe(self, recipe_id):
        if str(recipe_id) in self.saved_recipes:
            s = self.saved_recipes.split(',')
            s.remove(str(recipe_id))
            self.saved_recipes = ','.join(s)
            db.session.commit()
    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username, email from users where id = %s', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            User(user_id, result[0], result[1])
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False



@app.route('/', strict_slashes=False)
def home_page():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None
    recipes = randomrecipes
    return render_template('index.html', username=username, recipes=recipes)


@app.route('/home', strict_slashes=False)
def home():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None

    recipes = randomrecipes
    return render_template('index.html', username=username, recipes=recipes)


@app.route('/dashboard', strict_slashes=False)
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
         
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, username, email, password from users where email = %s', (email,))
        user_data = cursor.fetchone()
        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])
            login_user(user)
            username = user.username
            cursor.close()
            return redirect(url_for('home'))
  
        
    return render_template('login.html')

from flask import request, jsonify

@app.route('/search', methods=['POST', 'GET'])	
def search():
    query = ""
    data = request.args.get('query', '').split(" ")
    for i in range(len(data) - 1):
        query += data[i]
        if i != len(data) - 2:
            query += " "

    search_type = data[len(data) - 1]

    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None
    if search_type == 'recipe':
        recipes = search_recipe(query)
    elif search_type == 'ingredient':
        recipes = search_by_ingredients(query)
    else:
        recipes = None

    return render_template('index.html', recipes=recipes, username=username)


@app.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users(username, email, password) values(%s,%s,%s)',(
            username, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/recipe/<int:recipe_id>', strict_slashes=False, methods=['GET', 'POST'])
def recipe(recipe_id):
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None
    recipe = get_recipe_by_id(recipe_id)
    return render_template('recipe.html', recipe=recipe, username=username)


@app.route('/save_recipe/<int:recipe_id>', strict_slashes=False, methods=['POST'])
@login_required
def save_recipe(recipe_id):
    """Save or delete recipe based on user's action."""
    user = current_user
    saved = False
    if user.saved_recipes:
        if str(recipe_id) not in user.saved_recipes:
            user.save_recipe(recipe_id)
            saved = True
        else:
            user.delete_recipe(recipe_id)
    else:
        user.save_recipe(recipe_id)
        saved=True
    return jsonify({"saved":saved})


@app.route('/profile', strict_slashes=False)
@login_required
def profile():
    username = current_user.username
    return render_template('profile.html', username = username)

@app.route('/myrecipes', strict_slashes=False)
@login_required
def myrecipes():
    myrecipes = [""]
    username = current_user.username
    if current_user.saved_recipes:
        myrecipes = current_user.saved_recipes.split(',')

    saved_recipes = []
    if myrecipes[0]!= '':
        for id in myrecipes:
            saved_recipes.append(get_recipe_by_id(id))
    
    
    return render_template('myrecipes.html', recipes=saved_recipes, username=username)


@app.route('/remove_recipe/<recipe_id>', methods=['POST'])
@login_required
def remove_recipe(recipe_id):
    user = current_user

    try:

        user.delete_recipe(recipe_id)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'success': False}), 500


@app.route('/about')
def about():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None
    return render_template('about.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()
