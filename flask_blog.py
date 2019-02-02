from flask import Flask,render_template,flash,redirect,url_for
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] ='79d64c304c964d793be61e7fc7696a9b'
# secret key for this app
# config values in our application app.config

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
            flash(f'You have been logged in','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful.please try again','danger')
        return render_template('login.html',title='login',form='form')

            


    return render_template('login.html',title='Login',form=form)

if __name__ == '__main__':
    app.run(debug=True)