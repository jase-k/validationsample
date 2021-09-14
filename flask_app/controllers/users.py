import re
from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.user import User
import bcrypt


@app.route('/')
def main():
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/login')
def loginPage():
    print(session)
    if 'id' in session:
        return redirect(f"/users/{session['id']}")
    else:
        return render_template('login_registration.html')

@app.route('/new_user', methods = ["POST"])
def addUser():
    print("FORM DATA: ", request.form)

    data = {
            'first_name' : request.form["first_name"],
            'last_name' : request.form["last_name"],
            'email' : request.form["email"],
            'password' : bytes(request.form["password"], "utf8"),
            'confirm_password' : request.form['password'],
            'agree_to_terms' : request.form.get("checkbox")
    }

    data['password'] = bcrypt.hashpw(data["password"], bcrypt.gensalt(14)),
    
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    session['email'] = data['email']

    if(User.validateUser(data)):
        id = User.addNewUser(data)
        session['id'] = id
        return redirect (f'/users/{id}')
    else:
        return redirect('/login')





@app.route('/users', methods = ["POST"])
def loginAttempt():
    user = User.getUserByEmail(request.form["email"])
    session["email"] = request.form['email']
    if not user:
        session["feedback"] = "user email not found"
        return redirect('/login')
        
    data = {
        'email' : request.form["email"],
        'password' : request.form["password"]
    }

    print("USER DATA: ", user['password'])
    print("DATA: ", data)
    if(bcrypt.checkpw(bytes(data["password"], "utf8"), bytes(user['password'], "utf8"))):
        print("successful Login")
        session["id"] = user['id']
        return redirect(f'/users/{user["id"]}')
    else:
        session["feedback"] = "user email/password combonation not found"
        return redirect('/login')


@app.route('/users/<int:id>')
def displayUserPage(id):
    user = User.getUserById(id)
    print("USER DATA: ", user)

    allusers = User.getAllUsers()
    messages = user.getMessages()

    print('messages: :', messages)

    if 'id' in session:
        if session['id'] == user.id:
            return render_template("user_dashboard.html", user=user, friends = allusers, messages = messages)
    return redirect('/')

@app.route('/users/<int:id>/sendmessage', methods=["POST"])
def sendMessage(id):
    data = {
        "message": request.form['pm'],
        "sender": id,
        "reciever": request.form['reciever']
    }
    print("Sending Data to Messages Table: ", data)

    User.getUserById(id).sendMessages(data)
    
    return redirect(f'/users/{id}')