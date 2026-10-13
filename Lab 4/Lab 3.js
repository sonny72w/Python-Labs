document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            if (name === "" || email === "") {
                alert("Access Denied: Please fill in all required security fields.");
                event.preventDefault(); 
            } else {
                alert("Success: Secure connection established. Message sent!");
            }
        });
    }
});