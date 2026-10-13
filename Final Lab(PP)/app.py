from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///labdata.db"
app.config["SECRET_KEY"] = "thisisasecretkey"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


class AssignDuty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    duty = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=25)])
    password = PasswordField(validators=[InputRequired(), Length(min=5, max=128)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Username already exists.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=25)])
    password = PasswordField(validators=[InputRequired(), Length(min=5, max=128)])
    submit = SubmitField("Login")




@app.route("/")
@login_required
def home():
    return render_template("index.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for("login"))

        except IntegrityError:
            db.session.rollback()
            flash("Username already exists.", "danger")

    return render_template("register.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    if request.method == "POST":
        name = request.form["name"]
        duty = request.form["duty"]

        new_task = AssignDuty(name=name, duty=duty)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("todo"))
        except:
            return "There was an issue adding your task"

    tasks = AssignDuty.query.order_by(AssignDuty.created).all()
    return render_template("todo.html", tasks=tasks)



@app.route("/delete/<int:id>")
@login_required
def delete(id):
    task_to_delete = AssignDuty.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for("todo"))
    except:
        return "There was a problem deleting that task"


# --- EDIT TASK ---
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    task_to_edit = AssignDuty.query.get_or_404(id)

    if request.method == "POST":
        task_to_edit.name = request.form["name"]
        task_to_edit.duty = request.form["duty"]

        try:
            db.session.commit()
            return redirect(url_for("todo"))
        
        except:
            return "There was an issue updating the task"

    return render_template("edit.html", task=task_to_edit)



with app.app_context():
        db.create_all()

app.run(debug=True)