const contact_form = document.getElementById("contact_form");
const contact_form_successMessage = document.getElementById("contact_form_successmessage");
const contact_form_fields = {
  csrf_token: {
    input: contact_form.querySelector("[id='csrf_token']"),
    error: contact_form.querySelector("[id='csrf_token-error']"),
  },
  name: {
    input: contact_form.querySelector("[id='name']"),
    error: contact_form.querySelector("[id='name-error']")
  },
  email: {
    input: contact_form.querySelector("[id='email']"),
    error: contact_form.querySelector("[id='email-error']")
  },
  message: {
    input: contact_form.querySelector("[id='message']"),
    error: contact_form.querySelector("[id='message-error']")
  }     
};

contact_form.addEventListener('submit', async (e) => {
    e.preventDefault();        
    contact_form_successMessage.style.display = 'none';
    for (var key of Object.keys(contact_form_fields)) {
        contact_form_fields[key].input.classList.remove('is-invalid');
        contact_form_fields[key].error.innerHTML = "";
    }
    const response = await fetch(fetch_block_contact_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            csrf_token: contact_form_fields.csrf_token.input.value,
            name: contact_form_fields.name.input.value,
            email: contact_form_fields.email.input.value,
            message: contact_form_fields.message.input.value
        })
    });
    if (response.ok) {            
        contact_form_successMessage.innerHTML = await response.text();
        contact_form.style.display = 'none';
        contact_form_successMessage.style.display = 'block';
    } else {
        const errors = await response.json();
        Object.keys(errors).forEach((key) => {
            contact_form_fields[key].input.classList.add('is-invalid');
            contact_form_fields[key].error.innerHTML = errors[key][0];
        });
    }
});
