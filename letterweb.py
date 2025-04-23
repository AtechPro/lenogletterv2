from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from letterbackend import generate_pdf, create_data

app = Flask(__name__)

# Configuration for output folder
app.config['OUTPUT_FOLDER'] = 'output'
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Landing page with links to different letter forms."""
    return render_template('home.html')

@app.route('/<letter_type>', methods=['GET', 'POST'])
def letter_form(letter_type):
    """Form for generating a specific type of letter."""
    if request.method == 'POST':
        # Collect form data
        reference_no = request.form.get('reference_no')
        contract_title = request.form.get('contract_title')
        subject = request.form.get('subject')
        documents = request.form.get('documents').split(',')  # Split by comma
        contact_name = request.form.get('contact_name')
        designation = request.form.get('designation')

        # Create data dictionary
        data = create_data(
            reference_no=reference_no,
            contract_title=contract_title,
            subject=subject,
            documents=documents,
            contact_name=contact_name,
            designation=designation
        )

        # Generate PDF
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{letter_type}.pdf")
        generate_pdf(data=data, document_type=letter_type, output_path=output_path)

        # Redirect to PDF viewer
        return redirect(url_for('view_pdf', letter_type=letter_type))

    # Render the appropriate form based on letter type
    return render_template(f'{letter_type}_form.html')

@app.route('/view/<letter_type>')
def view_pdf(letter_type):
    """Render the generated PDF in the browser."""
    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{letter_type}.pdf")
    return render_template('view_pdf.html', pdf_path=f"/static/{letter_type}.pdf")

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (e.g., PDFs)."""
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))

if __name__ == '__main__':
    app.run(debug=True)