function toggleInbox() {
    const rightBox = document.getElementById("rightBox");
    const inboxButton = document.getElementById("inboxButton");
    
    if (!rightBox.style.display) {
        rightBox.style.display = "flex";
    }
    
    if (rightBox.style.display === "flex") {
        rightBox.style.display = "none";
        inboxButton.style.fill = "#555555";
    } else {
        rightBox.style.display = "flex";
        inboxButton.style.fill = "#000000";
    }
}

/********************
    Settings toggle  
*********************/

const settingsButton = document.getElementById("settingsButton");
const container = document.getElementById("container");
const settingContainer = document.getElementById("settingContainer");
const closeSettingsButton = document.getElementById("closeSettingsButton");

settingsButton.addEventListener("click", () => {
    container.style.display = "none";
    settingContainer.style.display = "flex";
    updateCharCount();
});

closeSettingsButton.addEventListener("click", () => {
    settingContainer.style.display = "none";
    container.style.display = "flex";
});

document.addEventListener("keydown", event => {
    if (event.key === "Escape" && settingContainer.style.display !== "none" && container.style.display == "none") {
      settingContainer.style.display = "none";
      container.style.display = "flex";
    }
});

/*************** 
  Settings Tabs
 ***************/

function showTab(event, tabID) {
    const tabContent = document.querySelectorAll(".tab-content");

    tabContent.forEach((tab) => {
        tab.classList.remove("active");
    });

    const tabLinks = document.querySelectorAll(".list-button");

    tabLinks.forEach((link) => {
        link.classList.remove("selected");
    });

    document.getElementById(tabID).classList.add("active");
    event.currentTarget.classList.add("selected");
}

/* Edit Profile */

function updateCharCount() {
    const textarea = document.getElementById("editedBio");
    const charCounter = document.getElementById("charCounter");
    
    const maxLength = 150;
    const currentLength = textarea.value.length;
    const remainingChars = maxLength - currentLength;
    
    charCounter.textContent = remainingChars;
    
    if (remainingChars < 0) {
        charCounter.style.color = "red"; 
    } else {
        charCounter.style.color = "var(--light-text-hover)";
    }
}

const submitProfileButton = document.getElementById("submitProfileButton");
const updateProfileForm = document.getElementById("updateProfileForm");

submitProfileButton.addEventListener("click", async () => {

    const formData = new FormData();
    formData.append("username", document.getElementById("editedUsername").value);
    formData.append("name", document.getElementById("editedDisplayName").value);
    formData.append("bio", document.getElementById("editedBio").value);

    const response = await fetch("/edit-profile/", {
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    });

    if (response.ok) {
        console.log("Edited profile");
    } else {
        console.error("[ERROR] Request failed.");
    }
}); 

/* Change password modal */
const openPasswordModalButton = document.getElementById("changePasswordButton");
const closePasswordModalButton = document.getElementById("closePasswordModalButton");
const passwordModal = document.getElementById("passwordModal");

openPasswordModalButton.addEventListener("click", () => {
    passwordModal.showModal();
});

closePasswordModalButton.addEventListener("click", () => {
    passwordModal.close();
});

/* Change email modal */
const openEmailModalButton = document.getElementById("openEmailModalButton");
const closeEmailModalButton = document.getElementById("closeEmailModalButton");
const emailModal = document.getElementById("emailModal");

openEmailModalButton.addEventListener("click", () => {
    emailModal.showModal();
});

closeEmailModalButton.addEventListener("click", () => {
    emailModal.close();
});

/* Logout */
document.addEventListener('htmx:afterRequest', function (event) {
    if (event.detail.elt.matches('.list-button[hx-post="/logout/"]')) {
        window.location.href = "/login"; 
    }
});





