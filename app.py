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
    return render_template('index.html')

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
    return render_template("create.html")

@app.route('/create/post', methods=["POST"])
def create_post():
    _title=request.form['title' ]
    _content=request.form['content']

    cur = connection.cursor()
    cur.execute("INSERT INTO  public.journal (title, content) VALUES ( ' %s ', ' %s ')", (_title, _content))
    connection.commit()
    connection.close()
    
  

    print(_title)
    print(_content)
    return redirect("/create")


@app.route('/delete')
def delete():
    return render_template("create.html")




if  __name__ =='__main__':
    app.run(debug=True)

