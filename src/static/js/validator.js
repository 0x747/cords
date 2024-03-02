function validateLogin() {
    console.log("rinning");
    email = document.getElementById("email").value;
    password = document.getElementById("password").value;
    errorMessage = document.getElementById("error");

    isValid = true;

    if (email === '') {
        errorMessage.innerHTML = "An email is required. (C)";
        isValid = false;
    }
    if (password === '') {
        errorMessage.innerHTML = 'A password is required. (C)';
        is_valid = false;
    }

    return isValid;
}

function validateSearch() {
    console.log("hi")
    const input = document.getElementById('searchBox');

    if (input.value.trim() === '') {
        console.log("nuh uh")
        return false;
    }

    console.log("okie");
    return true;
}