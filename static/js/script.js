document.addEventListener('DOMContentLoaded', function() {
    let input = document.querySelector('#movie');
    let results = document.querySelector('#results');

    input.addEventListener('keyup', function() {
        clearSuggestions();
        let suggestions = []

        if (input.value.length) {
            suggestions = movies.filter(movie => movie.toLowerCase().includes(input.value.toLowerCase()))
        }

        for (let i = 0; i < suggestions.length; i++) {
            let listItem = document.createElement("li");
            listItem.classList.add("list-items");
            listItem.innerHTML = suggestions[i];
            listItem.onclick = function() {
                input.value = listItem.innerHTML;
                clearSuggestions();
            };
            results.appendChild(listItem);
        }
    });

    function clearSuggestions() {
        let suggestions = document.querySelectorAll(".list-items");

        suggestions.forEach((item) => {
            item.remove();
        });
    };
});