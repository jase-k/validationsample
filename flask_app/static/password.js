console.log("JavaScript Connected!")
var confirmPW = document.getElementById("confirm_password");
var PW = document.getElementById("password");
var registrationButton = document.getElementById('register')

function pwvalidator(){
    if(PW.value != confirmPW.value){
        if(!confirmPW.parentElement.lastElementChild.innerHTML){
            var warning = document.createElement("p")
            warning.classList = ["error"]
            warning.id = 'pwcheck'
            warning.innerHTML = "Passwords Must Match"
            warning = confirmPW.parentElement.appendChild(warning)
        }
        register.type = 'button'
    }
    else{
        document.getElementById('pwcheck').remove()
        register.type = 'submit'
    }
};

function hide(e){
    console.log(e)
    e.remove()
}