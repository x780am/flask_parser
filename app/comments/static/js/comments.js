const commentAdd_form = document.getElementById("commentAdd_form");
const commentAdd_form_successMessage = document.getElementById("commentAdd_form_successmessage");
const commentAdd_form_fields = {
    csrf_token: {
    input: commentAdd_form.querySelector("[id='csrf_token']"),
    error: commentAdd_form.querySelector("[id='csrf_token-error']"),
    },
    name: {
    input: commentAdd_form.querySelector("[id='name']"),
    error: commentAdd_form.querySelector("[id='name-error']")
    },
    email: {
    input: commentAdd_form.querySelector("[id='email']"),
    error: commentAdd_form.querySelector("[id='email-error']")
    },
    message: {
    input: commentAdd_form.querySelector("[id='message']"),
    error: commentAdd_form.querySelector("[id='message-error']")
    }     
};

commentAdd_form.addEventListener('submit', async (e) => {
    e.preventDefault();        
    
    commentAdd_form_successMessage.style.display = 'none';
    for (var key of Object.keys(commentAdd_form_fields)) {
        commentAdd_form_fields[key].input.classList.remove('is-invalid');
        commentAdd_form_fields[key].error.innerHTML = "";
    }
    const response = await fetch(fetch_comments_add_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            csrf_token: commentAdd_form_fields.csrf_token.input.value,
            name: commentAdd_form_fields.name.input.value,
            email: commentAdd_form_fields.email.input.value,
            message: commentAdd_form_fields.message.input.value
        })
    });
    if (response.ok) {            
        commentAdd_form_successMessage.innerHTML = await response.text();
        commentAdd_form.style.display = 'none';
        commentAdd_form_successMessage.style.display = 'block';
    } else {
        const errors = await response.json();
        Object.keys(errors).forEach((key) => {
            commentAdd_form_fields[key].input.classList.add('is-invalid');
            commentAdd_form_fields[key].error.innerHTML = errors[key][0];
        });
    }
});

async function public_comment(comment_id, public){
    const response = await fetch(fetch_comments_public_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: comment_id,
            public: public
        })
    });
    if (response.ok) {
        location.reload();    
    } else {
        alert(await response.json());
    }
    return false;
}

async function del_comment(comment_id, admin=0){
    const response = await fetch(fetch_comments_delete_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: comment_id
        })
    });
    if (response.ok) {
        location.reload();    
    } else {
        alert(await response.json());
    }
    return false;
}

function edit_comment(comment_id){
    const EditCommentModal = document.getElementById('EditCommentModal');
    const modal = new bootstrap.Modal(EditCommentModal);
    EditCommentModal.querySelector("[id='EditCommentModalLabel']").innerHTML='Изменить отзыв';
    EditCommentModal.querySelector("[id='text']").innerHTML=document.getElementById("comment_text_"+comment_id).innerHTML;
    EditCommentModal.querySelector("[id='id']").setAttribute("value", comment_id);
    EditCommentModal.querySelector("[id='answer']").setAttribute("value", 0);
    EditCommentModal.querySelector("[id='email']").setAttribute("value", 'none');
    EditCommentModal.querySelector("[id='comment_text']").setAttribute("value", 'none');
    modal.show();
}

function answer_comment(comment_id, email){
    const EditCommentModal = document.getElementById('EditCommentModal');
    const modal = new bootstrap.Modal(EditCommentModal);
    EditCommentModal.querySelector("[id='EditCommentModalLabel']").innerHTML='Ответить на отзыв';
    EditCommentModal.querySelector("[id='text']").innerHTML='';
    EditCommentModal.querySelector("[id='id']").setAttribute("value", comment_id);
    EditCommentModal.querySelector("[id='answer']").setAttribute("value", 1);
    EditCommentModal.querySelector("[id='email']").setAttribute("value", email);
    EditCommentModal.querySelector("[id='comment_text']").setAttribute("value", document.getElementById("comment_text_"+comment_id).innerHTML);
    modal.show();
}


const EditComment_form = document.getElementById("EditComment_form");
const EditComment_form_fields = {
    csrf_token: {
    input: EditComment_form.querySelector("[id='csrf_token']"),
    error: EditComment_form.querySelector("[id='csrf_token-error']"),
    },
    text: {
    input: EditComment_form.querySelector("[id='text']"),
    error: EditComment_form.querySelector("[id='text-error']")
    },
    id: {
    input: EditComment_form.querySelector("[id='id']"),
    error: EditComment_form.querySelector("[id='id-error']")
    },
    answer: {
    input: EditComment_form.querySelector("[id='answer']"),
    error: EditComment_form.querySelector("[id='answer-error']")
    },
    email: {
    input: EditComment_form.querySelector("[id='email']"),
    error: EditComment_form.querySelector("[id='email-error']")
    },
    comment_text: {
    input: EditComment_form.querySelector("[id='comment_text']"),
    error: EditComment_form.querySelector("[id='comment_text-error']")
    }  
};

EditComment_form.addEventListener('submit', async (e) => {
    e.preventDefault();        
    
    for (var key of Object.keys(EditComment_form_fields)) {
        EditComment_form_fields[key].input.classList.remove('is-invalid');
        EditComment_form_fields[key].error.innerHTML = "";
    }
    if (EditComment_form_fields.answer.input.value == 1){
        url = fetch_comments_answer_url
    }
    else{
        url = fetch_comments_edit_url
    }
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            csrf_token: EditComment_form_fields.csrf_token.input.value,
            text: EditComment_form_fields.text.input.value,
            id: EditComment_form_fields.id.input.value,
            answer: EditComment_form_fields.answer.input.value,
            email: EditComment_form_fields.email.input.value,
            comment_text: EditComment_form_fields.comment_text.input.value
        })
    });
    if (response.ok) {          
        location.reload();
    } else {
        const errors = await response.json();
        Object.keys(errors).forEach((key) => {
            EditComment_form_fields[key].input.classList.add('is-invalid');
            EditComment_form_fields[key].error.innerHTML = errors[key][0];
        });
    }
});