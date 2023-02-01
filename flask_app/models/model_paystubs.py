from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models import model_users

class Paystub:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.name = data['name']
        self.url = data['url']
        self.created_at = data['created_at']
        self.employee_id = data['employee_id']


# create validation
    @staticmethod
    def validate(data):
        is_valid = True

        if not data['file']:
            flash("File required.","err_paystubs_url")
            is_valid=False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO paystubs (name, url,employee_id) VALUES (%(name)s, %(url)s, %(employee_id)s);"
        paystub_id = connectToMySQL(DATABASE).query_db(query, data) 

        return paystub_id

#R
    @classmethod
    def get_all_by_employee_id(cls,data):
        query = "SELECT * FROM paystubs WHERE employee_id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)

        all_paystubs = []
        for dict in results:
            all_paystubs.append(cls(dict))

        return all_paystubs

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM paystubs WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)

        if not results:
            return False

        return cls(results[0])

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM paystubs JOIN users ON paystubs.employee_id = users.employee_id WHERE paystubs.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)

        results = results[0]
        print(results)
        user_data = {
            'id' : results['users.id'],
            'first_name' : results['first_name'],
            'last_name' : results['last_name'],
            'password' : results['password'],
            'employee_id' : results['employee_id'],
            'created_at' : results['users.created_at'],
            'updated_at' : results['updated_at'],
            'admin' : results['admin'],
        }

        paystub = Paystub(results)
        paystub.user = model_users.User(user_data)

        return paystub


# #U
#     @classmethod
#     def update_one(cls,data):
#         query = "UPDATE banks SET bank_name = %(bank_name)s, routing = %(routing)s, account = %(account)s WHERE id = %(id)s;"

#         return connectToMySQL(DATABASE).query_db(query,data)

# #D
#     @classmethod
#     def delete_one(cls,data):
#         query = "DELETE FROM banks WHERE id = %(id)s;"

#         return connectToMySQL(DATABASE).query_db(query,data)