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