import model as model

#barebones implementation of Auth to demonstrate auth and data segregation
class Login:
    def login(self, username: str):
        user = model.USERS.get(username, None)
        if not user:
            raise ValueError("User not found.")
        print(f"Logged in as {username} ({user['role']})")
        return user
    