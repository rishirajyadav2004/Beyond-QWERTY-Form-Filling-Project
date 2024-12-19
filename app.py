from flask import Flask, render_template, request, redirect, flash, session, send_file, after_this_request, url_for
import os
import io
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from googletrans import Translator




# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize the Translator
translator = Translator()

# Environment variables (set these in Render's environment variables section)
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Connect to PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    return conn

# Home route
@app.route('/')
def home():
    return redirect('/signup')

@app.route('/templates/index.html')
def voice():
    return render_template('index.html')


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return submit_signup()
    return render_template('signup-btn.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/homepage')  # Change this to any route you want
def homepage():
    return render_template('index.html')

@app.route('/templates/Docker.html')
def docker_page():
    return render_template('Docker.html')

@app.route('/templates/Detect.html')
def detect():
    return render_template('Detect.html')

@app.route('/templates/Resources.html')
def resources():
    return render_template('Resources.html')

@app.route('/templates/Enterprise.html')
def enterprise():
    return render_template('Enterprise.html')

@app.route('/templates/Team.html')
def team():
    return render_template('Team.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return submit_login()
    return render_template('login-btn.html')

# Signup submission route
@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    try:
        first_name = request.form['firstName']
        middle_name = request.form.get('middleName', '')
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Connect to the database and insert user data
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Users (firstName, middleName, lastName, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, middle_name, last_name, email, hashed_password))
        conn.commit()
        cur.close()
        conn.close()

        flash("Signup successful! Please log in.", "success")
        return redirect('/login')
    except Exception as e:
        print(f"Unexpected Error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/signup')

# Login submission route
@app.route('/submit_login', methods=['POST'])
def submit_login():
    email = request.form['email']
    password = request.form['password']
    try:
        if email and password:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Query to fetch user from the Users table
            cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[5], password):  # user[5] is the password field (assuming it is at index 5)
                session['user_id'] = user[0]  # Store user ID (assuming it is at index 0)
                session['email'] = user[4]  # Store user email (assuming it is at index 4)
                flash("Login successful!", "success")
                cursor.close()
                conn.close()
                return redirect('/form-filling')
            else:
                flash("Invalid credentials. Please try again.", "error")
                cursor.close()
                conn.close()
                return redirect('/login')
        else:
            flash("Please enter both email and password.", "warning")
            return redirect('/login')
    except Exception as e:
        print(f"Unexpected Error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/login')



# Valid ENUM values
VALID_GENDER_VALUES = ['Male', 'Female', 'Other']
VALID_STATUS_VALUES = ['Single', 'Married', 'Student', 'Employed', 'Other']
VALID_APPLICANT_TYPE_VALUES = ['Partner', 'Child', 'Single', 'Married', 'Divorced', 'Widowed', 'Other']


@app.route('/form-filling', methods=['GET', 'POST'])
def form_filling():
    if 'user_id' not in session:
        flash("Please log in to access the Medical Insurance Form.", "warning")
        return redirect('/login')

    if request.method == 'POST':
        try:
            # Retrieve form data
            first_name = request.form['firstName']
            middle_name = request.form.get('middleName', '')
            last_name = request.form['lastName']
            gender = request.form['gender']
            age = int(request.form['age'])
            status = request.form['status']
            dob = request.form['dob']
            street_address = request.form['streetAddress']
            city = request.form['city']
            state_province = request.form['stateProvince']
            zip_code = request.form['zipCode']
            email = request.form['email']
            phone_number = request.form['phoneNumber']
            applicant_type = request.form['applicantType']
            applicant_full_name = request.form.get('applicantFullName', '')
            applicant_gender = request.form.get('applicantGender', '')
            applicant_dob = request.form.get('applicantDob', None)
            digital_signature = request.files.get('digitalSignature')
            signature_data = digital_signature.read() if digital_signature else None

            # Validate ENUM fields
            if gender not in VALID_GENDER_VALUES:
                flash(f"Invalid gender value. Allowed values: {VALID_GENDER_VALUES}", "error")
                return redirect('/form-filling')

            if status not in VALID_STATUS_VALUES:
                flash(f"Invalid status value. Allowed values: {VALID_STATUS_VALUES}", "error")
                return redirect('/form-filling')

            if applicant_type not in VALID_APPLICANT_TYPE_VALUES:
                flash(f"Invalid applicant type. Allowed values: {VALID_APPLICANT_TYPE_VALUES}", "error")
                return redirect('/form-filling')

            # Database insertion logic
            query = """
            INSERT INTO InsuranceForms (
                firstName, middleName, lastName, gender, age, status, dob, streetAddress, city, 
                stateProvince, zipCode, email, phoneNumber, applicantType, applicantFullName, 
                applicantGender, applicantDob, digitalSignature
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, middle_name, last_name, gender, age, status, dob, street_address, city,
                      state_province, zip_code, email, phone_number, applicant_type, applicant_full_name,
                      applicant_gender, applicant_dob, signature_data)

            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                    conn.commit()

            
            # Create an in-memory buffer to save the PDF
            pdf_buffer = io.BytesIO()

            # PDF Generation Logic
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "Medical Insurance Form Submission")
            c.line(100, 745, 500, 745)  # Draw a line

            # Add form fields
            c.drawString(100, 720, f"First Name: {first_name}")
            c.drawString(100, 700, f"Middle Name: {middle_name}")
            c.drawString(100, 680, f"Last Name: {last_name}")
            c.drawString(100, 660, f"Gender: {gender}")
            c.drawString(100, 640, f"Age: {age}")
            c.drawString(100, 620, f"Status: {status}")
            c.drawString(100, 600, f"Date of Birth: {dob}")
            c.drawString(100, 580, f"Address: {street_address}, {city}, {state_province} - {zip_code}")
            c.drawString(100, 560, f"Email: {email}")
            c.drawString(100, 540, f"Phone Number: {phone_number}")
            c.drawString(100, 520, f"Applicant Type: {applicant_type}")
            c.drawString(100, 500, f"Applicant Full Name: {applicant_full_name}")
            c.drawString(100, 480, f"Applicant Gender: {applicant_gender}")
            c.drawString(100, 460, f"Applicant DOB: {applicant_dob}")

            c.save()

            # Move the buffer cursor to the beginning of the file
            pdf_buffer.seek(0)

           # Return the PDF directly to the client
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=f"medical_form_{first_name}_{last_name}.pdf",
                mimetype="application/pdf"
            )

        except Exception as e:
            flash(f"Unexpected error: {str(e)}", "error")
            return redirect('/form-filling')

    return render_template('index.html')
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
