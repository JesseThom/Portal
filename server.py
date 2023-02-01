from flask_app import app
from flask_app.controllers import  controller_routes, controller_timecards, controller_users, controller_bank,controller_paystubs

if __name__ == "__main__":
    app.run(debug=True)