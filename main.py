from flask import Flask, render_template, request, redirect, make_response, send_file
from jwt import generate_jwt, validate_jwt, get_user_info
import db
import requests
from PIL import Image
from io import BytesIO

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


@app.route("/strict_static/<file_name>", endpoint='strict_static')
@restricted
def strict_static(file_name, *args, **kwargs):
    return send_file(f'./strict_static/{file_name}')


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


@app.route("/editproperty/<property_name>", methods=['GET', 'POST'], endpoint='editproperty')
@restricted
def editproperty(property_name, *args, **kwargs):

    if request.method == 'POST':
        print(request.form)
        f = request.files['file']
        f.save('./static/'+f.filename)
        db.update_or_add_properties(request.form, '/static/'+f.filename)
        return redirect("/")
    if property_name != "new":
        return render_template("editproperty.html", property=db.get_property_details(property_name), categories=db.categories, title='Edit Property')
    return render_template("editproperty.html", property=None, categories=db.categories,  title='Edit Property')


@app.route("/editvendor/<vendor_name>", methods=['GET', 'POST'], endpoint='editvendor')
@restricted
def editvendor(vendor_name, *args, **kwargs):

    if request.method == 'POST':
        f = request.files['file']
        f.save('./static/'+f.filename)
        app.logger.info(f.filename)
        db.update_or_add_vendors(request.form)
        return redirect("/")
    if vendor_name != "new":
        return render_template("editvendor.html", vendor=None)
    return render_template("editvendor.html", vendor=db.get_vendor_details(vendor_name),  title='Edit Property')


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
            return render_template("login.html", title='Login', remove_logout_icon=True, warning='Wrong Username or password')
    return render_template("login.html", title='Login', remove_logout_icon=True)

@app.route("/news", methods=['GET'], endpoint='news')
@restricted
def news(*args, **kwargs):
    # Defining the NewsAPI endpoint and parameters
    url = 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': '54bcf4603bce4e6dacf91bbc1fe2fb83',
        'q': 'real estate india OR property india OR real estate investment india OR rent india OR property tax india',
        'sortBy': 'relevancy',
        'language': 'en',
        'pageSize': 10
    }

    # Send a request to the NewsAPI endpoint and retrieve the JSON response
    response = requests.get(url, params=params)
    json_data = response.json()

    # Extract the articles from the JSON response
    articles = json_data['articles']
    news_data = []

    # Loop through the articles and retrieve the image associated with each article
    for article in articles:
        title = article['title']
        description = article['description']
        url = article['url']
        image_url = article['urlToImage']
        image_data = None

        if image_url is not None:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((10, 10))
            buffer = BytesIO()
            image_data = buffer.getvalue()

        # Add the article information and image data to the news_data list
        news_data.append({
            'title': title,
            'description': description,
            'url': url,
            'image': image_data
        })

    return render_template('news.html', news=news_data)


if __name__ == "__main__":
    with app.app_context():
        db.db.create_all()
        db.initalize()
    app.run(host="0.0.0.0", debug=False)
