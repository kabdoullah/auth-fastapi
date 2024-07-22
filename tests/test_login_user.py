def test_particular_login_success(client, test_particular_user, login_data):
    response = client.post("/api/v1/login", data=login_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert "refresh_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_particular_login_incorrect_password(client, test_particular_user, login_data):
    login_data["password"] = "wrongpassword"
    response = client.post("/api/v1/login", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_particular_login_nonexistent_user(client, login_data):
    login_data["username"] = "nonexistent@example.com"
    response = client.post("/api/v1/login", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

# professional user login tests

def test_professional_login_success(client, test_profesional_user, login_data):
    response = client.post("/api/v1/login", data=login_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert "refresh_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_professional_login_incorrect_password(client, test_profesional_user, login_data):
    login_data["password"] = "wrongpassword"
    response = client.post("/api/v1/login", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_professional_login_nonexistent_user(client, login_data):
    login_data["username"] = "nonexistent@example.com"
    response = client.post("/api/v1/login", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


    