from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database
from database_file import Db
import json
from aws import AWS
app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open("data.json", 'r') as json_file:
    users = json.load(json_file)
db=Database(users['user'],users['password'])
aws=AWS()
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in db.select_users() and db.get_password(email) == password:
            return render_template('search.html')
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['name']
        number=request.form['mobile']
        email=request.form['email']
        password = request.form['password']
        if email in db.select_users():
            flash('Username already exists')
        else:
            db.insert_table(username,number,email,password)
            flash('User created successfully!')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        print('a')
        search_query = request.form['query']  # Assuming the search query is sent as 'query' parameter
        if search_query:
            database = Db("saikumar-007","Saikumar20@")
            if database.initialized:
                database.create_table()
                database.insert_table()
            else:
                print('a')
                return render_template('search.html')
            print(search_query)
            search_results=database.search(search_query)
            x=search_results.split('.')
            # Render a template with the search results
            return render_template('search_results.html', results=aws.return_content(search_results))
        else:
            flash('Please enter a search query.')
            return redirect(url_for('search'))


@app.route('/home')
def home():
    query = request.args.get('query', '')
    # Here you can implement the logic to perform the search
    return render_template('home.html', query=query)

if __name__ == '__main__':
    app.run(debug=True)
