import mysql.connector
import getpass

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your mysql username",
        password="your mysql password",
        database="user_data"
    )

def register():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("Choose a username: ")
    password = getpass.getpass("Choose a password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        print("✅ Registration successful!\n")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def login():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
        print("✅ Login successful!\n")
        user_dashboard(user_id)
    else:
        print("❌ Login failed. Incorrect credentials.\n")

    cursor.close()
    conn.close()

def user_dashboard(user_id):
    while True:
        print("1. Add new note")
        print("2. View my notes")
        print("3. Logout")
        choice = input("Choose an option: ")

        conn = connect_db()
        cursor = conn.cursor()

        if choice == '1':
            note = input("Enter your note: ")
            cursor.execute("INSERT INTO user_texts (user_id, content) VALUES (%s, %s)", (user_id, note))
            conn.commit()
            print("✅ Note saved!\n")
        elif choice == '2':
            cursor.execute("SELECT content FROM user_texts WHERE user_id=%s", (user_id,))
            notes = cursor.fetchall()
            print("\n📄 Your Notes:")
            for idx, (note,) in enumerate(notes, 1):
                print(f"{idx}. {note}")
            print()
        elif choice == '3':
            print("👋 Logged out.\n")
            break
        else:
            print("❌ Invalid choice.\n")

        cursor.close()
        conn.close()

def main():
    while True:
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        option = input("Choose an option: ")

        if option == '1':
            login()
        elif option == '2':
            register()
        elif option == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")

if __name__ == "__main__":
    main()
