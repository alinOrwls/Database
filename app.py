from flask import Flask, request, render_template , redirect, get_flashed_messages, flash, session, url_for
import psycopg2
import psycopg2.extras



app = Flask (__name__)
app.secret_key = 'developers'


try:
    connection=psycopg2.connect(
        host='localhost',
        database='rest_api',
        user='postgres',
        password='admin'
        
    )
    print("you are connected")
except Exception as ex:
     print(ex)




@app.route('/')
def main():

    cur=connection.cursor()
    cur.execute("SELECT * FROM public.journal")
    entry=cur.fetchall()
    connection.commit()
    print(entry)

    return render_template('index.html', entry=entry)

@app.route("/register", methods=["GET", "POST"])
def register(): 
        if request.method =='POST':
            cur = connection.cursor() 

            name = request.form['name']  
            password = request.form['password']

            sql = "INSERT INTO public.users (name, password )VALUES(%s ,%s)"
            cur.execute(sql, (name, password))
            connection.commit()
            flash('Register succesfully', 'success')
            return redirect('/login')
        else: 
            return render_template("register.html")
        

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
 
            cur = connection.cursor()
            # Execute a SELECT query to retrieve user information
            cur.execute("SELECT id, password FROM users WHERE name = %s", (name,))
            user = cur.fetchone()
            
            if(user and (user[1], password)): # Store user ID in session to indicate user is logged in
                session['user_id'] = user[0]
               
                # Display success message
                flash('Logged in successfully!', 'success')
                # Redirect to home page
                return redirect('/create')
            else:
                # Display error message for invalid credentials
                flash('Invalid username or password', 'error')
                return redirect('/login')
           
        else:
            return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/logoutpage')
def logoutpage():
     return render_template('logout.html')

@app.route('/create')
def create():

    cur=connection.cursor()
    cur.execute("SELECT * FROM public.journal")
    entry=cur.fetchall()
    connection.commit()
    print(entry)

    return render_template("create.html", entry=entry)

@app.route('/create/post', methods=["POST"])
def create_post():
    _title=request.form['title' ]
    _content=request.form['content']
    _user_id =   session['user_id']  
   
    cur = connection.cursor()
    cur.execute("INSERT INTO  public.journal (title, content, user_id) VALUES ( %s , %s, %s )", (_title, _content, _user_id))
    connection.commit()

    print(_title)
    print(_content)
    return redirect("/create")


@app.route('/delete', methods = ['POST'])
def delete():
    _id = request.form[ 'txtID']
    print(_id)

    cur=connection.cursor()
    cur.execute("SELECT * FROM public.journal WHERE id=%s", (_id))
    entry=cur.fetchall()
    connection.commit()
    print(entry)

    cur=connection.cursor()
    cur.execute("DELETE FROM public.journal WHERE id=%s", (_id))
    connection.commit()

    return redirect('/')




if  __name__ =='__main__':
    app.run(debug=True)

