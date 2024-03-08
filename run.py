
from flask import Flask, request, render_template  # import flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # creating an instance called app and assign
# a variable to it.
app.config.update(

    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:newpassword@localhost:5433/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)  # creating instance of class


@app.route('/new/')
# homepage/root of any web application
# passed a parameter value here
def query_strings(greeting='hello'):  # put application's code here
    # create a variable
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is : {0} </h1>'.format(query_val)


@app.route('/user')
@app.route('/user/<name>')  # anything withing <> is a variable
# when we use variables in route, we need to pass variables into function definition
def no_query_strings(name='mina'):
    return '<h1> hello there ! {} </h1>'.format(name)


@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string : ' + name + '</h1>'


@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1> here is a number : ' + str(num) + '</h1>'


@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return f'<h1> the sum is = {num1 + num2}</h1>'


@app.route('/product/<float:num1>/<float:num2>')
def product_two_numbers(num1, num2):
    return f'<h1> the product is = {num1 * num2}</h1>'


# USING TEMPLATE
@app.route('/temp')
def using_templates():
    return render_template('hello.html')


# JINJA TEMPLATES
@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe',
                  'neon demon',
                  'kong:skull island',
                  'john wick 2',
                  'spiderman - homecoming']
    return render_template('movies.html',
                           movies=movie_list,
                           name='Harry')


@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'kong:skull island': 1.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}
    return render_template('table_data.html',
                           movies=movies_dict,
                           name='Sally')


@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'kong:skull island': 1.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}
    return render_template('filter_data.html',
                           movies=movies_dict,
                           name=None,
                           film='a christmas carol')


@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'kong:skull island': 1.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}
    return render_template('using_macros.html', movies=movies_dict)


class Publication(db.Model):
    __tablename__ = 'publication'

    # ORM converts class definitions to SQL statements
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, id, name):
        self.name = name

    def __repr__(self):
        return 'Name is {}'.format( self.name)

class Book(db.Model):
    __tablename__ = 'book'


    id = db.Column(db.Integer, primary_key=True)  # need primary key in every table
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date =db.Column(db.DateTime, default=datetime.utcnow())

    # relationship
    pub_id =db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, format,image, num_pages, pub_id ):
        #skip book id and pub key
        #pub_key and book id populatd automatically



        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format= format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)


pub = Publication(100, "Oxford Publications ")
paramount = Publication(102, "Paramount Press")
oracle = Publication(103, "Oracle Inc")

b1 = Book("Mikys Delivery Service","William Dobelli", 3.9, "ePub", "broom-145379.svg", 123, 100 )
b2 = Book("The Secret Life of Walter Kitty", "Kitty Stiller", 4.1, "Hardcover", "cat-150306.svg", 133, 100)




# we intend to run the code directly.
if __name__ == '__main__':  # how we intend to run this program
    with app.app_context():
        db.create_all()
        db.session.add_all([b1, b2])
        db.session.commit()

    app.run(debug=True)

