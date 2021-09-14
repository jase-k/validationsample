from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection
import re
from datetime import datetime, date, time, timezone

db = 'users_schema'

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data['updated_at']
    
    def getMessages(self):
        query = f"SELECT * from messages LEFT JOIN users ON messages.sender_id = users.id WHERE reciever_id = {self.id}"

        messages = MySQLConnection(db).query_db(query)
        for message in messages: 
            difference = datetime.now() - message['created_at']
            #Calculates difference in time in hours
            time = round(difference.seconds/3600) 
            if time > 24: 
                time = time / 24
                message['time_ago'] = str(time) + ' days ago'
            else:
                message['time_ago'] = str(time) + ' hours ago'

        return messages

    def sendMessages(self, data):
        query = "INSERT INTO messages (message, reciever_id, sender_id, created_at, updated_at) Values(%(message)s, %(reciever)s, %(sender)s, NOW(), NOW())"

        id = MySQLConnection(db).query_db(query, data)

        return id

    @classmethod
    def getAllUsers(cls):
        query = "Select * from users"

        results = MySQLConnection(db).query_db(query)

        return results

    @classmethod
    def addNewUser(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW(), %(password)s)"

        query_data = {
            'first_name' : data['first_name'],
            'last_name' : data["last_name"],
            'email' : data["email"],
            'password' : data['password']
        }

        id = MySQLConnection(db).query_db(query, query_data)
        return id

    @classmethod
    def validateUser(cls, data):
        is_valid = True
        print('DATA PASSED for Validation: ', data)
        #validates First_Name: 
        if(len(data['first_name']) < 2):
            flash("First Name must be greater than two characters", 'first_name')
            is_valid = False
        #validates Last_Name: 
        if(len(data['last_name']) < 2):
            flash("First Name must be greater than two characters", 'last_name')
            is_valid = False
        #Validates Email:
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if( not EMAIL_REGEX.match(data['email'])):
            flash("Must enter valid email", 'email')
            is_valid = False
        #Validates Password:
        if(len(data['confirm_password']) < 8):
            flash("Password must be at least 8 characters", 'password')
            is_valid = False
        numberandchar = re.compile(r'^.*[0-9].*')
        if(not numberandchar.match(data['confirm_password'])):
            flash("Password must contain at least 1 number", 'password')
            is_valid = False
        #Validates CheckBox:
        if(not data['agree_to_terms']):
            flash("Must accept terms to continue", "checkbox")
            is_valid = False

        return is_valid

    
    @classmethod
    def getUserByEmail(cls, email):
        query = "SELECT * from Users WHERE email = %(email)s"

        data = {
            "email" : email
        }

        results = MySQLConnection(db).query_db(query, data)

        #since SELECT query always returns an array, we only return the first result 
        if results:
            return results[0]
        else:
            return False

    @classmethod
    def getUserById(cls, id):
        query = "SELECT * from Users WHERE id = %(id)s"

        data = {
            "id" : id
        }

        results = MySQLConnection(db).query_db(query, data)
        user = User(results[0])

        #since SELECT query always returns an array, we only return the first result 
        return user
