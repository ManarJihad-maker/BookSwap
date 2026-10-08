from flask import Flask
from database.db import get_db_connection
from routes.books import books_bp
app = Flask(__name__)  
app.register_blueprint(books_bp)  

@app.route("/")
def home():
    return "BookSwap Backend is running!"


@app.route("/test-db")
def test_db():
    connection = get_db_connection()

    if connection:
        connection.close()
        return "Database connection OK!"

    return "Database connection failed!"


if __name__ == "__main__":   
    app.run(debug=True)  