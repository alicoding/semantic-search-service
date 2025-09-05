def authenticate_user(username, password):
    # This function handles user authentication
    if username == "admin" and password == "secret":
        return True
    return False
