import mysql.connector
from werkzeug.security import generate_password_hash

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rishiraj@123",
    database="insurancedb"
)

try:
    cursor = db.cursor()

    # Fetch all users
    cursor.execute("SELECT id, password FROM Users")
    users = cursor.fetchall()

    # Update each user's password to be hashed
    for user in users:
        user_id, plain_password = user
        hashed_password = generate_password_hash(plain_password)
        
        # Update the password in the database
        cursor.execute(
            "UPDATE Users SET password = %s WHERE id = %s",
            (hashed_password, user_id)
        )
    db.commit()
    print("Passwords updated to hashed values.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    cursor.close()
    db.close()
