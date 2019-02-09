import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for,request,abort
from Flaskblog.forms import RegistrationForm, LoginForm,UpdateAccountForm,PostForm
from Flaskblog import app,db,bcrypt
from Flaskblog.models import User , Post
from flask_login import login_user,current_user,logout_user,login_required


# posts =[
#     {
#         'author':' Dorothy Kabarozi',
#         'title':'Dealing with coding and backache',
#         'content':'You can  never code while sleeping probably you will hurt yo back but sitting for long hours is also not that easy',
#         'date_posted':'Jan 28th,2019'
#     },
#     {
#         'author':' Dorothy Kabarozi',
#         'title':'Moms can code too',
#         'content':""" Distractions from our little ones,their cries their smiles always let us
#                      leave what we are doing and attend to them.Being a coding mom is equally
#                       not easy but it is doable """,
#         'date_posted':'Jan 30th,2019'
#     }
# ]
 
@app.route('/')
@app.route('/home')
def home():
    # posts = Post.query.all() 
    page =request.args.get('page',1,type=int)
    # pagination
    posts = Post.query.order_by(Post.date_posted.desc()).paginate( page=page,per_page=5) 
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
            return render_template('login.html', title='login', form = form)

    return render_template('login.html', title='login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# function for saving uploaded picture to our file system
    # using random hex module  that takes in 8 bytes to avoid collusion with files already in the system
    # Os gets the path for the file

def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)
    # _ means an omitted/used variable,os.path.splitext returns the fname and fext but we dont use fname so use _
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',  picture_fn)
    # os.path.join helps concatenate the application path to the directory of the picture 
    
    # resizing Images
    output_size =(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    # form_picture.save(picture_path)
    return picture_fn

@app.route('/account',methods=["GET","POST"]) 
@login_required
def account():
    form = UpdateAccountForm()
    # form validation 

    if form.validate_on_submit():
        # setting a users profile picture
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success') 
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename ='profile_pics/'+ current_user.image_file)
    return render_template('account.html',
                             title='Account',image_file = image_file,form = form)


@app.route('/post/new',methods=["GET","POST"]) 
@login_required
def new_post():

    form = PostForm()
    if form.validate_on_submit():
        # adding post to the database
        # backref=using current_user
        post = Post(title = form.title.data, content = form.content.data, author =current_user) 
        db.session.add(post)
        db.session.commit()

        flash('Your Post has been created!', 'success')
        return redirect(url_for('home')) 
    return render_template('create_post.html', title = 'New Post',
                            form = form , legend ='New Post')
 
# get asingle post
@app.route('/post/<int:post_id>')
def post(post_id):
    post =Post.query.get_or_404(post_id)
    #  method that gets the id or return the error 404
    return render_template('post.html',title=post.title,post=post)
      
# update a post
@app.route('/post/<int:post_id>/update',methods=["GET","POST"])
@login_required
def update(post_id):
    post =Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        # response for a forbidden route
        
    form =PostForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.content =form.content.data 
        # we do not do the session.add because they are already in the database 
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post_id))
    elif request.method == 'GET':
        # form will be populated with the current post details
        form.title.data =post.title
        form.content.data =post.content

    return render_template('create_post.html', title = 'New Post',
                            form = form , legend ='Update Post')


 #delete post
@app.route('/post/<int:post_id>/delete',methods=["POST"])
@login_required
def delete_post(post_id):
    post =Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash ('Your post has been deleted!','success')
    return redirect(url_for('home'))

# get users post
@app.route('/user/<string:username>')
def user_posts(username):

    # posts = Post.query.all() 
    page =request.args.get('page',1,type=int)
    # get a first user or return a 404
    user =User.query.filter_by(username=username).first_or_404() 
    # pagination
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate( page=page,per_page=5) 
    return render_template('user_post.html',posts=posts,user=user)

       