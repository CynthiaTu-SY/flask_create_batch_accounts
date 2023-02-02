import os

from flask import Blueprint, current_app, flash, render_template, request
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

from . import db
from .models import Account, Group

upload = Blueprint('upload', __name__)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def fileParse(filepath):
    file = open(filepath, 'r')
    Lines = file.readlines()
    file.close()
    os.remove(filepath)
    print('FP 1')
    groupcount = 0
    usercount = 0
    for line in Lines:
        try:
            userobject = []
            line = line.rstrip()
            account = line.split(':')
            print(account[0])
            # print(str(hash('pd1')))
            # print(account[1])
            # print(generate_password_hash(account[1], method='sha256')))
            groupexist = Group.query.filter_by(groupname = account[2]).first()
            userexist = Account.query.filter_by(username = account[0]).first()
            print("check exist done")
            if userexist:
                if check_password_hash(userexist.password, account[1]):
                # userexist.password == generate_password_hash(account[1], method='sha256'):
                    if not groupexist:
                        new_group = Group(groupname = account[2])
                        groupcount += 1
                        print("Create New Group")
                        new_group.users.append(userexist)
                        db.session.add(new_group)
                    else:
                        print("Append existing Group")
                        groupexist.users.append(userexist)
            else:
                new_user = Account(username = account[0], password = generate_password_hash(account[1], method='sha256'))
                usercount += 1
                if not groupexist:
                    new_group = Group(groupname = account[2])
                    groupcount += 1
                    print("Create New User and New Group")
                    new_group.users.append(new_user)
                    userobject.append(new_user)
                    db.session.add(new_group)
                    db.session.add_all(userobject)
                else:
                    print("Create New User and add to existing Group")
                    groupexist.users.append(new_user)
                    db.session.add_all(new_user)
            print("Start commit")
            db.session.commit()
        except:
            print('{} import failed'.format(line))
    return groupcount, usercount            

        
@upload.route('/', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        filename = file.filename
        print(filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[-1]
            if file_ext.upper() not in current_app.config['UPLOAD_EXTENSIONS']:
                flash('Only text (.txt) file is accepted', category='error')
            else:  
                filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)),current_app.config['UPLOAD_FOLDER'],'{}.txt'.format(filename))                  
                file.save(filepath) # Then save the filex
                if os.stat(filepath).st_size > 0:                    
                    # Windows & Linux
                    newGroup_no, newUser_no = fileParse(filepath)
                    flash('File ({0}) included {1} new groups and {2} new accounts has been uploaded.'.format(filename, newGroup_no, newUser_no), category='success')
                else:
                    os.remove(filepath)
                    flash('Empty is NOT accepted', category='error')            

    return render_template('upload.html', form=form)