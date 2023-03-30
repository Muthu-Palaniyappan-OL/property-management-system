from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, select
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, Session, scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy

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
    url: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    no_of_units: Mapped[int] = mapped_column(nullable=True)
    list_of_units: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"property(id={self.id},property_name={self.property_name},url={self.url})"


class Vendor(db.Model):
    __tablename__ = "vendors"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    address: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)
    name_contact_person: Mapped[str] = mapped_column(nullable=True)
    phone_number_of_contact: Mapped[str] = mapped_column(nullable=True)
    vendor_type: Mapped[str] = mapped_column(nullable=True)
    name_of_director: Mapped[str] = mapped_column(nullable=True)
    pan_no: Mapped[str] = mapped_column(nullable=True)
    gst: Mapped[str] = mapped_column(nullable=True)
    msme_or_not: Mapped[str] = mapped_column(nullable=True)
    bank_account_name: Mapped[str] = mapped_column(nullable=True)
    bank_account_number: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"property(id={self.id},property_name={self.property_name},url={self.url})"


def initalize() -> None:
    db.session.add(User(username='admin', password='admin', level=1))
    db.session.add(User(username='muthu', password='muthu', level=2))
    db.session.add(Property(property_name='Flat1',
                            url='https://assets-news.housing.com/news/wp-content/uploads/2022/03/28143140/Difference-between-flat-and-apartment.jpg', location='Chennai', no_of_units=5, list_of_units='10-20', address='No.19khjdfhj'))
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


def update_or_add_properties(form_data: dict, url: str):
    results = db.session.query(Property).filter(
        Property.property_name == form_data['property_name'])

    user = None
    if results.first() is not None:
        user = results[0]
    else:
        user = User()

    for key in form_data:
        setattr(user, key, form_data[key])

    setattr(user, "url", url)

    db.session.commit()


def update_or_add_vendors(form_data: dict):
    results = db.session.query(Property).filter(
        Property.property_name == form_data['vendor_name'])

    user = None
    if results.first() is not None:
        user = results[0]
    else:
        user = User()

    for key in form_data:
        setattr(user, key, form_data[key])

    db.session.commit()


def get_properties_list():
    return list(db.session.query(Property).all())


def get_users_list():
    return list(db.session.query(User).all())


def get_users_details(username):
    return db.session.query(User).filter(User.username == username)[0]


def get_vendor_details(name):
    return db.session.query(Vendor).filter(Vendor.name == name)[0]


def delete_user(username):
    results = db.session.query(User).filter(User.username == username)
    if results.first() is not None:
        db.session.delete(results[0])
        db.session.commit()


if __name__ == "__main__":
    initalize()
    print(get_users_list())
    update_or_add_users("admin", "yahoo")
    print(get_users_list())
