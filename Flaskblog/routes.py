from flask import render_template, flash, redirect, url_for,request
from Flaskblog.forms import RegistrationForm, LoginForm,UpdateAccountForm
from Flaskblog import app,db,bcrypt
from Flaskblog.models import User , Post
from flask_login import login_user,current_user,logout_user,login_required


posts =[
    {
        'author':' Dorothy Kabarozi',
        'title':'Dealing with coding and backache',
        'content':'You can  never code while sleeping probably you will hurt yo back but sitting for long hours is also not that easy',
        'date_posted':'Jan 28th,2019'
    },
    {
        'author':' Dorothy Kabarozi',
        'title':'Moms can code too',
        'content':""" Distractions from our little ones,their cries their smiles always let us
                     leave what we are doing and attend to them.Being a coding mom is equally
                      not easy but it is doable """,
        'date_posted':'Jan 30th,2019'
    }
]
 
@app.route('/')
@app.route('/home')
#home function that displays the home page
def home():

    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    """
         about function that displays the about page
    """
    return render_template('about.html', title='About page')
    #  in this case if no methods the form does not submit

@app.route('/register', methods=["GET", "POST"])
def register():
    """
         register function that displays the registration page
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # one time alert use flash
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data , password = hashed_password )
        db.session.add(user)
        db.session.commit()
        # adding user to the database
        flash(f'Your account has been successfully created you can now login', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    # checking if current user is already logged in redirected

    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            # ternary conditional
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('You have an invalid password or email', 'danger')
            return render_template('login.html', title='login', form=form)

    return render_template('login.html', title='login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account',methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename ='profile_pics/'+ current_user.image_file)
    return render_template('account.html',
                             title='Account',image_file = image_file,form = form)
 