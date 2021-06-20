from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
from datetime import datetime
import math
import os





app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/GameAndPcReview'
app.config['UPLOAD_FOLDER']='/home/zeus//Desktop/GAME AND PC REVIEW PROJECT/static/img'
app.secret_key="xyz"
db = SQLAlchemy(app)







"""""""""""""""""""""""""""""""""""""""""Class Models"""""""""""""""""""""""""""""""""""""""
class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    tagline = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    firstImage = db.Column(db.String(80), nullable=False)
    firstContent = db.Column(db.String(80), nullable=False)
    secondImage = db.Column(db.String(80), nullable=False)
    secondHeading = db.Column(db.String(80), nullable=False)
    secondContent = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    writer = db.Column(db.String(80), nullable=True, default=" ")
    active = db.Column(db.String(80), nullable=False)


class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(80), nullable=True)

class Comment(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    comment = db.Column(db.String(80), nullable=False)
    postTagline = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)













"""""""""""""""""""""""""""""""""""Autintication"""""""""""""""""""""""""""

@app.route("/userSignup", methods=["GET","POST"])
def userSignup():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        if len(name)<2:
            return '<script>alert("name must be greater than 2 character")</script>'
        elif len(email)<4:
            return '<script>alert("email must be greater than 4 character")</script>'
        elif len(password)<7:
            return '<script>alert("password must be greater than 7 character")</script>'
        else:
            entry=Users(name=name,email=email,password=password,date=datetime.now())
            db.session.add(entry)
            db.session.commit()
            return redirect("/userLogin")

    return render_template("userSignup.html")



@app.route("/userLogin", methods=["GET","POST"])
def userLogin():
    if request.method=="POST":
        email=request.form.get("email")
        session["user"]=email
        password=request.form.get("password")
        users=Users.query.filter_by(email=email).first()
        if users is not None:
            return redirect("/profile")
        else:
            return '<script>alert("Wrong email or password")</script>'

    return render_template("userLogin.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")




"""Admin Login"""
@app.route("/adminLogin", methods=["GET","POST"])
def adminLogin():
    if request.method=="POST":
        id=request.form.get("id")
        session["admin"]=id
        password=request.form.get("password")

        if id =="mohi12345" and password=="12345678":
            return redirect("/dashboard")


    return render_template("adminLogin.html")

@app.route("/adminLogout")
def adminLogout():
    session.pop("admin", None)
    return redirect("/")
    














"""""""""""""""""""""profile"""""""""""""""""""""""



"""profile"""
@app.route("/profile")
def profile():
    if "user" in session:
        users=Users.query.filter_by(email=session["user"]).first()
        return render_template("profile.html",users=users)
    else:
        return redirect("/userLogin")




"""user Review"""
@app.route("/userReview",methods=["GET","POST"])
def userReview():
    if "user" in session:
        users=Users.query.filter_by(email=session["user"]).first()
    if request.method=="POST":
        tagline=request.form.get("tagline")
        category=request.form.get("category")
        firstImage = request.files['firstImage']
        firstContent=request.form.get("firstContent")
        secondHeading=request.form.get("secondHeading")
        secondImage = request.files['secondImage']
        secondContent=request.form.get("secondContent")
        firstImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(firstImage.filename)))
        secondImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(secondImage.filename)))
        entry=Posts(tagline=tagline,category=category,firstImage=firstImage.filename,secondImage=secondImage.filename,secondContent=secondContent,firstContent=firstContent,secondHeading=secondHeading,date=datetime.now(),writer=users.name,active=0)
        db.session.add(entry)
        db.session.commit()
        return redirect("/userPost")

    return render_template("userReview.html")



@app.route("/editProfile",methods=["GET","POST"])
def editProfile():
    if "user" in session:
        users=Users.query.filter_by(email=session["user"]).first()
        if request.method=="POST":
            image = request.files['image']
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
            users.image=image.filename
            db.session.commit()
            return redirect("/profile")

    return render_template("editProfile.html",users=users)
    

@app.route("/timeline")
def timeline():
    posts=Posts.query.all()
    if "user" in session:
        user=Users.query.filter_by(email=session["user"]).first()
        user_name=user.name
        posts=Posts.query.filter_by(writer=user_name).all()
    return render_template("timeline.html",posts=posts)


@app.route("/editUserPost/<string:sno>",methods=["GET","POST"])
def editUserPost(sno):
    post=Posts.query.filter_by(sno=sno).first()
    if request.method=="POST":
        tagline=request.form.get("tagline")
        category=request.form.get("category")
        firstImage = request.files['firstImage']
        firstContent=request.form.get("firstContent")
        secondHeading=request.form.get("secondHeading")
        secondImage = request.files['secondImage']
        secondContent=request.form.get("secondContent")
        firstImage = request.files['firstImage']
        firstImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(firstImage.filename)))
        secondImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(secondImage.filename)))
        post=Posts.query.filter_by(sno=sno).first()
        post.tagline=tagline
        post.category=category
        post.firstImage=firstImage.filename
        post.firstContent=firstContent
        post.secondHeading=secondHeading
        post.secondImage=secondImage.filename
        post.secondContent=secondContent
        db.session.commit()
        return redirect("/postTable")

    return render_template("editUserPost.html",post=post,sno=sno)

@app.route("/deleteUserPost/<string:sno>")
def deleteUserPost(sno):
    post=Posts.query.filter_by(sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/timeline")

@app.route("/deleteUser/<string:sno>")
def deleteUser(sno):
    user=Users.query.filter_by(sno=sno).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/userTable")




"""""""""""""""""""""""""""""""""""""""""""""""""Tech World"""""""""""""""""""""""""""""""""""""""




"""Home"""


@app.route("/", methods=["POST","GET"])
def index():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(5))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(5):(page-1)*int(5)+ int(5)]
    if page==1:
        prev = "#"
        next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)
    if request.method=="POST":
        search=request.form.get("search")
        posts=Posts.query.filter_by(tagline=search).all()
        return render_template("index.html",posts=posts)

    return render_template("index.html",posts=posts, prev=prev, next=next)



"""Post"""


@app.route("/post/<string:tagline>", methods=["GET","POST"])
def post(tagline):
    post=Posts.query.filter_by(tagline=tagline).first()
    comments=Comment.query.filter_by(postTagline=tagline).all()
    if request.method=="POST":
        comment=request.form.get("comment")
        if "user" in session:
            email=session["user"]
            users=Users.query.filter_by(email=email).first()
            entry=Comment(name=users.name,email=users.email,comment=comment,date=datetime.now(),postTagline=post.tagline)
            db.session.add(entry)
            db.session.commit()
            comments=Comment.query.filter_by(postTagline=post.tagline).all()
            return render_template("post.html",comments=comments,post=post)
        else:
            return redirect("/userLogin")

    return render_template("post.html",post=post,comments=comments)




"""Game Review"""

@app.route("/gameReview",methods=["GET","POST"])
def gameReview():
    posts = Posts.query.filter_by().all()
    if request.method=="POST":
        search=request.form.get("search")
        posts=Posts.query.filter_by(tagline=search).all()
        return render_template("gameReview.html",posts=posts)       
    return render_template("gameReview.html",posts=posts)


"""pc Review"""

@app.route("/pcReview", methods=["GET","POST"])
def pcReview():
    posts = Posts.query.filter_by().all()
    if request.method=="POST":
        search=request.form.get("search")
        posts=Posts.query.filter_by(tagline=search).all()
        return render_template("pcReview.html",posts=posts)

    return render_template("pcReview.html",posts=posts)

"""User Review"""

@app.route("/userPost",methods=["GET","POST"])
def userPost():
    if request.method=="POST":
        search=request.form.get("search")
        posts=Posts.query.filter_by(tagline=search).all()
        return render_template("userPost.html",posts=posts)
    posts=Posts.query.filter_by().all()
    return render_template("userPost.html",posts=posts)



""";""""""""""""""""""""""""""""""""""""""Dashboard"""


@app.route("/dashboard")
def dashboard():
    if "admin" in session:
        print(session["admin"])
        users=Users.query.filter_by().all()    
        return render_template("dashboard.html",users=users)



"""""UserTable"""
@app.route("/userTable")
def userTable():
    if "admin" in session:
        users=Users.query.filter_by().all()
        return render_template("userTable.html",users=users)



"""Post Table"""
@app.route("/postTable")
def postTable():
    if "admin" in session:
        posts=Posts.query.filter_by().all()
        return render_template("postTable.html",posts=posts)



"""Tables"""
@app.route("/tables")
def tables():
    if "admin" in session:
        users=Users.query.filter_by().all()
        posts=Posts.query.filter_by().all()
        return render_template("tables.html",users=users,posts=posts)



"""""AddPostByAdmin"""
@app.route("/addPost",methods=["GET","POST"])
def addPost():
    if request.method=="POST":
        tagline=request.form.get("tagline")
        category=request.form.get("category")
        firstImage = request.files['firstImage']
        firstContent=request.form.get("firstContent")
        secondHeading=request.form.get("secondHeading")
        secondImage = request.files['secondImage']
        secondContent=request.form.get("secondContent")
        
        firstImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(firstImage.filename)))
        secondImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(secondImage.filename)))
        entry=Posts(tagline=tagline,category=category,firstImage=firstImage.filename,secondImage=secondImage.filename,secondContent=secondContent,firstContent=firstContent,secondHeading=secondHeading,date=datetime.now(),active=1,writer="Admin")
        db.session.add(entry)
        db.session.commit()
        return redirect("/postTable")

    return render_template("addPost.html")


@app.route("/editPost/<string:sno>",methods=["GET","POST"])
def editPost(sno):
    post=Posts.query.filter_by(sno=sno).first()
    if request.method=="POST":
        tagline=request.form.get("tagline")
        category=request.form.get("category")
        firstImage = request.files['firstImage']
        firstContent=request.form.get("firstContent")
        secondHeading=request.form.get("secondHeading")
        secondImage = request.files['secondImage']
        secondContent=request.form.get("secondContent")
        firstImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(firstImage.filename)))
        secondImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(secondImage.filename)))

        post=Posts.query.filter_by(sno=sno).first()
        post.tagline=tagline
        post.category=category
        post.firstImage=firstImage.filename
        post.firstContent=firstContent
        post.secondHeading=secondHeading
        post.secondImage=secondImage.filename
        post.secondContent=secondContent
        db.session.commit()
        return redirect("/postTable")

    return render_template("editPost.html",post=post,sno=sno)

@app.route("/deletePost/<string:sno>")
def deletePost(sno):
    if "admin" in session:
        post=Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect("/postTable")


app.run(debug=True)