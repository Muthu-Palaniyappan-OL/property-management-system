import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def initalize() -> None:
    con = get_db_connection()
    c = con.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARYKEY UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        property_name TEXT PRIMARYKEY UNIQUE NOT NULL,
        url TEXT NOT NULL
    );
    """)

    c.execute(
        "INSERT OR REPLACE INTO users(username, password) VALUES('admin', 'admin')")

    c.execute(
        "INSERT OR REPLACE INTO users(username, password) VALUES('muthu', 'muthu')")

    c.execute(
        "INSERT OR REPLACE INTO properties (property_name, url) VALUES('FLAT1', 'https://cdn.confident-group.com/wp-content/uploads/2021/08/26224309/oakwood_gallery_image.jpg')")

    c.close()
    con.commit()


def validate_username_password(username, password):
    con = get_db_connection()
    c = con.cursor()
    c.execute(
        f"SELECT username, password from users WHERE username = \'{username}\' LIMIT 1")
    result = c.fetchall()
    if len(result) != 1:
        return False
    c.close()
    if password == result[0][1]:
        return True
    else:
        return False


def update_or_add_users(username, password):
    con = get_db_connection()
    c = con.cursor()
    c.execute(
        f"INSERT OR REPLACE into users (username, password) VALUES(\'{username}\', \'{password}\')")
    c.close()
    con.commit()


def get_properties_list():
    con = get_db_connection()
    c = con.cursor()

    c.execute("SELECT property_name, url FROM properties")
    result = c.fetchall()
    c.close()
    return result


def get_users_list():
    con = get_db_connection()
    c = con.cursor()

    c.execute("SELECT username FROM users")
    result = c.fetchall()
    c.close()
    return result


def delete_user(username):
    con = get_db_connection()
    c = con.cursor()

    c.execute(
        f"DELETE FROM users WHERE username = \'{username}\'")
    c.close()
    con.commit()


def get_property_details(property):
    con = get_db_connection()
    c = con.cursor()

    c.execute(
        f"SELECT property_name, url FROM properties WHERE property_name = \'{property}\'")
    result = c.fetchall()
    c.close()
    return result
