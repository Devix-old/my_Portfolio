#!/usr/bin/python3
import cmd
from app import search_recipe
from classes.db_storage import storage
from time import sleep

class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        print('Shutting down...')
        for _ in range(10):
            sleep(0.2)
            print('.', end='', flush=True)
        print(' Good bye!')
        sleep(0.5)
        return True
    

    def do_search(self, arg):
        recipes = search_recipe(arg)

    def do_all(self, arg):
        print(storage().all_recipes())
    
    def do_show_users(self, arg):
        print(storage().all_users())

    def do_saved_recipes(self, arg):
        print(storage().all_saved_recipes())
        

if __name__ == '__main__':
    HBNBCommand().cmdloop()
