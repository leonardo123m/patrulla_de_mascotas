function signIn() {
    let oauthEndpoint = "https://accounts.google.com/o/oauth2/v2/auth";

    // Crear el formulario correctamente
    let form = document.createElement('form');
    form.setAttribute('method', 'GET');
    form.setAttribute('action', oauthEndpoint);

    // Parámetros para la autenticación
    let params = {
        "client_id": "628880919045-8dac5sgt2c77h7pvhlrdpqied69amuc1.apps.googleusercontent.com",
        "redirect_uri": "http://127.0.0.1:5500/profile",

        "response_type": "token",
        "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email  https://www.googleapis.com/auth/youtube.readonly",
        "include_granted_scopes": 'true',
        'state': 'pass-through-value'
    };
    

    // Añadir los parámetros al formulario como inputs ocultos
    for (var p in params) {
        let input = document.createElement('input'); // Corrección aquí
        input.setAttribute('type', 'hidden');
        input.setAttribute('name', p);
        input.setAttribute('value', params[p]);
        form.appendChild(input);
    }

    // Añadir el formulario al cuerpo del documento y enviarlo
    document.body.appendChild(form);
    form.submit();
}

const pass = document.getElementById('pass'),
        icono = document.querySelector('.ojo');
icono.addEventListener("click", e => {
    if(pass.type === "password"){
        pass.type = "text";
        icono.classList.remove('bi-eye-slash')
        icono.classList.add('bi-eye')
    } else {
        pass.type = "password"
        icono.classList.add('bi-eye-slash')
        icono.classList.remove('bi-eye')
    }
    
})

