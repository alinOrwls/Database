from flask import Flask, request, render_template , redirect
import psycopg2


app = Flask (__name__)
# app.config.from_object('config')

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

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    return render_template("index.html")

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

    cur = connection.cursor()
    cur.execute("INSERT INTO  public.journal (title, content) VALUES ( %s , %s )", (_title, _content))
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

