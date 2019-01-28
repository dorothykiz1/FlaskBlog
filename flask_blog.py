from flask import Flask,render_template
app = Flask(__name__)

posts =[
    {
        'author':' Dorothy Kabarozi',
        'title':'Dealing with coding and backache',
        'content':'first post content',
        'date_posted':'Jan 28th,2019'
    },
    {
        'author':' Dorothy Kabarozi',
        'title':'Moms can code too',
        'content':'second post content',
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

if __name__ == '__main__':
    app.run(debug=True)