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

// var trash_icons = document.getElementsByClassName('trash')
// console.log(trash_icons)

// for(var i = 0; i< trash_icons.length; i++){
//     console.log("i'm in the for loop")
//     trash_icons[i].addEventListener('click',  (this)=>{
//         console.log(this)
//         hideGrandParent(this)
//     })
//     //  hideGrandParent(trash_icons[i])
// }

function hideGrandParent(node){
    node.parentElement.parentElement.remove()
}