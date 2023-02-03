import uuid

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash

from . import db
from .models import Account, Group

result = Blueprint('result', __name__)

@result.route('/login', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        username = request.form.get('username')
        password= request.form.get('password')
        user = Account.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                linkuuid = uuid.uuid4().hex
                return redirect(url_for("result.showgroupmembers", username=username, linkuuid=linkuuid, page=1))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')
    return render_template("login.html")


@result.route('/groupmates/<username>/<linkuuid>/<int:page>', methods=['GET', 'POST'])
def showgroupmembers(username, linkuuid, page):
    print("Enter the groumate function!")
    end_page = False
    limit = 20
    current_user = Account.query.filter_by(username=username).first()
    print(current_user.groups)
    groupmates_list = db.session.query(Group.groupname, Account.username)\
        .join(Group.users)\
        .filter(Group.users.contains(current_user),Account.id != current_user.id)\
        .order_by(Group.id.asc())\
        .offset((page-1)*limit)\
        .limit(limit+1)\
        .all()
    print('you have {} groupmates'.format(len(groupmates_list)))
    if not groupmates_list:
        if page != 1:
            flash('Incorrect page index in url, report is ended in previous page.', category='error')
        else:
            flash('No groupmate found in data base!', category='error')
        end_page = True
    elif len(groupmates_list) <= limit:
        end_page = True
    else:
        groupmates_list.pop()
    return render_template("groupmates.html", username=username, linkuuid = linkuuid, batchresult=groupmates_list, page=page, end=end_page)