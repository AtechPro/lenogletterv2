from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory, session, jsonify, flash
import os
from letterbackend import generate_pdf, create_data
from databases.lenogdb import LetterForm, SessionLocal, User
from sqlalchemy.exc import SQLAlchemyError
import json 
from functools import wraps
import pandas as pd
from io import BytesIO
from openpyxl.utils import get_column_letter

app = Flask(__name__)
app.secret_key = 'JawaJawaJawaGahDamnDiuLeiLouMou'  # Change this to a secure key in production

app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'output')
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def create_user(db, username, password):
    """
    Helper function to create a user in the database.
    :param db: Database session
    :param username: Username for the new user
    :param password: Password for the new user
    :return: None
    """
    try:
        # Check if the user already exists
        existing_user = db.query(User).filter_by(username=username).first()
        if not existing_user:
            # Create the user
            new_user = User(username=username)
            new_user.set_password(password)  # Assuming set_password hashes the password
            db.add(new_user)
            db.commit()
            print(f"User '{username}' created successfully.")
        else:
            print(f"User '{username}' already exists.")
    except Exception as e:
        db.rollback()
        print(f"Error creating user '{username}': {e}")


def create_admin_user():
    db = SessionLocal()
    try:
        # Create the admin user
        create_user(db, username="lenogadmin", password="lenog12345")
        create_user(db, username="abc", password="123")

    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred: {e}")
    finally:
        db.close()


create_admin_user()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

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
            flash("You need to log in first.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

    
@app.route('/logout')
def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for('login'))   

@app.route('/')
@login_required
def index():
    return render_template('main.html')

PDF_NAME_MAP = {
    'cl': '1. Cover Letter - Technical Proposal.pdf',
    'scope': '2. Letter of Compliance - Attachment A - Scope of Work.pdf',
    'ack': '4. Letter of Acknowledgement - EXHIBIT V.pdf',
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
        
        data = create_data(
            reference_no=reference_no,
            contract_title=contract_title,
            subject=subject,
            documents=documents,
            contact_name=contact_name,
            designation=designation
        )
        # print(f"Data for {letter_type}: {json.dumps(data, indent=2)}")  # Debugging log
        
        #fetch the created_data function
        reference_no = data.get("REFERENCE NO")
        contract_title = data.get("CONTRACT TITLE")
        subject = data.get("SUBJECT")
        contact_name = data.get("Contact title")
        designation = data.get("designation")
        no = data.get("no")  
        email = data.get("email")  
        if not no or not email:
            return "Phone number and email are required", 400
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
            print(f"Database error: {e}")  
        finally:
            db.close()
        pdf_filename = PDF_NAME_MAP.get(letter_type)
        if not pdf_filename:
            return "Invalid letter type", 404
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
        generate_pdf(data=data, document_type=letter_type, output_path=output_path)
        return redirect(url_for('view_pdf', letter_type=letter_type))
    return render_template(f'{letter_type}')

@app.route('/view/<letter_type>') 
@login_required
def view_pdf(letter_type):
    pdf_filename = PDF_NAME_MAP.get(letter_type)
    if not pdf_filename:
        return "Invalid letter type", 404
    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
    if not os.path.exists(pdf_path):
        return "PDF not found", 404
    return render_template('view_pdf.html', pdf_filename=pdf_filename)

@app.route('/output/<path:filename>')
@login_required
def serve_static(filename):
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], safe_filename)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")  
        return "File not found", 404
    
    # Serve the file
    return send_file(file_path)

@app.route('/letters', methods=['GET'])
@login_required
def view_letters():
    # Get filter from query string
    letter_type = request.args.get('letter_type', None)

    db = SessionLocal()
    try:
        # Query the database
        query = db.query(LetterForm)
        if letter_type:
            query = query.filter_by(letter_type=letter_type)
        letters = query.all()

        # Convert letters to JSON format
        letters_json = [
            {
                "id": letter.id,
                "letter_type": letter.letter_type,
                "reference_no": letter.reference_no,
                "contract_title": letter.contract_title,
                "subject": letter.subject,
                "contact_name": letter.contact_name,
                "designation": letter.designation,
                "phone_no": letter.no,
                "email": letter.email,
            }
            for letter in letters
        ]

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        letters_json = []
    finally:
        db.close()

    # Render the template with JSON data
    return render_template('excelviewer.html', letters=letters_json, letter_type=letter_type)

@app.route('/api/letters', methods=['GET'])
@login_required
def api_view_letters():
    # Get filter from query string
    letter_type = request.args.get('letter_type', None)

    db = SessionLocal()
    try:
        # Query the database
        query = db.query(LetterForm)
        if letter_type:
            query = query.filter_by(letter_type=letter_type)
        letters = query.all()

        # Convert letters to JSON format
        letters_json = [
            {
                "id": letter.id,
                "letter_type": letter.letter_type,
                "reference_no": letter.reference_no,
                "contract_title": letter.contract_title,
                "subject": letter.subject,
                "contact_name": letter.contact_name,
                "designation": letter.designation,
                "phone_no": letter.no,
                "email": letter.email,
            }
            for letter in letters
        ]

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        letters_json = []
    finally:
        db.close()

    return jsonify(letters_json)

@app.route('/export/<letter_type>', methods=['GET'])
@login_required
def export_to_excel(letter_type):
    """Export filtered letters to an Excel file with auto-width columns and a serial number column."""
    db = SessionLocal()
    try:
        # Query the database
        query = db.query(LetterForm)
        if letter_type != 'all':
            query = query.filter_by(letter_type=letter_type)
        letters = query.all()

        # Convert data to a DataFrame
        data = [
            {
                "Letter Type": letter.letter_type,
                "Reference No": letter.reference_no,
                "Contract Title": letter.contract_title,
                "Subject": letter.subject,
                "Contact Name": letter.contact_name,
                "Designation": letter.designation,
                "Phone No": letter.no,
                "Email": letter.email,
            }
            for letter in letters
        ]
        df = pd.DataFrame(data)

        # Add a "No." column (auto-incrementing serial number)
        df.insert(0, "No.", range(1, len(df) + 1))

        # Export to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=f"{letter_type}_letters")

            # Access the workbook and worksheet to adjust column widths
            workbook = writer.book
            worksheet = writer.sheets[f"{letter_type}_letters"]

            # Auto-adjust column widths
            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter  # Get the column name (e.g., 'A', 'B', etc.)
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except TypeError:
                        pass
                adjusted_width = (max_length + 2)  # Add some padding
                worksheet.column_dimensions[column].width = adjusted_width

        output.seek(0)

        # Return the Excel file
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f"{letter_type}_letters.xlsx"
        )
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        flash("An error occurred while exporting data.", "danger")
        return redirect(url_for('view_letters'))
    finally:
        db.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)