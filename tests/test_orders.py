def test_create_order_with_sufficient_stock(client, db):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "stock": 50
    }

    response = client.post("api/v1/products", json=product_data)
    assert response.status_code == 200
    product = response.json()
    order_data = {
        "status": "in process",
        "items": [{"product_id": product["id"], "quantity": 10}]
    }
    response = client.post("api/v1/orders", json=order_data)
    assert response.status_code == 200

    updated_product = client.get(f"api/v1/products/{product['id']}")
    assert updated_product.status_code == 200
    assert updated_product.json()["stock"] == 40


def test_create_order_with_insufficient_stock(client, db):
    product_data = {
        "name": "Limited Stock Product",
        "description": "Test Description",
        "price": 150.0,
        "stock": 5
    }

    response = client.post("api/v1/products", json=product_data)
    assert response.status_code == 200
    product = response.json()

    order_data = {
        "status": "in process",
        "items": [{"product_id": product["id"], "quantity": 10}]
    }
    response = client.post("api/v1/orders", json=order_data)

    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 400
    assert response.json()[
        "detail"] == f"Not enough stock for product {product['id']}"
