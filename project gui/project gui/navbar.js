// navbar.js
// navbar.js
fetch('../navbar.html')
    .then(response => response.text())
    .then(html => {
        document.getElementById('navbar-placeholder').innerHTML = html;
    })
    .catch(error => {
        console.error('Error fetching navbar:', error);
    });

    document.addEventListener("DOMContentLoaded", function() {
        console.log("Script loaded successfully!");
        // Select the dropdown trigger element
        var dropdownTrigger = document.querySelector(".dropdown-trigger");
        var dropdownMenu = document.querySelector(".dropdown-menu");

        // Function to handle item selection and menu removal
        function selectItem(item) {
            alert("Selected: " + item);
            dropdownMenu.classList.remove("show"); // Hide the menu
        }

        // Function to toggle dropdown visibility
        function toggleDropdown() {
            dropdownMenu.classList.toggle("show"); // Toggle "show" class for visibility
        }

        // Attach click event to the trigger element
        dropdownTrigger.addEventListener("click", toggleDropdown);
    });