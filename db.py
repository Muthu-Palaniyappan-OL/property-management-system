from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import LargeBinary, ARRAY
from flask_sqlalchemy import SQLAlchemy
import base64
import spacy
import pandas as pd
from word2number import w2n
import joblib

nlp = spacy.load('en_core_web_md')
model = joblib.load('elastic_net.joblib')

df = pd.read_csv('rent_data.csv')
localities = df['locality'].unique()
cities = df['city'].unique()

db = SQLAlchemy()
categories = ["bunglow", "society", "under-construction",
              "induvijual-house", "appartment/flats", "office-complex"]


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    level: Mapped[int] = mapped_column(nullable=False)  # 1 (ADMIN), 2 (READ)

    def __repr__(self) -> str:
        return f"user(id={self.id},username={self.username},password={self.password})"


class Property(db.Model):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    category: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    no_of_units: Mapped[int] = mapped_column(nullable=True)
    list_of_units: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    pancard: Mapped[str] = mapped_column(nullable=True)
    discription: Mapped[str] = mapped_column(nullable=True)
    finance: Mapped[str] = mapped_column(nullable=True)
    locality: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    area: Mapped[str] = mapped_column(nullable=True)
    bathroom: Mapped[str] = mapped_column(nullable=True)
    bedroom: Mapped[str] = mapped_column(nullable=True)
    predicted_rent: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"property(id={self.id},property_name={self.property_name},discription={self.discription})"


class Vendor(db.Model):
    __tablename__ = "vendors"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_name: Mapped[str] = mapped_column(nullable=False)
    vendor_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)
    name_contact_person: Mapped[str] = mapped_column(nullable=True)
    phone_number_of_contact: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"vendor(property_name={self.property_name},vendor_name={self.vendor_name},email={self.email})"


class Tenants(db.Model):
    __tablename__ = "tenants"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_name: Mapped[str] = mapped_column(nullable=False)
    tenant_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)
    name_contact_person: Mapped[str] = mapped_column(nullable=True)
    phone_number_of_contact: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"tenant(property_name={self.property_name},vendor_name={self.vendor_name},email={self.email})"


def initalize() -> None:
    db.session.add(User(username='admin', password='admin', level=1))
    db.session.add(User(username='muthu', password='muthu', level=2))
    # db.session.add(Property(property_name='Flat1',
    #                         url='https://assets-news.housing.com/news/wp-content/uploads/2022/03/28143140/Difference-between-flat-and-apartment.jpg', location='Chennai', no_of_units=5, list_of_units='10-20', address='No.19khjdfhj'))
    db.session.commit()


def validate_username_password(username, password):
    results = db.session.query(User).filter(User.username == username)
    if results.count() != 1:
        return False
    if results[0].password == password:
        return True
    else:
        return False


def get_property_details(property_name):
    return list(db.session.query(Property).filter(Property.property_name == property_name))[0]


def update_or_add_users(username, password, level):
    results = db.session.query(User).filter(User.username == username)
    if results.first() is not None:
        results[0].password = password
    else:
        db.session.add(User(username=username, password=password, level=level))
    db.session.commit()


def update_or_add_properties(req):
    results = db.session.query(Property).filter(
        Property.property_name == req.form['property_name'])

    user = None
    if results.first() is not None:
        user = results[0]
    else:
        user = Property()

    for key in req.form:
        if req.form[key] != '':
            setattr(user, key, req.form[key])
    
    for key in req.files:
        if req.files[key].filename:
            setattr(user, key, base64.b64encode(req.files[key].read()).decode('UTF-8'))
    

    print(user)

    if (user.discription != None or user.discription == ''):
        data = analyse(user.discription)
        if (data['locality'] != '')[0]:
            user.locality = data['locality'][0]
        if (data['city'] != '')[0]:
            user.city = data['city'][0]
        if (data['area'] != 0)[0]:
            user.area = data['area'][0]
        if (data['bedroom'] != 0)[0]:
            user.bedroom = data['bedroom'][0]
        if (data['bathroom'] != 0)[0]:
            user.bathroom = data['bathroom'][0]
        print(data)
        user.predicted_rent = int(model.predict(data)[0])
        

    db.session.add(user)

    db.session.commit()

def update_finance(property_name, data):
    results = db.session.query(Property).filter(
        Property.property_name == property_name)
    property = results[0]
    setattr(property, 'finance', data.decode('UTF-8'))
    db.session.add(property)
    db.session.commit()

def update_or_add_vendors(property_name, form_data: dict):
    results = db.session.query(Vendor).filter(
        Vendor.vendor_name == form_data['vendor_name'] and Vendor.property_name == property_name)


    vendor = None
    if results.first() is not None:
        vendor = results[0]
    else:
        vendor = Vendor()

    for key in form_data:
        setattr(vendor, key, form_data[key])

    db.session.add(vendor)
    db.session.commit()


def update_or_add_tenants(property_name, form_data: dict):
    results = db.session.query(Tenants).filter(
        Tenants.tenant_name == form_data['tenant_name'] and Tenants.property_name == property_name)

    tenants = None
    if results.first() is not None:
        tenants = results[0]
    else:
        tenants = Tenants()

    for key in form_data:
        setattr(tenants, key, form_data[key])

    db.session.add(tenants)
    db.session.commit()


def get_properties_list():
    return list(db.session.query(Property).all())


def get_vendor_list():
    return list(db.session.query(Vendor).all())


def get_users_list():
    return list(db.session.query(User).all())


def get_users_details(username):
    return db.session.query(User).filter(User.username == username)[0]


def get_vendor_list_details(property_name):
    return list(db.session.query(Vendor).filter(Vendor.property_name == property_name))


def get_vendor_details(property_name, tenant_name):
    return db.session.query(Vendor).filter(Vendor.property_name == property_name and Tenants.tenant_name == tenant_name)[0]


def get_tenants_list_details(property_name):
    return list(db.session.query(Tenants).filter(Tenants.property_name == property_name))


def get_tenant_details(property_name, tenant_name):
    return db.session.query(Tenants).filter(Tenants.property_name == property_name and Tenants.tenant_name == tenant_name)[0]


def delete_user(username):
    results = db.session.query(User).filter(User.username == username)
    if results.first() is not None:
        db.session.delete(results[0])
        db.session.commit()


def delete_vendor(property_name, vendor_name):
    results = db.session.query(Vendor).filter(
        Vendor.property_name == property_name and Vendor.vendor_name == vendor_name)
    if results.first() is not None:
        db.session.delete(results[0])
        db.session.commit()


def delete_tenant(property_name, tenant_name):
    results = db.session.query(Tenants).filter(
        Tenants.property_name == property_name and Tenants.tenant_name == tenant_name)
    if results.first() is not None:
        db.session.delete(results[0])
        db.session.commit()

def analyse(text):
    seller_type = "OWNER"
    bedroom = 0 
    layout_type = "BHK"
    property_type = "Apartment"
    locality = ""
    area = 0
    furnish_type = "Furnished"
    bathroom = 0
    city = ""
    data = pd.DataFrame({
        'seller_type': [seller_type],
        'bedroom': [bedroom],
        'layout_type': [layout_type],
        'property_type': [property_type],
        'locality': [locality],
        'area': [area],
        'furnish_type': [furnish_type],
        'bathroom': [bathroom],
        'city': [city]
    })

    doc = nlp(text)
    for ent in doc.ents:
        if (ent.label_ == 'QUANTITY'):
            if ent.text.find('sq'):
                data['area'] = w2n.word_to_num(ent.text.split(' ')[0])
            else:
                data['area'] = w2n.word_to_num(ent.text)
            
        if (ent.label_ == 'CARDINAL'):
            next_word = [i for i in ent.root.ancestors][0]
            if (nlp(next_word.lemma_).similarity(nlp('bed bedroom')) > 0.8):
                data['bedroom'] = w2n.word_to_num(ent.text)
            if (nlp(next_word.lemma_).similarity(nlp('bath rest bathroom restroom')) > 0.8):
                data['bathroom'] = w2n.word_to_num(ent.text)
            if (nlp(next_word.lemma_).similarity(nlp('sq ft')) > 0.8):
                data['area'] = w2n.word_to_num(ent.text)
        if (ent.label_ == 'GPE'):
            if (ent.text.lower().title() in cities):
                data['city'] = ent.text.lower().title()
            if (ent.text.lower().title() in localities):
                data['locality'] = ent.text.lower().title()
    return data

if __name__ == "__main__":
    initalize()
    print(get_users_list())
    update_or_add_users("admin", "yahoo")
    print(get_users_list())
