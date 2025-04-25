from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory, session, jsonify, flash
import os
from letterbackend import generate_pdf, create_data
from databases.lenogdb import LetterForm, SessionLocal, User
from sqlalchemy.exc import SQLAlchemyError
import json 
from functools import wraps

app = Flask(__name__)
app.secret_key = 'JawaJawaJawaGahDamnDiuLeiLouMou'  # Change this to a secure key in production

app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'output')
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def create_admin_user():
    db = SessionLocal()
    try:
        # Check if the admin user already exists
        admin_user = db.query(User).filter_by(username="admin").first()
        if not admin_user:
            # Create the admin user
            admin_user = User(username="lenogadmin")
            admin_user.set_password("lenog12345")  # Replace "password" with your desired password
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
    except Exception as e:
        db.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

# Call this function to create the admin user
create_admin_user()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if the request is JSON (AJAX)
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            db = SessionLocal()
            user = db.query(User).filter_by(username=username).first()

            if user and user.verify_password(password):
                session['logged_in'] = True
                return jsonify({"success": True, "message": "Login successful!"})
            else:
                return jsonify({"success": False, "message": "Invalid username or password"})
        else:
            # Handle traditional form submission as a fallback
            username = request.form.get('username')
            password = request.form.get('password')

            db = SessionLocal()
            user = db.query(User).filter_by(username=username).first()

            if user and user.verify_password(password):
                session['logged_in'] = True
                flash("Login successful!", "success")
                return redirect(url_for('index'))
            else:
                flash("Invalid username or password", "danger")
                return redirect(url_for('login'))

    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            # Flash a message to inform the user
            flash("You need to log in first.", "warning")
            # Redirect to the login page
            return redirect(url_for('login'))
        # If the user is logged in, proceed to the requested route
        return f(*args, **kwargs)
    return decorated_function

    
@app.route('/logout')
def logout():
        # Clear the session to log the user out
        session.clear()
        # Flash a message to inform the user
        flash("You have been logged out.", "info")
        # Redirect to the login page
        return redirect(url_for('login'))   

@app.route('/')
@login_required
def index():
    return render_template('main.html')

PDF_NAME_MAP = {
    'cl': '1. Cover Letter - Technical Proposal.pdf',
    'ack': '4. Letter of Acknowledgement - EXHIBIT V.pdf',
    'scope': '2. Letter of Compliance - Attachment A - Scope of Work.pdf',
    'toc': '3. Letter of Compliance - Terms and Conditions.pdf',
}


@app.route('/<letter_type>', methods=['GET', 'POST'])
@login_required
def letter_form(letter_type):
    """Form for generating a specific type of letter."""
    if request.method == 'POST':

        reference_no = request.form.get('reference_no')
        contract_title = request.form.get('contract_title')
        subject = request.form.get('subject')
        contact_name = request.form.get('contact_name')
        designation = request.form.get('designation')
        

        # Handle document selection
        if letter_type != 'cl':
            documents = ["Not Involved with the documents"] 
        else:
  
            documents = request.form.getlist('documents[]')
            

            if not documents:
                documents = []
        
        # Create data dictionary
        data = create_data(
            reference_no=reference_no,
            contract_title=contract_title,
            subject=subject,
            documents=documents,
            contact_name=contact_name,
            designation=designation
        )
        # Convert data to JSON for debugging
        print(f"Data for {letter_type}: {json.dumps(data, indent=2)}")  # Debugging log
        
        #fetch the created_data function
        reference_no = data.get("REFERENCE NO")
        contract_title = data.get("CONTRACT TITLE")
        subject = data.get("SUBJECT")
        contact_name = data.get("Contact title")
        designation = data.get("designation")
        no = data.get("no")  # Phone number
        email = data.get("email")  # Email address

        # Validate required fields
        if not no or not email:
            return "Phone number and email are required", 400
        # Save to database
        try:
            db = SessionLocal()
            entry = LetterForm(
            letter_type=letter_type,
            reference_no=reference_no,
            contract_title=contract_title,
            subject=subject,
            contact_name=contact_name,
            designation=designation,
            no=no,
            email=email
            )
            entry.set_documents(documents)
            db.add(entry)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Database error: {e}")  # Log any DB issues
        finally:
            db.close()

        # Get the corresponding filename from the mapping
        pdf_filename = PDF_NAME_MAP.get(letter_type)
        if not pdf_filename:
            return "Invalid letter type", 404

        # Generate PDF with the dynamic filename
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
        generate_pdf(data=data, document_type=letter_type, output_path=output_path)

        # Redirect to PDF viewer
        return redirect(url_for('view_pdf', letter_type=letter_type))

    # Render the appropriate form based on letter type
    return render_template(f'{letter_type}')

@app.route('/view/<letter_type>') #pdf rendering 
@login_required
def view_pdf(letter_type):
    """Render the generated PDF in the browser."""
    # Get the corresponding filename from the mapping
    pdf_filename = PDF_NAME_MAP.get(letter_type)
    if not pdf_filename:
        return "Invalid letter type", 404

    # Construct the full path to the PDF file
    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)

    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        return "PDF not found", 404

    # Pass only the filename to the template
    return render_template('view_pdf.html', pdf_filename=pdf_filename)

@app.route('/output/<path:filename>') #pdf output file serving (for download)
@login_required
def serve_static(filename):
    # Sanitize the filename to prevent directory traversal attacks
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], safe_filename)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")  # Debugging log
        return "File not found", 404
    
    # Serve the file
    return send_file(file_path)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)