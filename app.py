import sqlite3
from werkzeug.utils import redirect
from flask import Flask,render_template,request,session
from flask_session import Session

app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
connection=sqlite3.connect("anime_sekai.db",check_same_thread=False)
connection.execute('''CREATE TABLE IF NOT EXISTS ANIME_INFO(ANIME_ID INTEGER PRIMARY KEY AUTOINCREMENT,
ANIME_NAME VARCHAR(20),
PLOT VARCHAR,
RELEASE_DATE DATE,
RATING INTEGER, 
IMAGE VARCHAR(200),
LINK VARCHAR(200),
AUTHOR VARCHAR(20),NO_OF_EPISODES INTEGER);''')

connection.execute('''CREATE TABLE IF NOT EXISTS ANIME_GENRE(GENRE VARCHAR(15),ANIME_ID INTEGER,
FOREIGN KEY (ANIME_ID) REFERENCES ANIME_INFO(ANIME_ID));''')

@app.route("/")
def app_start():
    session["id"]=""
    return render_template("index.html")

@app.route("/homepage")
def homepage():
    message='none'
    a=connection.execute(f"SELECT ANIME_ID,ANIME_NAME,IMAGE,RATING FROM ANIME_INFO ORDER BY RATING DESC LIMIT 5;").fetchall()
    b=connection.execute(f"SELECT ANIME_ID,ANIME_NAME,IMAGE,RELEASE_DATE FROM ANIME_INFO ORDER BY RELEASE_DATE DESC LIMIT 5;").fetchall()
    print(a)
    if session["id"]=="admin":
        message='block'
    return render_template("homepage.html",message=message,result_1=a,result_2=b)
    

@app.route("/admin-login",methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        get_username=request.form['username']
        get_password=request.form['password']
        if get_username=="admin" and get_password=="123hello":
            session["id"]="admin"
            return redirect("/homepage")
    return render_template("admin_login.html")

@app.route("/anime-info",methods=['GET','POST'])
def anime_info():
    if session["id"]=="admin":
        message="none" 
        if request.method=='POST':
            get_Anime_name=request.form['anime_name']
            get_Plot=request.form['plot']
            get_Release_Date=request.form['release_date']
            get_Rating=request.form['rating']
            get_Link=request.form['link']
            get_Image=request.form['image']
            get_Author=request.form['author']
            get_No_of_episodes=request.form['episodes']
            print(get_No_of_episodes)
            connection.execute(f"INSERT INTO ANIME_INFO(ANIME_NAME,PLOT,RELEASE_DATE,RATING,IMAGE,LINK,AUTHOR,NO_OF_EPISODES) VALUES ('{get_Anime_name}','{get_Plot}','{get_Release_Date}','{get_Rating}','{get_Image}','{get_Link}','{get_Author}','{get_No_of_episodes}' );")
            connection.commit()
            x=connection.execute(f"SELECT * FROM ANIME_INFO;").fetchall()
            print(x)
            message="block"

        return render_template("anime_info.html",message=message)
    return redirect("/")
    

@app.route("/view-details/<anime_id>",methods=['GET','POST'])
def view_details(anime_id):
    message='none'
    if request.method=='POST':
        get_genre=request.form['Genre']
        connection.execute(f"INSERT INTO ANIME_GENRE(GENRE,ANIME_ID) VALUES('{get_genre}','{anime_id}');")
        connection.commit()
    z=connection.execute(f"SELECT * FROM ANIME_INFO WHERE ANIME_ID='{anime_id}';").fetchall()
    print(z)
    y=connection.execute(f"SELECT GENRE FROM ANIME_GENRE WHERE ANIME_ID='{anime_id}';").fetchall()
    print(y)
    if session["id"]=='admin':
        message='block'
    return render_template("anime_detail.html",result=z[0],genre=y,message=message)


@app.route("/view-anime-info")
def view_anime_info():
    if session["id"]=='admin':
        x=connection.execute("SELECT ANIME_ID,ANIME_NAME,RELEASE_DATE,AUTHOR FROM ANIME_INFO;").fetchall()
        return render_template("view_anime_info.html",result=x)
    return redirect("/")

@app.route("/get/<get_genre>")
def get_anime(get_genre):
    message='none'
    if session["id"]=="admin":
        message='block'
    t=connection.execute(f"SELECT ANIME_INFO.ANIME_ID,ANIME_INFO.ANIME_NAME,ANIME_INFO.IMAGE FROM ANIME_INFO JOIN ANIME_GENRE ON ANIME_GENRE.ANIME_ID=ANIME_INFO.ANIME_ID WHERE ANIME_GENRE.GENRE='{get_genre}'; ").fetchall()

    return render_template("get_anime.html",message=message,result=t)



if __name__=="__main__":
    app.run(debug=True)