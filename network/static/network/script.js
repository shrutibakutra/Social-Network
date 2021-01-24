edit = document.querySelectorAll(".edit");
text_area = document.querySelectorAll(".textarea");
like = document.querySelectorAll(".post-like");

//Edit post api fetch call
edit.forEach((element) => {
    element.addEventListener("click", () => {
        handleEdit(element)
    })

});

//Like post
like.forEach((element) => {
    element.addEventListener("click", () => {
        handleLike(element)
    })
});

function editPost(id, newtext) {
    form = new FormData();
    form.append("id", id);
    form.append("text", newtext.trim());
    fetch("edit", {
        method: 'POST',
        body: form,
    }).then((res) => {
        document.querySelector(`#post-content-${id}`).textContent = newtext;
        document.querySelector(`#post-box-${id}`).style.display = "block";
        document.querySelector(`#post-edit-${id}`).style.display = "none";
    })
}

function handleEdit(element) {
    post_id = element.getAttribute("data-id");
    edit_btn = document.querySelector(`#edit-btn-${post_id}`);
    if (edit_btn.textContent == 'Save') {
        edited_text = document.querySelector(`#post-edit-${post_id}`).value;
        //Fetch edit api 
        editPost(post_id, edited_text);
        edit_btn.textContent = "Edit";
        edit_btn.setAttribute("class", "text-primary edit");
    } else if (edit_btn.textContent = 'Edit') {

        document.querySelector(`#post-box-${post_id}`).style.display = "none";
        document.querySelector(`#post-edit-${post_id}`).style.display = "block";
        document.querySelector(`#post-edit-${post_id}`).style.width = "80%";
        edit_btn.textContent = 'Save';
        edit_btn.setAttribute("class", "text-success edit");

    }
}

function likePost(id, is_liked) {
    console.log(is_liked)
    post_id = id
    form = new FormData();
    form.append("post_id", post_id);
    form.append("is_liked", is_liked);

    fetch("like", {
            method: 'POST',
            body: form,
        }).then((res) => res.json())
        .then((res) => {
            if (res.status == 201) {
                if (res.is_liked === "yes") {
                    icon.src = "https://img.icons8.com/plasticine/100/000000/like.png";
                    // element.setAttribute("data-is_liked", "yes");
                    is_liked = "yes"
                } else {
                    icon.src =
                        "https://img.icons8.com/carbon-copy/100/000000/like--v2.png";
                    // element.setAttribute("data-is_liked", "no");
                    is_liked = "no"
                }
                count.textContent = res.like_count;
            }
        })
        .catch(function(res) {
            alert("Network Error. Please Check your connection.");
        });
}

function handleLike(element) {
    post_id = element.getAttribute("data-id");
    is_liked = element.getAttribute("data-is_liked");

    like_btn = document.querySelector(`#post-like-${post_id}`);
    likePost(post_id, is_liked)
}