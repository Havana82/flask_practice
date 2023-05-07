from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, abort, make_response, request

# cnalass Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description
# books = [
#     Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
#     Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imagiry world.")]

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")
# helper function
authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if not model :
        abort(make_response({"message" : f"{cls.__name__} {model_id} not found"}, 404))
    return model

# routes
@books_bp.route("", methods=['POST'])
def create_book():
    request_body = request.get_json()
    new_book = Book.from_dict(request_body)
    db.session.add(new_book)
    db.session.commit()
    
    return make_response(jsonify(f"Book {new_book.title} was created successfully"), 201)

@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    books_response= []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_model(Book, book_id)
    
    return book.to_dict()

@books_bp.route("/<book_id>", methods = ["PUT"])
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]
    
    db.session.commit()
    return make_response(jsonify(f"Book {book_id} updated succesffuly"))

@books_bp.route("/<book_id>", methods = ["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return make_response(jsonify(f"Book {book_id} deleted succesffuly"))

@authors_bp.route("", methods = ['POST'])
def create_author():
    request_body = request.get_json()
    new_author = Author(name = request_body["name"])
    
    db.session.add(new_author)
    db.session.commit
    
@authors_bp.route("", methods = ['GET'])
def get_authors():
    response_body = []
    authors = Author.query.all()
    for author in authors:
        response_body.append({"name": author.name})
    
    return jsonify(response_body)

@authors_bp.route('/<author_id>/books', methods = ['POST'])
def create_book(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"],
                    author=author)
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@authors_bp.route('/<author_id>/books', methods=['GET'])
def read_books(author_id):
    author = validate_model(Author, author_id)
    books_response = []
    for book in author.books:
        books_response.append(
            {"id": book.id,
            "title": book.title,
            "description": book.description
            }
        )
    return jsonify(books_response)

    