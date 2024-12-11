from flask import Flask, render_template, request, redirect, flash, session, send_file
import os
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from googletrans import Translator


# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)


# Initialize the Translator
translator = Translator()

# Home route
@app.route('/')
def home():
    return redirect('/signup')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return submit_signup()
    return render_template('signup-btn.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

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

        # Simulate a successful signup and redirect to login
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
        if email and password:  # Simplified condition for demo purposes
            session['user_id'] = email  # Dummy user ID
            session['email'] = email
            flash("Login successful!", "success")
            return redirect('/form-filling')
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect('/login')
    except Exception as e:
        print(f"Unexpected Error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/login')

@app.route('/form-filling', methods=['GET', 'POST'])
def form_filling():
    if 'user_id' not in session:
        flash("Please log in to access the Medical Insurance Form.", "warning")
        return redirect('/login')

    if request.method == 'POST':
        return submit_form()  # Call the function to handle form submission

    return render_template('index.html')  # Render the form-filling template

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Retrieve form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        age = request.form.get('age')
        middle_name = request.form.get('middleName', '')
        gender = request.form.get('gender', '')
        status = request.form.get('status', '')
        dob = request.form.get('dob', None)
        street_address = request.form.get('streetAddress', '')
        city = request.form.get('city', '')
        state_province = request.form.get('stateProvince', '')
        zip_code = request.form.get('zipCode', '')
        phone_number = request.form.get('phoneNumber', '')
        applicant_type = request.form.get('applicantType', '')
        applicant_full_name = request.form.get('applicantFullName', '')
        applicant_gender = request.form.get('applicantGender', '')
        applicant_dob = request.form.get('applicantDob', None)
        digital_signature = request.form.get('digitalSignature', '')

        # Create PDF in memory
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.drawString(100, 750, f"First Name: {first_name}")
        c.drawString(100, 730, f"Last Name: {last_name}")
        c.drawString(100, 710, f"Email: {email}")
        c.drawString(100, 690, f"Age: {age}")
        c.drawString(100, 670, f"Middle Name: {middle_name}")
        c.drawString(100, 650, f"Gender: {gender}")
        c.drawString(100, 630, f"Status: {status}")
        c.drawString(100, 610, f"DOB: {dob}")
        c.drawString(100, 590, f"Street Address: {street_address}")
        c.drawString(100, 570, f"City: {city}")
        c.drawString(100, 550, f"State/Province: {state_province}")
        c.drawString(100, 530, f"Zip Code: {zip_code}")
        c.drawString(100, 510, f"Phone Number: {phone_number}")
        c.drawString(100, 490, f"Applicant Type: {applicant_type}")
        c.drawString(100, 470, f"Applicant Full Name: {applicant_full_name}")
        c.drawString(100, 450, f"Applicant Gender: {applicant_gender}")
        c.drawString(100, 430, f"Applicant DOB: {applicant_dob}")
        c.drawString(100, 410, f"Digital Signature: {digital_signature}")

        c.save()
        pdf_buffer.seek(0)

        # Send the PDF to the user
        return send_file(pdf_buffer, as_attachment=True, download_name="form_data.pdf", mimetype="application/pdf") 
        
    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while submitting the form. Please try again.", "error")
        return redirect('/form-filling')
        


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
