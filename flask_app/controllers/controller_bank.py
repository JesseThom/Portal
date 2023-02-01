from flask import render_template, redirect, session, request
from flask_app import app
from cryptography.fernet import Fernet
from flask_app.config.helpers import encrypt,decrypt

from flask_app.models.model_banks import Bank
from flask_app.models.model_users import User

#route to create new bank
@app.route('/employee/<employee_id>/bank/new')
def bank_new(employee_id):
    if 'uuid' not in session:
        return redirect('/')

    admin = session['admin']
    user = User.get_one_by_employee_id({'employee_id': employee_id})

    return render_template('/users/bank_new.html',admin=admin,user=user)

#route to submit create bank form
@app.route('/bank/<employee_id>/<int:id>/create',methods=['post'])
def bank_create(employee_id,id):

    if not Bank.validate(request.form):
        return redirect(f'/employee/{employee_id}/bank/edit')

    encrypted_data = {
        'bank_name':encrypt(request.form['bank_name']),
        'routing': encrypt(request.form['routing']),
        'account': encrypt(request.form['account']),
        'user_id': id,
    }

    bank_id = Bank.create(encrypted_data)

    if bank_id == False:
        print("Failed to create bank")
    else:
        print(f"bank Created at {bank_id} id")
    if session['admin'] == 1:
        return redirect(f'/admin/employee/{employee_id}')
    else:
        return redirect('/dashboard')


#route to edit bank
@app.route('/employee/<employee_id>/bank/edit')
def bank_edit(employee_id):
    if 'uuid' not in session:
        return redirect('/')

    admin = session['admin']
    user = User.get_one_with_bank({'employee_id': employee_id})

    return render_template('/users/bank_edit.html',admin=admin,user=user)

#route to submit edit form
@app.route('/bank/<int:id>/update',methods=['post'])
def bank_update(id):

    if not Bank.validate(request.form):
        return redirect('bank/new')

    encrypted_data = {
        'bank_name':encrypt(request.form['bank_name']),
        'routing': encrypt(request.form['routing']),
        'account': encrypt(request.form['account']),
        'id': id,
    }

        
    Bank.update_one(encrypted_data)

    return redirect('/dashboard')