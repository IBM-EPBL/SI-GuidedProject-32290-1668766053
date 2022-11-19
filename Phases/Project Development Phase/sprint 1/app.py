from flask import Flask,render_template,request,url_for,redirect,flash,session
import hashlib

import requests

app=Flask(__name__)
app.secret_key = "abc"  


@app.route("/")
def index():
    return  render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")
    

@app.route("/register",methods=['GET','POST'])
def register():
    error = None
    if request.method=='POST':
        username= request.form['username']
        email=request.form['email']
        password=request.form['password']
        cpass=request.form['cpassword']
        if password != cpass:
            error = "Password and Confirm password should be same!!"
        else:
            hashed_password=hashlib.sha256(password.encode()).hexdigest()

            
            sql="SELECT * FROM newstracker WHERE username=?"
            stat =ibm_db.prepare(connection,sql)
            ibm_db.bind_param(stat,1,username)
            ibm_db.execute(stat)
            res=ibm_db.fetch_assoc(stat)

            if res:
                error="Username is already exits user different username"
                
            else:
                sql1="INSERT INTO newstracker VALUES (?,?,?)"
                pre_stat =ibm_db.prepare(connection,sql1)
                ibm_db.bind_param(pre_stat,1,username)
                ibm_db.bind_param(pre_stat,2,email)
                ibm_db.bind_param(pre_stat,3,hashed_password)
                ibm_db.execute(pre_stat)

                flash('Account created successfully')
                return redirect(url_for('index'))
    return render_template('signup.html', error = error)


@app.route('/login',methods=["GET","POST"])
def login():
    error = None
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        hashed=hashlib.sha256(password.encode()).hexdigest()
        
        sql="SELECT * FROM newstracker WHERE username=?"
        con =ibm_db.prepare(connection,sql)
        ibm_db.bind_param(con,1,username)
        ibm_db.execute(con)
        res=ibm_db.fetch_assoc(con)
        if res:
            if hashed == res['PASSWORD']:
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            else:
                error = "Login Failed!!"
                return render_template('index.html',error=error)
        else:
            error = "Login Failed!!"
            return render_template('index.html',error=error)

 
 
         
@app.route('/home')
def home():
    error=None
    if 'username' in session:
        username = session['username']
        main_url="https://newsapi.org/v2/top-headlines?country=in&apiKey="+news_api_key
        news=requests.get(main_url).json()
        articles=news["articles"]
        news_articles_title=[]
        for a in articles:
            news_articles_title.append(a["title"])

        news_articles_description=[]
        for a in articles:
            news_articles_description.append(a["description"])

        news_articles_url=[]
        for a in articles:
            news_articles_url.append(a["url"])

        news_articles_urlToImage=[]
        for a in articles:
            news_articles_urlToImage.append(a["urlToImage"])

        news_articles_publishedAt=[]
        for a in articles:
            news_articles_publishedAt.append(a["publishedAt"])

        news_articles_content=[]
        for a in articles:
            news_articles_content.append(a["content"])


        return render_template("home.html",user=username,articles=articles)
    else:
        error="Pleasr Login to access"
        return render_template('index.html',error=error)
          


@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))


if __name__=="__main__":
    app.run(debug=True)
    