def test_get_all_books_with_no_records(client):
    response = client.get("/books")
    response_body = response.get_json()
    
    # assert
    assert response.status_code == 200
    assert response_body == []
    
def test_get_one_book(client, two_saved_books):
    response = client.get("/books/1")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
    
def test_create_one_book(client):
    
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!"}
)
    
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 201
    assert response_body == "Book New Book was created successfully"