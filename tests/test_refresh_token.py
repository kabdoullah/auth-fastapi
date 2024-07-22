
def test_par_refresh_token_success(client, test_particular_user, valid_par_refresh_token):
    header = {
        "refresh_token": "Bearer " + valid_par_refresh_token,
    }
    response = client.post("/api/v1/refresh", json={}, headers=header)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["refresh_token"] == valid_par_refresh_token
    assert json_response["token_type"] == "bearer"

# def test_refresh_token_invalid(client):
#     invalid_refresh_token = "invalid_token"
#     response = client.post("/api/v1/refresh", json={"refresh_token": invalid_refresh_token})
#     assert response.status_code == 401
#     assert response.json()["detail"] == "Could not validate credentials"

# def test_refresh_token_user_not_found(client, test_db, invalid_refresh_token):
   
#     response = client.post("/api/v1/refresh", json={"refresh_token": invalid_refresh_token})
#     assert response.status_code == 401
#     assert response.json()["detail"] == "User not found"
