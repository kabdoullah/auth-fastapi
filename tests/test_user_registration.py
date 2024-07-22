def test_register_particular_success(client,particular_user_data):
    response = client.post("/api/v1/register/particular", json=particular_user_data)
    assert response.status_code == 201
    assert response.json()["email"] == particular_user_data['email']
    assert "password" not in response.json()


def test_register_particular_email_already_registered(client, particular_user_data):
    response = client.post("/api/v1/register/particular", json=particular_user_data)
    assert response.status_code == 201
    response = client.post("/api/v1/register/particular", json=particular_user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"



def test_register_professional_success(client, professional_user_data):
    response = client.post("/api/v1/register/professional", json=professional_user_data)
    assert response.status_code == 201
    assert response.json()["email"] == professional_user_data['email']
    assert "password" not in response.json()

def test_register_professional_email_already_registered(client, professional_user_data):
    response = client.post("/api/v1/register/professional", json=professional_user_data)
    assert response.status_code == 201

    response = client.post("/api/v1/register/professional", json=professional_user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
   


