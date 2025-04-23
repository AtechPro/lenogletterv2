from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from letterbackend import generate_pdf, create_data

app = Flask(__name__)

# Configuration for output folder
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'output')
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Landing page with links to different letter forms."""
    return render_template('main.html')

PDF_NAME_MAP = {
    'cl': '1. Cover Letter - Technical Proposal.pdf',
    'ack': '2. Letter of Acknowledgement - EXHIBIT V.pdf',
    'scope': '3. Letter of Compliance - Attachment A - Scope of Work.pdf',
    'toc': '4. Letter of Compliance - Terms and Conditions.pdf',
}


@app.route('/<letter_type>', methods=['GET', 'POST'])
def letter_form(letter_type):
    """Form for generating a specific type of letter."""
    if request.method == 'POST':
        # Collect common form data
        reference_no = request.form.get('reference_no')
        contract_title = request.form.get('contract_title')
        subject = request.form.get('subject')
        contact_name = request.form.get('contact_name')
        designation = request.form.get('designation')

        # Handle document selection
        if letter_type != 'cl':
            documents = ["test"]  # Predefined documents for non-cl letters
        else:
            # Get all selected documents from checkboxes (will be a list)
            documents = request.form.getlist('documents[]')
            
            # If no documents were selected, provide an empty list
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

@app.route('/view/<letter_type>')
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

@app.route('/output/<path:filename>')
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

@app.route('/favicon.ico')
def favicon():
    return '', 204  # HTTP 204: No Content

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)