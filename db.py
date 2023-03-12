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


def update_or_add_properties(property_name, url, category, location, no_of_units, list_of_units, address):
    results = db.session.query(Property).filter(
        Property.property_name == property_name)
    if results.first() is not None:
        results[0].property_name = property_name
        results[0].url = url
        results[0].category = category
        results[0].location = location
        results[0].no_of_units = no_of_units
        results[0].list_of_units = list_of_units
        results[0].address = address
    else:
        db.session.add(Property(property_name=property_name, url=url, category=category, location=location,
                       no_of_units=no_of_units, list_of_units=list_of_units, address=address))
    db.session.commit()


def get_properties_list():
    return list(db.session.query(Property).all())


def get_users_list():
    return list(db.session.query(User).all())


def get_users_details(username):
    return db.session.query(User).filter(User.username == username)[0]


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
