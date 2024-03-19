document.addEventListener('DOMContentLoaded', (event) => {

    
	const saveIcons = document.querySelectorAll('.save_icon');
	saveIcons.forEach(icon => {
	    icon.addEventListener('click', function(event) {
		// Send recipe ID to Flask route to save the recipe
		const recipeId = icon.getAttribute('data-recipe-id');
		saveRecipe(recipeId);
		event.preventDefault();
		document.querySelector('.pop-up').style.display = 'flex';
	    });
	});
    
	document.getElementById('closePopUp').addEventListener('click', function() {
	    document.querySelector('.pop-up').style.display = 'none';
	});
    
	window.addEventListener('click', function(event) {
	    const popUp = document.querySelector('.pop-up');
	    if (event.target === popUp) {
		popUp.style.display = 'none';
	    }
	});
    });
    
    // Function to send recipe ID to Flask route to save the recipe
    function saveRecipe(recipeId) {
	fetch(`/save_recipe/${recipeId}` ,{ //
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify({id: recipeId}) //
	    })
	    .then (response => response.json())
	    .then (data => {
		const popUp = document.querySelector('.pop-up');
        	const popUpContent = popUp.querySelector('h1');
		const popUpicon = popUp.querySelector('img');
		const saveIcon = document.querySelector(`.save_icon[data-recipe-id="${recipeId}"]`); //
		
		if (data.saved) //
		{
			saveIcon.style.backgroundColor = "green";
			popUpContent.textContent = "recipe saved!";
			popUpicon.src = "https://icon-library.com/images/validity-icon/validity-icon-27.jpg"
		}
		else { //

			saveIcon.style.backgroundColor = "#d80b0b";
			popUpicon.src = "https://cdn2.iconfinder.com/data/icons/ui-elements-bright-fill/60/049_-_Remove-512.png"
			popUpContent.textContent = "Recipe unsaved!";
		}

	     })
	     
		
    }
    
// Function to send recipe ID to Flask route to remove the recipe
function removeRecipe(recipeId) {
	fetch(`/remove_recipe/${recipeId}`, {
	    method: 'POST',
	    headers: {'Content-Type': 'application/json'},
	    body: JSON.stringify({id: recipeId})
	})
	.then(response => {
	    if(response.ok) {
		// Remove the card from the DOM
		document.querySelector(`.recipe-card[data-recipe-id="${recipeId}"]`).remove();
	    }
	})
	.catch(error => console.error('Error:', error));
    }
    
    document.addEventListener('DOMContentLoaded', () => {
	const removeIcons = document.querySelectorAll('.remove_icon'); // Ensure your class matches this
	removeIcons.forEach(icon => {
	    icon.addEventListener('click', function(event) {
		event.preventDefault(); // Prevent the link action
		const recipeId = this.getAttribute('data-recipe-id');
		removeRecipe(recipeId);
	    });
	});
    });
