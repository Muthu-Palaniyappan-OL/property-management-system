from flask import Flask, render_template, request, redirect, make_response
from jwt import generate_jwt, validate_jwt, get_user_info
import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
db.db.init_app(app)


def restricted(func):
    def wrapper(*args, **kwargs):
        try:
            if not validate_jwt(request.cookies.get('authorization')):
                return redirect("/login")
        except Exception:
            return redirect("/login")
        kwargs.update(get_user_info(request.cookies.get('authorization')))
        return func(*args, **kwargs)
    return wrapper


@app.route("/", endpoint='dashboard')
@restricted
def dashboard(*args, **kwargs):
    return render_template("dashboard.html", properties_list=db.get_properties_list(), title='Dashboard')


@app.route("/property/<property_name>", endpoint='property')
@restricted
def property(property_name, *args, **kwargs):
    return render_template("property.html", property=db.get_property_details(property_name), title=property_name)


@app.route("/manageusers", methods=['GET', 'POST'], endpoint='manageusers')
@restricted
def property(*args, **kwargs):
    if request.method == "POST":
        db.update_or_add_users(
            request.form['new-username'], request.form['new-password'], request.form['level'])
        return render_template("manageusers.html", users_list=db.get_users_list(), level=kwargs['level'], title='Manage Users')
    return render_template("manageusers.html", users_list=db.get_users_list(), level=kwargs['level'], title='Manage Users')


@app.route("/deleteuser", methods=['GET', 'POST'], endpoint='deleteuser')
@restricted
def deleteuser(*args, **kwargs):
    if request.method == 'POST':
        db.delete_user(request.json['username'])
    return "OK"


@app.route("/newproperty", endpoint='newproperty')
@restricted
def newproperty(*args, **kwargs):
    return render_template("newproperty.html", title='Manage Users')


@app.route("/logout", endpoint='logout')
@restricted
def logout(*args, **kwargs):
    response = make_response(redirect("/"))
    response.set_cookie("authorization", "")
    return response


@app.route("/login", methods=["POST", "GET"], endpoint='login')
def login(*args, **kwargs):
    if request.method == "POST":
        if db.validate_username_password(request.form['username'], request.form['password']):
            response = make_response(redirect("/"))
            user = db.get_users_details(request.form['username'])
            response.set_cookie(
                "authorization", generate_jwt({'username': user.username, 'level': user.level}))
            return response
        else:
            return render_template("login.html", title='Login', remove_logout_icon=True)
    return render_template("login.html", title='Login', remove_logout_icon=True)


if __name__ == "__main__":
    with app.app_context():
        db.db.create_all()
        db.initalize()
    app.run(debug=True)
