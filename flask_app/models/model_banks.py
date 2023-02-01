from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DATABASE, bcrypt
import re
# from flask_app.models import model_timecards

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Bank:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.bank_name = data['bank_name']
        self.routing = data['routing']
        self.account = data['account']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


#create validation
    @staticmethod
    def validate(data):
        is_valid = True

        if len(data["bank_name"]) < 2:
            flash("Bank name must be at least 2 characters.","err_banks_bank_name")
            is_valid=False

        if len(data["routing"]) != 9:
            flash("routing number must be 9 characters","err_banks_routing")
            is_valid=False

        if len(data['account']) != 6:
            flash("account number must be 6 characters.","err_banks_account")
            is_valid=False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO banks (bank_name, routing, account,user_id) VALUES (%(bank_name)s, %(routing)s, %(account)s, %(user_id)s);"
        bank_id = connectToMySQL(DATABASE).query_db(query, data) 

        return bank_id
#R
    @classmethod
    def get_one_by_user_id(cls, data):
        query = "SELECT * FROM banks WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)

        if not results:
            return False

        return cls(results[0])

#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE banks SET bank_name = %(bank_name)s, routing = %(routing)s, account = %(account)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)

# #D
#     @classmethod
#     def delete_one(cls,data):
#         query = "DELETE FROM banks WHERE id = %(id)s;"

#         return connectToMySQL(DATABASE).query_db(query,data)