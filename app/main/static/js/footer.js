const subscribe_form = document.getElementById("subscribe_form");
const subscribe_form_successMessage = document.getElementById("subscribe_form_successmessage");
const subscribe_form_fields = {
    csrf_token: {
    input: subscribe_form.querySelector("[id='csrf_token']"),
    error: subscribe_form.querySelector("[id='csrf_token-error']"),
    },
    email: {
    input: subscribe_form.querySelector("[id='email']"),
    error: subscribe_form.querySelector("[id='email-error']")
    }     
};

subscribe_form.addEventListener('submit', async (e) => {
    e.preventDefault();        
    
    subscribe_form_successMessage.style.display = 'none';
    for (var key of Object.keys(subscribe_form_fields)) {
        subscribe_form_fields[key].input.classList.remove('is-invalid');
        subscribe_form_fields[key].error.innerHTML = "";
    }
    const response = await fetch(fetch_footer_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            csrf_token: subscribe_form_fields.csrf_token.input.value,
            email: subscribe_form_fields.email.input.value
        })
    });
    if (response.ok) {            
        subscribe_form_successMessage.innerHTML = await response.text();
        subscribe_form.style.display = 'none';
        subscribe_form_successMessage.style.display = 'block';
    } else {
        const errors = await response.json();
        Object.keys(errors).forEach((key) => {
            subscribe_form_fields[key].input.classList.add('is-invalid');
            subscribe_form_fields[key].error.innerHTML = errors[key][0];
        });
    }
});
