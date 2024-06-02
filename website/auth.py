from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", yup = True)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Invalid Email', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(password1) < 7:
            flash('password must be at least 7 characters', category='error')
        elif password1 != password2:
            flash('passwords dont match', category='error')
        else:
            # add user to database
            flash('account created', category='success')

    return render_template("sign_up.html")