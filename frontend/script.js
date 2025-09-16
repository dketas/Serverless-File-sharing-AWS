const apiBaseUrl = 'https://tvpxpxx011pd4.execute-aip.eeee-eest-17.amaz000000onaws.com/Severless_File_Sharing_System'; // Update with your API Gateway URL

// Configure Cognito User Pool
const poolData = {
    UserPoolId: 'eu-west-1_ruh2fQmWE', // Your User Pool ID
    ClientId: '7tj09inpo7pu2fn2tkgs4ko2t2', // Your App Client ID
};
const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

// Check if user is authenticated on page load
window.onload = function () {
    checkAuthentication();
};

// Check if the user is authenticated
function checkAuthentication() {
    const cognitoUser = userPool.getCurrentUser();
    if (cognitoUser) {
        cognitoUser.getSession((err, session) => {
            if (err || !session.isValid()) {
                showLoginForm();
            } else {
                showFileOperations();
            }
        });
    } else {
        showLoginForm();
    }
}

// Show login form
function showLoginForm() {
    document.getElementById('loginSection').style.display = 'block';
    document.getElementById('fileActionsSection').style.display = 'none';
}

// Show file-sharing operations
function showFileOperations() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('fileActionsSection').style.display = 'block';
    listFiles(); // Populate the file list
}

// Login user
function loginUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const authDetails = new AmazonCognitoIdentity.AuthenticationDetails({
        Username: username,
        Password: password,
    });

    const userData = {
        Username: username,
        Pool: userPool,
    };

    const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    cognitoUser.authenticateUser(authDetails, {
        onSuccess: function (result) {
            console.log('Login successful!');
            showFileOperations();
        },
        onFailure: function (err) {
            alert('Login failed: ' + err.message);
        },
    });
}

// Logout user
function logoutUser() {
    const cognitoUser = userPool.getCurrentUser();
    if (cognitoUser) {
        cognitoUser.signOut();
        showLoginForm();
    }
}

// Upload File
function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please choose a file to upload.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch(`${apiBaseUrl}/upload`, {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            alert('File uploaded successfully!');
            listFiles(); // Refresh file list
        })
        .catch(error => {
            alert('Error uploading file: ' + error);
        });
}

// List Files
function listFiles() {
    fetch(`${apiBaseUrl}/list`)
        .then(response => response.json())
        .then(data => {
            const fileList = document.getElementById('fileList');
            const fileSelect = document.getElementById('fileSelect');
            const deleteSelect = document.getElementById('deleteSelect');

            fileList.innerHTML = '';
            fileSelect.innerHTML = '';
            deleteSelect.innerHTML = '';

            data.files.forEach(file => {
                const listItem = document.createElement('li');
                listItem.textContent = file.name;
                fileList.appendChild(listItem);

                const option1 = document.createElement('option');
                option1.value = file.name;
                option1.textContent = file.name;
                fileSelect.appendChild(option1);

                const option2 = document.createElement('option');
                option2.value = file.name;
                option2.textContent = file.name;
                deleteSelect.appendChild(option2);
            });
        })
        .catch(error => {
            alert('Error fetching file list: ' + error);
        });
}

// Download File
function downloadFile() {
    const fileSelect = document.getElementById('fileSelect');
    const fileName = fileSelect.value;

    if (!fileName) {
        alert('Please select a file to download.');
        return;
    }

    fetch(`${apiBaseUrl}/download?fileName=${encodeURIComponent(fileName)}`)
        .then(response => response.blob())
        .then(blob => {
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = fileName;
            link.click();
        })
        .catch(error => {
            alert('Error downloading file: ' + error);
        });
}

// Delete File
function deleteFile() {
    const deleteSelect = document.getElementById('deleteSelect');
    const fileName = deleteSelect.value;

    if (!fileName) {
        alert('Please select a file to delete.');
        return;
    }

    fetch(`${apiBaseUrl}/delete?fileName=${encodeURIComponent(fileName)}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            alert('File deleted successfully!');
            listFiles(); // Refresh file list
        })
        .catch(error => {
            alert('Error deleting file: ' + error);
        });
}

