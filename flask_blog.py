from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '79d64c304c964d793be61e7fc7696a9b'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
# sqlite /// specify the relative path 
# secret key for this app
# config values in our application app.config
db = SQLAlchemy(app)


# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # backref-adding another column if we have apost we can get ts author

#    this method specifies how the object will be printed out
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(100),unique=True,nullable=False)
    date_posted =db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title }','{self. date_posted}')"

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
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About page')
    #  in this case if no methods the form does not submit

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # one time alert use flash
        flash(f'Account created for {form.Username.data}!','success')
        return redirect(url_for('home'))

    return render_template('register.html',title='Register',form=form)
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.Email.data == 'kizdorothy@gmail.com' and form.Password.data =='password':
            flash('You have been logged in','success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful.please try again','danger')
        return render_template('login.html',title='login',form=form)



if __name__ == '__main__':
    app.run(debug=True)