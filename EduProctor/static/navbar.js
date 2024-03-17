// navbar.js
// navbar.js
fetch('../static/navbar.html')
    .then(response => response.text())
    .then(html => {
        document.getElementById('navbar-placeholder').innerHTML = html;
    })
    .catch(error => {
        console.error('Error fetching navbar:', error);
    });
