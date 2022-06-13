from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
db = SQLAlchemy(app)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    genre = db.Column(db.String(40), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(200), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    title = db.Column(db.String(100))
    text = db.Column(db.String(1000))


db.create_all()

movies = Movies.query.all()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
def home():
    return render_template('home.html', movies=movies, user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                flash("გამარჯობა! :) დღეს რას უყურებთ?", category="success")
                login_user(user, remember=True)
                return redirect("/")
            else:
                flash("პაროლი არასწორია", category="error")
        else:
            flash("მეილი არასწორია", category="error")
    return render_template('login.html', user=current_user)


@app.route("/logout")
@login_required
def logout():
    flash("თქვენ გახვედით პროფილიდან", category="success")
    logout_user()
    return redirect("login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("იმეილი უკვე გამოყენებულია", category="error")
        elif len(username) < 3:
            flash("მომხმარებლის სახელი უნდა შეიცავდეს მინიმუმ 3 სიმბოლოს", category="error")
        elif "@" not in email:
            flash("მეილში უნდა იყოს გამოყენებული @ სიმბოლო", category="error")
        elif password1 != password2:
            flash("პაროლები არ ემთხვევა ერთმანეთს", category="error")
        elif len(password1) < 8:
            flash("პაროლი უნდა შეიცავდეს მინიმუმ 8 სიმბოლოს", category="error")
        else:
            flash("თქვენ წარმატებით დარეგისტრირდით! :)", category="success")
            new_user = User(username=username, email=email, password=password1)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
    return render_template('signup.html', user=current_user)


@app.route("/<title>", methods=["GET", "POST"])
def video(title):
    if request.method == "POST":
        text = request.form.get("comment")
        if len(text) < 1:
            flash("თქვენი კომენტარი არ შეიცავს სიმბოლოებს", category="error")
        else:
            new_comment = Comment(username=current_user.username, title=title, text=text)
            db.session.add(new_comment)
            db.session.commit()
    comment = Comment.query.filter_by(title=title).all()
    single_url = Movies.query.filter_by(title=title).first()
    return render_template("title.html", user=current_user, comment=comment, url=single_url.url)


if __name__ == "__main__":
    app.run(debug=True)