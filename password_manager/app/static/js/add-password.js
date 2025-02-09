async function generatePassword(length) {
    const response = await fetch(`/generate-password?length=${length}`);
    const data = await response.json();
    document.getElementById('password').value = data.password;
}

async function confirmPassword() {
    const website = document.getElementById('website').value;
    const password = document.getElementById('password').value;
    const masterPassword = document.getElementById('master_password').value;

    if (website && password && masterPassword) {
        const response = await fetch('/add-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ website: website, password: password, master_password: masterPassword })
        });
        const data = await response.json();
        if (data.status === 'success') {
            document.getElementById('message').innerText = 'Adding successful!';
            document.getElementById('message').style.color = 'green';
        } else {
            document.getElementById('message').innerText = 'A problem has been encountered';
            document.getElementById('message').style.color = 'red';
        }
    } else {
        document.getElementById('message').innerText = 'Please fill in all fields';
        document.getElementById('message').style.color = 'red';
    }
}

// Toggle password visibility 
const togglePassword = document.querySelector('#togglePassword'); 
const password = document.querySelector('#password'); 

togglePassword.addEventListener('click', function (e) { 
    // Toggle the type attribute 
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password'; 
    password.setAttribute('type', type); 
    // Toggle the eye icon 
    this.classList.toggle('fa-eye-slash');
});