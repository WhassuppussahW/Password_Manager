async function fetchWebsites() {
    const response = await fetch('/get-websites');
    const data = await response.json();
    const websiteSelect = document.getElementById('website');
    data.websites.forEach(website => {
        let option = document.createElement('option');
        option.value = website;
        option.text = website;
        websiteSelect.add(option);
    });
}

async function retrievePassword() {
    const website = document.getElementById('website').value;
    const masterPassword = document.getElementById('master_password').value;

    console.log('Website:', website);
    console.log('Master Password:', masterPassword);

    if (website && masterPassword) {
        const response = await fetch('/retrieve-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ website: website, master_password: masterPassword })
        });
        console.log('Request sent: POST /retrieve-password');

        const data = await response.json();
        console.log('Response:', data);

        if (response.ok) {
            document.getElementById('password').innerText = data.password;
        } else {
            document.getElementById('password').innerText = 'Error retrieving password';
        }
    } else {
        document.getElementById('password').innerText = 'Please fill in all fields';
    }
}

window.onload = fetchWebsites;
