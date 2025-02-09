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

async function deletePassword() {
    const website = document.getElementById('website').value;
    if (confirm(`Are you sure you want to delete the password for ${website}?`)) {
        const response = await fetch('/delete-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ website: website })
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById('message').innerText = 'Deletion successful!';
            document.getElementById('message').style.color = 'green';
        } else {
            document.getElementById('message').innerText = 'Error deleting password';
            document.getElementById('message').style.color = 'red';
        }
    }
}

window.onload = fetchWebsites;
