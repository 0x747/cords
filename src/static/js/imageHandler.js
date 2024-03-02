import "./croppie.js"

/*************************************/
/***** UPDATING AVATAR ***************/
/*************************************/

const changePfpButton = document.getElementById("changePfpButton");
const closePfpModalButton = document.getElementById("closePfpModalButton");
const pfpModal = document.getElementById("pfpModal");
const pfpFilePicker = document.getElementById("pfpFilePicker");
const submitPfpButton = document.getElementById("submitPfpButton");
const pfpForm = document.getElementById("pfpForm");
const pfpDiv = document.getElementById("pfp");

let cropPreview = document.getElementById("imagePreview");
let imageURL;
let cropper;

changePfpButton.addEventListener("click", () => {
    
    pfpFilePicker.click() ;

    pfpFilePicker.onchange = () => {

        const selectedImage = pfpFilePicker.files[0];

        if (selectedImage) {
            imageURL = URL.createObjectURL(selectedImage);
            
            pfpModal.showModal();

            cropper = new Croppie(cropPreview, {
                viewport: {width: 360, height: 360},
                boundary: {width: 480, height: 360},
                showZoomer: true,
            });

            cropper.bind({
                url: imageURL
            });

            URL.revokeObjectURL(imageURL);
        }
    }
});

closePfpModalButton.addEventListener("click", () => {
    pfpModal.close();
    cropper.destroy();
});

submitPfpButton.addEventListener("click", async () => {
    try {
        const blob = await cropper.result({type: 'blob'});
        const imageFile = new File([blob], pfpFilePicker.files[0].name, {type: "image/png", format: "png"});

        const formData = new FormData();
        formData.append("avatar", imageFile);

        const response = await fetch("/update-avatar/", {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            }
        });

        if (response.ok) {
            const data = await response.json();

            if (data.avatar) {
                pfpDiv.style.backgroundImage = `url(${data.avatar})`;
            } else {
                console.error("[ERROR] Invalid data in repsonse.");
            }
        } else {
            console.error("[ERROR] Request failed.");
        }
        pfpForm.reset();
        cropper.destroy();
        pfpModal.close();
    } catch (err) {
        console.error(err);
        pfpForm.reset();
        cropper.destroy();
        pfpModal.close();
    }
});

/*************************************/
/***** UPDATING BANNER ***************/
/*************************************/

const changeBannerButton = document.getElementById("changeBannerButton");
const closeBannerModalButton = document.getElementById("closeBannerModalButton");
const bannerModal = document.getElementById("bannerModal");
const bannerFilePicker = document.getElementById("bannerFilePicker");
const bannerDiv = document.getElementById("banner");
const bannerForm = document.getElementById("bannerForm");

changeBannerButton.addEventListener("click", () => {
    
    bannerFilePicker.click();

    bannerFilePicker.onchange = () => {
        const selectedImage = bannerFilePicker.files[0];

        if (selectedImage) {
            imageURL = URL.createObjectURL(selectedImage);

            bannerModal.showModal();

            let cropPreview = document.getElementById("bannerPreview");
            cropper = new Croppie(cropPreview, {
                viewport: {width: 480, height: 120},
                boundary: {width: 480, height: 360},
                showZoomer: true,
            });

            cropper.bind({
                url: imageURL
            });


            URL.revokeObjectURL(imageURL);
        }
    }
});

submitBannerButton.addEventListener("click", async () => {
    try {
        const blob = await cropper.result({type: 'blob', size: 'original'});
        const imageFile = new File([blob], bannerFilePicker.files[0].name, {type: "image/png", format: "png"});

        const formData = new FormData();
        formData.append("banner", imageFile);

        const response = await fetch("/update-banner/", {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            }
        });

        if (response.ok) {
            const data = await response.json();

            if (data.banner) {
                bannerDiv.style.backgroundImage = `url(${data.banner})`;
            } else {
                console.error("[ERROR] Invalid data in response.");
            }
        } else {
            console.error("[ERROR] Request failed.");
        }
        bannerForm.reset();
        cropper.destroy();
        bannerModal.close();
    } catch (err) {
        console.error(err);
        bannerForm.reset();
        cropper.destroy();
        bannerModal.close();
    }
});


closeBannerModalButton.addEventListener("click", () => {
    bannerModal.close();
    cropper.destroy();
});

/*************************************/
/***** RESET AVATAR ******************/
/*************************************/

const resetPfpButton = document.getElementById("resetPfpButton");

resetPfpButton.addEventListener("click", async () => {
    const response = await fetch("/reset-avatar/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    });

    if (response.ok) {
        const data = await response.json();

        if (data.default_avatar) {
            pfpDiv.style.backgroundImage = `url(${data.default_avatar})`;
        } else {
            console.error("[ERROR] Invalid data in response.");
        }
    } else {
        console.error("[ERROR] Request failed.");
    }
});

/*************************************/
/***** RESET BANNER ******************/
/*************************************/

const resetBannerButton = document.getElementById("resetBannerButton");

resetBannerButton.addEventListener("click", async () => {
    const response = await fetch("/reset-banner/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    });

    if (response.ok) {
        const data = await response.json();

        if (data.default_banner) {
            bannerDiv.style.backgroundImage = `url(${data.default_banner})`;
        } else {
            console.error("[ERROR] Invalid data in response.");
        }
    } else {
        console.error("[ERROR] Request failed.");
    }
});

/*************************************/
/***** ADD POST **********************/
/*************************************/

const addPostButton = document.getElementById("addPostButton");
const addPostForm = document.getElementById("addPostForm");
const postModal = document.getElementById("postModal");
const closePostModalButton = document.getElementById("closePostModalButton");
const postPreview = document.getElementById("postPreview");
const postFilePicker = document.getElementById("postFilePicker");
const submitPostButton = document.getElementById("submitPostButton");

addPostButton.addEventListener("click", () => {
    
    postFilePicker.click() ;

    postFilePicker.onchange = () => {

        const selectedImage = postFilePicker.files[0];

        if (selectedImage) {
            imageURL = URL.createObjectURL(selectedImage);
            
            postModal.showModal();

            cropper = new Croppie(postPreview, {
                viewport: {width: 480, height: 360},
                boundary: {width: 480, height: 360},
                showZoomer: true,
            });

            cropper.bind({
                url: imageURL
            });

            URL.revokeObjectURL(imageURL);
        }
    }
});

closePostModalButton.addEventListener("click", () => {
    postModal.close();
    cropper.destroy();
});

submitPostButton.addEventListener("click", async () => {
    try {
        const blob = await cropper.result({type: 'blob', size: 'original'});
        const imageFile = new File([blob], postFilePicker.files[0].name, {type: "image/png", format: "png"});

        const formData = new FormData();
        formData.append("media", imageFile);
        formData.append("caption", document.getElementById("captionText").value);

        const response = await fetch("/add-post/", {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            }
        });

        if (response.ok) {
            console.log("Added post");
        } else {
            console.error("[ERROR] Request failed.");
        }
        addPostForm.reset();
        cropper.destroy();
        postModal.close();
        window.location.reload();
    } catch (err) {
        console.error(err);
        addPostForm.reset();
        cropper.destroy();
        postModal.close();
        window.location.reload();
    }
});