import time


def test_create_product(client, db):
    product_data = {
        "name": "New Product",
        "description": "A new product",
        "price": 100.0,
        "stock": 30
    }
    response = client.post("api/v1/products", json=product_data)
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == "New Product"
    assert product["price"] == 100.0
    assert product["stock"] == 30


def test_get_product(client, db):
    product_data = {
        "name": "Get Product",
        "description": "Product for testing get",
        "price": 50.0,
        "stock": 10
    }
    response = client.post("api/v1/products", json=product_data)
    assert response.status_code == 200
    product = response.json()

    response = client.get(f"api/v1/products/{product['id']}")
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == "Get Product"
    assert product["description"] == "Product for testing get"
    assert product["price"] == 50.0
    assert product["stock"] == 10


def test_update_product(client, db):
    product_data = {
        "name": "Update Product",
        "description": "Product for update",
        "price": 75.0,
        "stock": 25
    }
    response = client.post("api/v1/products", json=product_data)
    assert response.status_code == 200
    product = response.json()

    updated_data = {
        "name": "Updated Product",
        "description": "Updated description",
        "price": 80.0,
        "stock": 15
    }
    response = client.put(
        f"api/v1/products/{product['id']}", json=updated_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == "Updated Product"
    assert updated_product["description"] == "Updated description"
    assert updated_product["price"] == 80.0
    assert updated_product["stock"] == 15


def test_delete_product(client, db):
    product_data = {
        "name": "Delete Product",
        "description": "Product for deletion",
        "price": 60.0,
        "stock": 5
    }
    response = client.post("api/v1/products", json=product_data)
    assert response.status_code == 200
    product = response.json()

    response = client.delete(f"api/v1/products/{product['id']}")
    assert response.status_code == 200

    response = client.get(f"api/v1/products/{product['id']}")
    assert response.status_code == 404


def test_cache_read_products(client, db):
    product_data = {
        "name": "Cache Product",
        "description": "Product for caching test",
        "price": 40.0,
        "stock": 20
    }
    response = client.post("api/v1/products", json=product_data)
    assert response.status_code == 200

    start_time = time.time()
    response = client.get("api/v1/products")
    assert response.status_code == 200
    first_response_time = time.time() - start_time

    assert first_response_time > 0

    start_time = time.time()
    response = client.get("api/v1/products")
    assert response.status_code == 200
    second_response_time = time.time() - start_time

    assert second_response_time < first_response_time
