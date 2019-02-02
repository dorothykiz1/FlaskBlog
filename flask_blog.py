from flask import Flask,render_template
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] ='79d64c304c964d793be61e7fc7696a9b'
# secret key for this app

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

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html',title='Register',form=form)
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html',title='Login',form=form)

if __name__ == '__main__':
    app.run(debug=True)