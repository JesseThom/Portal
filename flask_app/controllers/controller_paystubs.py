from flask import render_template, redirect, session, request,url_for
from flask_app import app,BUCKET
from werkzeug.utils import secure_filename
import os
import boto3
import key_config as keys

from flask_app.models.model_paystubs import Paystub
from flask_app.models.model_timecards import Timecard


#route to create new paystub
@app.route('/admin/employee/<employee_id>/timecard/<int:id>/<int:processed>/paystub')
def paystub_new(employee_id,id,processed):
    if 'uuid' not in session:
        return redirect('/')
    elif session['admin'] != 1:
        return redirect('/')

    timecard = Timecard.get_one({'id': id})
    return render_template('/admin/paystub_new.html',timecard=timecard,employee_id=employee_id,processed=processed)

#route to submit create paystub form
@app.route('/employee/<employee_id>/<int:id>/<int:processed>/paystub/create',methods=['post'])
def paystub_create(employee_id,id,processed):
    if not Paystub.validate(request.files):
        return redirect(f'/admin/employee/{employee_id}/timecard/{id}/{processed}/paystub')
    if processed == 0:
        processed = 1
    else:
        processed = 0

# file upload to s3***********************
    s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key= keys.ACCESS_SECRET_KEY
                    )


    pdf = request.files['file']
    filename = secure_filename(pdf.filename)

    pdf.save(filename)
    s3.upload_file(
        Bucket = BUCKET,
        Filename=filename,
        Key = filename
    )
    os.remove(filename)
#******************************************

    #file upload to local server*************************
    # image = request.files['file']
    # filename = secure_filename(image.filename)
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # image.save(os.path.join(basedir,app.upload_folder,filename))
    #*****************************************************

    paystub_data = {
        **request.form,
        'employee_id':employee_id,
        'url': filename
    }
    timecard_data = {
        'id': id,
        'processed':processed
    }
    Timecard.process(timecard_data)
    paystub_id = Paystub.create(paystub_data) 
    if paystub_id == False:
        print("Failed to create paystub")
    else:
        print(f"paystub Created at {paystub_id} id")

    return redirect('/')

@app.route('/paystub/<int:id>/show')
def paystub_show(id):
    if 'uuid' not in session:
        return redirect('/')

    paystub = Paystub.get_one_with_user({'id':id})
    return render_template('/paystubs/paystub_show.html',admin=session['admin'],paystub=paystub,bucket=BUCKET)


# #delete user route
# @app.route('/user/<int:id>/delete')
# def user_delete(id):
#     User.delete_one({'id': id})
#     return redirect('/')