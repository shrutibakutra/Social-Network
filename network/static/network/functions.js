document.addEventListener('DOMContentLoaded', function() {
    // Add post API fetch call
    const form = document.querySelector("#compose-form");
    let element = document.createElement('div');
    text_f = document.querySelector("#compose-text");

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        fetch('/addPost', {

                method: 'POST',
                body: JSON.stringify({
                    text: document.querySelector('#compose-text').value,
                })
            })
            .then(response =>
                response.json(),
                text_f.value = "",

                //create a new element for reflecting newly added post
                element.className = `border`,
                element.style = `width:95%;height:100px;margin-left: 20px;margin-top: 20px;background-color:lightgreen;text-align:center`,
                element.innerHTML = `<div class="card-body"  id="item-show" >
                <br>
                The post has been created successfully!
                </div>`,
                document.querySelector("#main-view").appendChild(element),
            )
    })


    //Edit post api fetch call
    // edit = document.querySelectorAll(".edit");
    // text_area = document.querySelectorAll(".textarea");

    // edit.forEach((element) => {
    //     element.addEventListener("click", () => {
    //         handleEdit(element)
    //     })
    // })
})

// function handleEdit(element) {
//     console.log("in handle edit function")
//     post_id = element.getAttribute("data-id");
//     edit_btn = document.querySelector(`#edit-btn-${post_id}`);

//     if (edit_btn.textContent = 'Edit') {
//         document.querySelector(`#post-box-${post_id}`).style.display = "none";
//         document.querySelector(`post-edit-${post_id}`).style.display = "block";
//         edit_btn.textContent = "Save";
//         edit_btn.setAttribute("class", "text-success edit");
//     } else if (edit_btn.textContent = 'Save') {
//         edited_text = document.querySelector(`#post-edit-${post_id}`).value
//         editPost(post_id, edited_text)
//         edit_btn.textContent = "Edit";
//         edit_btn.setAttribute("class", "text-primary edit");
//     }
// }

// function editPost(id, newtext) {

//     fetch(`edit/${id}`, {
//         method = 'POST',
//         body: newtext,
//     }).then((res) => {
//         document.querySelector(`#post-content-${id}`).textContent = newtext;
//         document.querySelector(`#post-box-${id}`).style.display = "block";
//         document.querySelector(`#post-edit-${id}`).style.display = "none";
//     })
// }