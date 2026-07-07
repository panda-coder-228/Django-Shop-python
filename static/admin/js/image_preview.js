document.addEventListener("change", function(e){
    const input = e.target;

    if(input.type != "file" || !input.files || !input.files[0]) return;

    const file = input.files[0]
    const url = URL.createObjectURL(file);

    // main_prview_image

    if(!input.closet(".inline-related, tr.form-row")){
        const mainPreview = document.getElementById("main-preview-img");
        const noPhotoText = mainPreview?.nextElementSibling;

        if (mainPreview){
            mainPreview.src = URL.createObjectURL(file)
            mainPreview.style.display = "block";
        }
        if (noPhotoText && noPhotoText.classList.contains(".no-photo-text")){
            noPhotoText.style.display = "none";
        }

        return;
    }

    // inline image Preview

    const inlineRow = input.closet(".inline-releted, tr.form-row");
    if (!inlineRow) return;

    const preview = inlineRow.querySelectorAll(".inline-preview-img");
    const noPhotoText = inlineRow.querySelector(".no-photo-text");

    preview.forEach(preview => {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    });

    if (noPhotoText){
        noPhotoText.style.display = "none"
    }
})


// preview_image_category
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("id_image_category");

    if (!input) return;

    const preview = document.querySelector(".main-image-category");

    input.addEventListener("change", function () {
        const file = this.files[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";
        };

        reader.readAsDataURL(file);
    });
});