from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models import model_users


class Timecard:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.start_day = data['start_day']
        self.end_day = data['end_day']
        self.job_number_1 = data['job_number_1']
        self.hours_1 = data['hours_1']
        self.job_number_2 = data['job_number_2']
        self.hours_2 = data['hours_2']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.processed = data['processed']



#validation
    @staticmethod
    def validate(data):
        is_valid = True

        if not data["start_day"]:
            flash("start_day required","err_timecards_start_day")
            is_valid=False

        if not data["end_day"]:
            flash("end_day required","err_timecards_end_day")
            is_valid=False

        if not data["job_number_1"] :
            flash("date required","err_timecards_job_number_1")
            is_valid=False

        if not data["hours_1"]:
            flash("hours required","err_timecards_hours_1")
            is_valid=False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO timecards (start_day, end_day, job_number_1, hours_1, job_number_2, hours_2, user_id) VALUES (%(start_day)s,%(end_day)s,%(job_number_1)s,%(hours_1)s,%(job_number_2)s,%(hours_2)s,%(user_id)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data) 

        return user_id
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM timecards WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False

        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM timecards"
        results = connectToMySQL(DATABASE).query_db(query)

        all_timecards = []
        for dict in results:
            all_timecards.append(cls(dict))

        return all_timecards

    @classmethod
    def get_all_by_user_id(cls,data):
        query = "SELECT * FROM timecards WHERE user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return []

        all_timecards = []
        for dict in results:
            all_timecards.append(cls(dict))

        return all_timecards

    @classmethod
    def get_all_by_employee_id(cls,data):
        query = "SELECT * FROM timecards WHERE employee_id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return []

        all_timecards = []
        for dict in results:
            all_timecards.append(cls(dict))

        return all_timecards

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM timecards JOIN users ON timecards.user_id = users.id WHERE timecards.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return False

        results = results[0]
        
        user_data = {
            'id' : results['users.id'],
            'first_name' : results['first_name'],
            'last_name' : results['last_name'],
            'password' : results['password'],
            'employee_id' : results['employee_id'],
            'created_at' : results['users.created_at'],
            'updated_at' : results['users.updated_at'],
            'admin' : results['admin'],
        }
#TODO might not need this dictionary
        timecard_data = {
            'id' :results['id'],
            'start_day' :results['start_day'],
            'end_day' :results['end_day'],
            'job_number_1' :results['job_number_1'],
            'hours_1' :results['hours_1'],
            'job_number_2' :results['job_number_2'],
            'hours_2' :results['hours_2'],
            'created_at' :results['created_at'],
            'updated_at' :results['updated_at'],
            'user_id' :results['user_id'],
            'processed' :results['processed'],
        }

        timecard = Timecard(timecard_data)
        timecard.user = model_users.User(user_data)

        return timecard

#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE timecards SET start_day = %(start_day)s, end_day = %(end_day)s, job_number_1 = %(job_number_1)s, hours_1 =%(hours_1)s,job_number_2 = %(job_number_2)s, hours_2 =%(hours_2)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def process(cls,data):
        query = "UPDATE timecards SET processed = %(processed)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM timecards WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)



    # @classmethod
    # def get_all_with_liked(cls):
    #     query = "SELECT * FROM timecards LEFT JOIN liked_shows ON timecards.id = timecard_id JOIN users ON users.id = timecards.user_id;"
    #     results = connectToMySQL(DATABASE).query_db(query)

    #     if not results:
    #         return []

    #     all_timecards = []
    #     for dict in results:
    #         timecard_data = {
    #             'id' : dict['id'],
    #             'start_day' : dict['start_day'],
    #             'end_day' : dict['end_day'],
    #             'hours_1' : dict['hours_1'],
    #             'job_number_1' : dict['job_number_1'],
    #             'created_at' : dict['created_at'],
    #             'updated_at' : dict['updated_at'],
    #             'user_id' : dict['user_id'],
    #         }
            
    #         user_data = {
    #             'id':dict['users.id'],
    #             'first_name' : dict['first_name'],
    #             'last_name' : dict['last_name'],
    #             'email' : dict['email'],
    #             'password' : dict['password'],
    #             'created_at' : dict['created_at'],
    #             'updated_at' : dict['updated_at'],
    #         }

    #         liked_data = {
    #             'user_id':dict['liked_shows.user_id'],
    #             'timecard_id': dict['timecard_id'],
    #         }

    #         timecard = cls(timecard_data)
    #         timecard.users = model_users.User(user_data)
    #         timecard.liked = model_liked_shows.Liked_show(liked_data)
    #         all_timecards.append(timecard)
            
    #     return all_timecards


