from flask import Blueprint, jsonify, request   
from database.db import get_db_connection
books_bp = Blueprint("books", __name__)  


@books_bp.route("/api/books", methods=["GET"])
def get_books():
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(books) 

@books_bp.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    cursor.close()
    connection.close()

    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book), 200      


@books_bp.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = [
        "user_id",
        "title",
        "author",
        "description",
        "category",
        "condition_status",
        "image"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        INSERT INTO books
        (user_id, title, author, description, category,
         condition_status, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["user_id"],
            data["title"],
            data["author"],
            data["description"],
            data["category"],
            data["condition_status"],
            data["image"]
        )
    )

    connection.commit()
    book_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Book added successfully",
        "id": book_id
    }), 201    