function login(){
    login_btn = document.getElementById("login_btn");
    username = document.getElementById("username");
    password = document.getElementById("password");

    fetch('/validate', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'username': username.value,
            'password': password.value 
        }
    }).then(response => response.json())
    .then(data =>{
        if(data["Status"]){
            exist_form = document.querySelector('form');
            // if(exist_form){
            //     document.body.removeChild(exist_form)
            // }
            home_page(data["Token"])

        }else{
            alert("Usuário ou senha inválidos!")
            alert("Caso não tenha acesso, por gentileza realize o cadastro!")
        }
    }
    )
}

function create(){
    create_btn = document.getElementById("create_btn");
    exist_form = document.querySelector("form");
    if (exist_form){
        document.body.removeChild(exist_form);
    }
    form = document.createElement("form");
    username_inp = document.createElement('input');
    password_inp = document.createElement("input");
    confirm_pass = document.createElement("input");
    create_btn = document.createElement("input");
    username_inp.setAttribute("id", "username_inp");
    username_inp.setAttribute("type", "text");
    username_inp.setAttribute("placeholder", "Username");
    password_inp.setAttribute("id", "password_inp");
    password_inp.setAttribute("type", "password");
    password_inp.setAttribute("placeholder", "Password");
    confirm_pass.setAttribute("type", "password");
    confirm_pass.setAttribute("placeholder", "Confirm your pass");
    create_btn.setAttribute("id", "create_btn");
    create_btn.setAttribute("type", "button");
    create_btn.setAttribute("value", "Create");
    create_btn.onclick = function(){

    if (password_inp.value != confirm_pass.value){
            alert('Verifique se as credenciais se coincidem!');
        }
    else{
            fetch('/create', {
            method: 'POST',
            headers: {
                'username': username_inp.value,
                'password': confirm_pass.value
            }
        })
    }

    };

    form.appendChild(username_inp);
    form.appendChild(password_inp);
    form.appendChild(confirm_pass);
    form.appendChild(create_btn);

    document.body.appendChild(form);


}

function home_page(token){
    fetch('/home', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'token': token
        }
    }).then(response => response.json())
    .then(data =>{
        console.log(data)
    })
}