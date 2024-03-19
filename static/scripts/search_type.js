$(document).ready(function () {
	$('.for_recipe').click(function () {
		$('#searchInput').attr('placeholder', 'Search for recipes...');
		$('.search_type').hide();
			$("#searchBtn").click(function() {
			    var searchQuery = $("#searchInput").val();
			    window.location.href = `/search?query=${encodeURIComponent(searchQuery) + '+recipe'}`;

			});
		
	    });

	$('.by_ingredient').click(function () {
            $('#searchInput').attr('placeholder', 'Search by ingredients... (ex: Tomato Onion Garlic)');
            $('.search_type').hide();
	    $("#searchBtn").click(function() {
		var searchQuery = $("#searchInput").val();
		console.log("User searched for:", searchQuery);
		window.location.href = `/search?query=${encodeURIComponent(searchQuery)+'+ingredient'}`;

	    });
        });
    });



