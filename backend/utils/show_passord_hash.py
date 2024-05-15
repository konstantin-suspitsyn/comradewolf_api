from backend.db.user_service import create_password_hash

if __name__ == "__main__":
    password = input("Введи пароль: ")
    print(create_password_hash(password))
