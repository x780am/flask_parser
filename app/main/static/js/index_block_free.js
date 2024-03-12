const free_form = document.getElementById("freeform");
const free_form_successMessage = document.getElementById("free_form_successmessage");
const freeform_spiner_btn = document.getElementById("freeform_spiner");
const freeform_submit_btn = document.getElementById("freeform_submit");

const free_form_fields = {
    csrf_token: {
    input: free_form.querySelector("[id='csrf_token']"),
    error: free_form.querySelector("[id='csrf_token-error']"),
    },
    url: {
    input: free_form.querySelector("[id='url']"),
    error: free_form.querySelector("[id='url-error']")
    },
    email: {
    input: free_form.querySelector("[id='email']"),
    error: free_form.querySelector("[id='email-error']")
    },
    checkPD: {
    input: free_form.querySelector("[id='checkPD']"),
    error: free_form.querySelector("[id='checkPD-error']")
    }     
};
const FreeFields = free_form.querySelector("[id='FreeFields']");

free_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    var LoaderModal = new bootstrap.Modal(document.getElementById('LoaderModal'), {
        keyboard: false 
      })
    LoaderModal.show();

    free_form_successMessage.style.display = 'none';
    for (var key of Object.keys(free_form_fields)) {
        free_form_fields[key].input.classList.remove('is-invalid');
        free_form_fields[key].error.innerHTML = "";
    }
    freeform_spiner_btn.style.display = 'block';
    freeform_submit_btn.style.display = 'none';
    FreeFields.disabled = true;
    
    const response = await fetch(fetch_block_free_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            csrf_token: free_form_fields.csrf_token.input.value,
            url: free_form_fields.url.input.value,
            email: free_form_fields.email.input.value,
            checkPD: free_form_fields.checkPD.input.value
        })
    });
    if (response.ok) {            
        free_form_successMessage.innerHTML = await response.text();
        free_form_successMessage.style.display = 'block';
        //free_form.style.display = 'none';
        
        FreeFields.disabled = false;
        freeform_submit_btn.style.display = 'block';
        freeform_spiner_btn.style.display = 'none';  
    } else {
        const errors = await response.json();
        Object.keys(errors).forEach((key) => {
            free_form_fields[key].input.classList.add('is-invalid');
            free_form_fields[key].error.innerHTML = errors[key][0];
        });
        FreeFields.disabled = false;
        freeform_submit_btn.style.display = 'block';
        freeform_spiner_btn.style.display = 'none'; 

    }
    LoaderModal.hide();
});
