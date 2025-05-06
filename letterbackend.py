from fpdf import FPDF
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Set larger margins (in millimeters)
        self.set_left_margin(20)   # Increased from 10 to 15
        self.set_right_margin(20)  # Increased from 10 to 15
        self.set_top_margin(20)    # You can also adjust the top margin if needed

    def header(self):
        # Add the company header image if it exists
        if os.path.exists(resource_path('icons/Company Header.jpg')):
            self.image(resource_path('icons/Company Header.jpg'), x=20, y=10, w=170)  # Adjusted x and y for better placement
        # Set the height of the header
        self.set_y(50)  # Adjusted to accommodate larger top margin if necessary


class CoverLetterSection:
    @staticmethod
    def number_to_letter(n):
        """Convert a number to its corresponding uppercase letter (0 → A, 1 → B, etc.)"""
        return chr(ord('a') + n)

    @staticmethod
    def add(pdf, data):
        """Add the cover letter section to the PDF"""
        pdf.set_y(40)
        
        # Title
        pdf.set_font("Helvetica", size=14, style='BU')
        pdf.cell(0, 10, 'COVER LETTER (TECHNICAL PROPOSAL)', align='C', ln=True)
        pdf.ln(5)
        
        def add_labeled_cell(pdf, label, key, data_dict, width=60):
            pdf.set_font("Helvetica", size=11, style='B')
            pdf.cell(width, 6, f'{label}:', border=0)
            pdf.set_font("Helvetica", size=11, style='BU')
            text = data_dict.get(key, "").upper()
            if len(text) > 0:
                pdf.multi_cell(0, 6, text, align='L')
            else:
                pdf.cell(0, 6, '', ln=True)
            pdf.ln(2)

        # Add Reference
        add_labeled_cell(pdf, 'REFERENCE NO', 'REFERENCE NO', data)

        # Add Contract Title
        add_labeled_cell(pdf, 'CONTRACT TITLE', 'CONTRACT TITLE', data)

        # Add Subject
        add_labeled_cell(pdf, 'SUBJECT', 'SUBJECT', data)

        pdf.ln(3)
        
        # Main body text
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, "Dear Sir/Madam,", align='J')
        pdf.write(6, "We would like to thank PETRONAS for the opportunity to quote for the above tender. We are pleased to hereby submit our Technical Proposal for the ")
        
        pdf.set_font("Helvetica", style="BU", size=11)
        pdf.write(6, data.get("CONTRACT TITLE", "").upper())
        pdf.set_font("Helvetica", "", 11)  # Reset to normal font

        pdf.write(6, ". We hope our Technical Proposal and capabilities meet your requirement.\n")
        pdf.ln(3)
        # List of documents
        pdf.set_font("Helvetica", "B", 11)  # Set to Bold
        pdf.write(6, "List of documents:\n")
        pdf.set_font("Helvetica", "", 11)  # Reset to normal font

        user_documents = data.get("documents", [])
        if not user_documents:
            pdf.write(6, "No documents provided.\n")
        else:
            for index, doc in enumerate(user_documents):
                prefix = CoverLetterSection.number_to_letter(index) + '.'
                pdf.cell(10, 10, '')
                pdf.cell(10, 10, prefix)
                pdf.cell(0, 10, doc, ln=True)

        

class ScopeSection:
    @staticmethod
    def add(pdf, data):
        """Add the cover letter section to the PDF"""
        pdf.set_y(40)
        
        # Title
        pdf.set_font("Helvetica", size=14, style='BU')
        pdf.cell(0, 10, 'LETTER OF COMPLIANCE TO SCOPE OF WORKS', align='C', ln=True)
        pdf.ln(5)
        
        # Reference, Contract Title, Subject
        def add_labeled_cell(pdf, label, key, data_dict, width=60):
            pdf.set_font("Helvetica", size=11, style='B')
            pdf.cell(width, 6, f'{label}:', border=0)
            pdf.set_font("Helvetica", size=11, style='BU')
            text = data_dict.get(key, "").upper()
            if len(text) > 0:
                pdf.multi_cell(0, 6, text, align='L')
            else:
                pdf.cell(0, 6, '', ln=True)
            pdf.ln(2)

        # Add Reference
        add_labeled_cell(pdf, 'REFERENCE NO', 'REFERENCE NO', data)

        # Add Contract Title
        add_labeled_cell(pdf, 'CONTRACT TITLE', 'CONTRACT TITLE', data)

        # Add Subject
        add_labeled_cell(pdf, 'SUBJECT', 'SUBJECT', data)

        pdf.ln(3)
        
        # Main body text
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, "Dear Sir/Madam,\n", align='J')
        # Use write instead of multi_cell to avoid spacing problems
        pdf.write(6, "We are writing in response to the ")
        
        pdf.set_font("Helvetica", style="BU", size=11)
        pdf.write(6, data.get("REFERENCE NO", "").upper())
        pdf.set_font("Helvetica", "", 11)  # Reset to normal font

        # Write inline instead of multi_cell to avoid space issues
        pdf.write(6, " for ")

        # Underlined contract title
        pdf.set_font("Helvetica", style="BU", size=11)
        pdf.write(6, data.get("CONTRACT TITLE", "").upper())
        pdf.set_font("Helvetica", "", 11)  # Reset to normal font
        
        # Continue with normal text
        pdf.write(6, ". After a thorough review of the documents, we are pleased to submit our letter of compliance with the scope of work outlined in the ")
        pdf.set_font("Helvetica", "B", 11)
        pdf.write(6, "ATTACHMENT A - SCOPE OF WORKS.\n")
        pdf.set_font("Helvetica", "", 11)
        
        pdf.ln(3)
        # Multi-line content with proper width calculation
        text = "We would like to confirm our understanding of the requirements and specifications detailed in the tender documentation. Our team has carefully reviewed each section of Scope of Work, and we are fully committed to meet and comply with all the stipulated requirements, scopes, terms and conditions."
        
        # Calculate available width based on margins
        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(available_width, 6, text, align='J')
        pdf.ln(3)

class ToCSection:
    @staticmethod
    def add(pdf, data):
        """Add the Letter of Compliance to Terms & Conditions section to the PDF"""
        pdf.set_y(40)

        # Title
        pdf.set_font("Helvetica", size=14, style='BU')
        pdf.cell(0, 10, 'LETTER OF COMPLIANCE TO TERMS & CONDITIONS', align='C', ln=True)
        pdf.ln(5)
        
        # Helper function to add labeled cells
        def add_labeled_cell(pdf, label, key, data_dict, width=60):
            pdf.set_font("Helvetica", size=11, style='B')
            pdf.cell(width, 6, f'{label}:', border=0)
            pdf.set_font("Helvetica", size=11, style='BU')
            text = data_dict.get(key, "").upper()
            if len(text) > 0:
                pdf.multi_cell(0, 6, text, align='L')
            else:
                pdf.cell(0, 6, '', ln=True)
            pdf.ln(2)

        # Add Reference No, Contract Title, Subject
        add_labeled_cell(pdf, 'REFERENCE NO', 'REFERENCE NO', data)
        add_labeled_cell(pdf, 'CONTRACT TITLE', 'CONTRACT TITLE', data)
        add_labeled_cell(pdf, 'SUBJECT', 'SUBJECT', data)

        pdf.ln(5)  # Extra space before body text

        # Main body text
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, "Dear Sir/Madam,\n", align='J')

        pdf.write(6, "We are writing in response to the ")

        # Underlined Reference Number
        pdf.set_font("Helvetica", style="BU", size=11)
        pdf.write(6, data.get("REFERENCE NO", "").upper())
        pdf.set_font("Helvetica", "", 11)

        pdf.write(6, " for ")

        # Underlined Contract Title
        pdf.set_font("Helvetica", style="BU", size=11)
        pdf.write(6, data.get("CONTRACT TITLE", "").upper())
        pdf.set_font("Helvetica", "", 11)

        pdf.write(6, ". After a thorough review of the documents, we are pleased to submit our letter of compliance with the terms & conditions outlined in the ")
        pdf.set_font("Helvetica", "B", 11)
        pdf.write(6, "ATTACHMENT B - TERMS & CONDITIONS.\n")
        pdf.set_font("Helvetica", "", 11)
        pdf.ln(3)

        # Multi-line paragraph
        body_text = (
            "We would like to confirm our understanding of the requirements and specifications detailed "
            "in the tender documentation. Our team has carefully reviewed each section of Terms & Conditions, "
            "and we are fully committed to meet and comply with all the stipulated requirements, terms and conditions."
        )

        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(available_width, 6, body_text, align='J')
        pdf.ln(3)
 
class AckSection:
    @staticmethod
    def add(pdf, data):
        pdf.set_y(40)
        # Title
        pdf.set_font("Helvetica", size=14, style='BU')
        pdf.cell(0, 10, 'LETTER OF ACKNOWLEDGEMENT TO EXHIBIT V', align='C', ln=True)
        pdf.ln(5)
        # Reference, Contract Title, Subject
        def add_labeled_cell(pdf, label, key, data_dict, width=60):
            pdf.set_font("Helvetica", size=11, style='B')
            pdf.cell(width, 6, f'{label}:', border=0)
            pdf.set_font("Helvetica", size=11, style='BU')
            text = data_dict.get(key, "").upper()
            if len(text) > 0:
                pdf.multi_cell(0, 6, text, align='L')
            else:
                pdf.cell(0, 6, '', ln=True)
            pdf.ln(2)

        # Add Reference
        add_labeled_cell(pdf, 'REFERENCE NO', 'REFERENCE NO', data)

        # Add Contract Title
        add_labeled_cell(pdf, 'CONTRACT TITLE', 'CONTRACT TITLE', data)

        # Add Subject
        add_labeled_cell(pdf, 'SUBJECT', 'SUBJECT', data)

        pdf.ln(5)
        
        # Main body text
        pdf.set_font("Helvetica", size=11)
        pdf.write(6, "Dear Sir/Madam,\n")
        pdf.ln(3)
        pdf.write(6, "We are writing this letter to acknowledge that we have read and understood the ")
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.write(6, "EXHIBIT V - HEALTH, SAFETY AND ENVIRONMENT REQUIREMENTS")
        pdf.set_font("Helvetica",size=11)
        pdf.write(6, " for ")
        pdf.set_font("Helvetica", style="BU", size=11)
        pdf.write(6, data.get("REFERENCE NO", "").upper())
        pdf.write(6, " ")
        pdf.set_font("Helvetica", style="BU", size=11)
        pdf.write(6, data.get("CONTRACT TITLE", "").upper())
        pdf.set_font("Helvetica", "", 11)  # Reset to normal font
        pdf.ln(10)


class ClarificationSection:
    @staticmethod
    def add(pdf, data):
        """Add the clarification contact section to the PDF"""
        contact_title = data.get('Contact title', '')
        contact_info = (
            f"For further clarification, do not hesitate to contact Mr. {contact_title} "
            f"at {data.get('no', '')} or email {data.get('email', '')}.\n"
        )
        # Calculate available width based on margins
        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(available_width, 6, contact_info)


class CompClarificationSection:
    @staticmethod
    def add(pdf, data):
        """Add the clarification contact section to the PDF"""
        contact_title = data.get('Contact title', '')
        contact_info = (
            f"Thank you for the bidding invitation. We look forward to the opportunity to contribute our expertise. "
            f"For further clarification, do not hesitate to contact Mr. {contact_title} "
            f"at {data.get('no', '')} or email {data.get('email', '')}.\n"
        )
        
        # Calculate available width based on margins
        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        # Use the calculated width to ensure text fits
        pdf.multi_cell(available_width, 6, contact_info)

class CoverClarificationSection:
    @staticmethod
    def add(pdf, data):
        pdf.ln(10)
        """Add the clarification contact section to the PDF"""
        contact_title = data.get('Contact title', '')
        contact_info = (
            f"For further clarification, do not hesitate to contact Mr. {contact_title} "
            f"at {data.get('no', '')} or email {data.get('email', '')}.\n"
        )
        # Calculate available width based on margins
        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(available_width, 6, contact_info)


class SignatureSection:
    @staticmethod
    def add(pdf, data):
        """Add the signature section to the PDF, ensuring it adheres to the PDF margins."""
        # Calculate the space required for the signature section
        REQUIRED_HEIGHT = 10 + 20 + 5 + 6 + 6 + 6 + 5  # Approximate height based on font sizes and spacing

        # Current vertical position
        current_y = pdf.get_y()
        # In fpdf2, we can access the page height via pdf.h and bottom margin via pdf.b_margin
        page_height = pdf.h - pdf.b_margin  # Total height minus bottom margin

        # Check if the signature section fits on the current page
        if current_y + REQUIRED_HEIGHT > page_height:
            pdf.add_page()  # Add a new page
            # Important: get new Y position after page break
            current_y = pdf.get_y()

        # Set the font for the thank you message
        pdf.set_font("Helvetica", "", 11)
        
        # Calculate the available width based on margins
        available_width = pdf.w - pdf.l_margin - pdf.r_margin

        # Thank you message
        pdf.cell(available_width, 10, "Thank you and best regards,", align='L', ln=True)

        # Signature image
        contact_image = data.get('contact_image_path', '')
        if contact_image and os.path.exists(contact_image):
            SIGNATURE_WIDTH = 60
            SIGNATURE_HEIGHT = 20

            # Calculate the x position to align with the left margin
            signature_x = pdf.l_margin
            signature_y = pdf.get_y()

            pdf.image(
                contact_image, 
                x=signature_x, 
                y=signature_y, 
                w=SIGNATURE_WIDTH,
                h=SIGNATURE_HEIGHT
            )

            pdf.ln(SIGNATURE_HEIGHT + 5)
        else:
            # If no signature image is available, align the text with the left margin
            pdf.cell(available_width, 10, "[Signature Not Available]", align='L', ln=True)
            pdf.ln(20)

        # Underline
        pdf.set_draw_color(0, 0, 0)  # Set color to black
        pdf.set_line_width(0.5)  # Set line width
        underline_x_start = pdf.l_margin
        underline_x_end = pdf.w - pdf.r_margin
        pdf.line(underline_x_start, pdf.get_y(), 80, pdf.get_y())  # Draw a line across the available width

        # Name and designation
        pdf.set_font("Helvetica", "B", 11)  
        pdf.cell(0, 6, data.get('Contact title', ''), ln=True)
        
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, data.get("designation", ""), ln=True)
        
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, "LENOG SDN BHD", ln=True)



# Define a mapping of document types to their respective sections
DOCUMENT_SECTIONS = {
    'ack': [
        AckSection,
        ClarificationSection,
        SignatureSection
    ],
    'cl': [
        CoverLetterSection,
        CoverClarificationSection,
        SignatureSection
    ],
    'scope': [
        ScopeSection,
        CompClarificationSection,
        SignatureSection
    ],
    'toc': [
        ToCSection,
        CompClarificationSection,
        SignatureSection
    ],
    # Add more document types and their sections as needed
}

def generate_pdf(data, document_type=None, sections=None, output_path="ack.pdf"):

    # Use predefined sections if document_type is provided and sections are not
    if document_type and not sections:
        sections = DOCUMENT_SECTIONS.get(document_type)
        if not sections:
            raise ValueError(f"No predefined sections found for document type '{document_type}'.")
    
    # If sections are still not provided, use default sections
    if sections is None:
        sections = [
            AckSection,
            ClarificationSection,
            SignatureSection
        ]
    
    # Initialize PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add header
    pdf.header()
    
    # Add each section
    for section_class in sections:
        try:
            section_method = getattr(section_class, 'add')
            section_method(pdf, data)
        except Exception as e:
            print(f"Error adding section {section_class.__name__}: {e}")
            # Print more detailed error information to help with debugging
            import traceback
            traceback.print_exc()
    
    # Save the PDF
    try:
        pdf.output(output_path)
        print(f"Successfully created PDF: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving PDF to {output_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

# Contact dictionary
CONTACTS = {
    "Dwayne Marshall Labangka": {
        "Contact title": "Dwayne Marshall Labangka",
        "no": "+60 13-8340611",
        "email": "dwayne.ml@lenog.com.my",
        "contact_image_path": "dwayne"
    },
    "Cheok Jia Jun": {
        "Contact title": "Cheok Jia Jun",
        "no": "+60 11-1980 1595",
        "email": "juncheok@lenog.com.my",
        "contact_image_path": "choek"
    },
    "Sao Lip Zhou": {
        "Contact title": "Sao Lip Zhou",
        "no": "+60 12-658 6823",
        "email": "sao.lip.zhou@lenog.com.my",
        "contact_image_path": "sao"
    },
    "Mars Tan Han Yeong": {
        "Contact title": "Mars Tan Han Yeong",
        "no": "+60 17-294 0802",
        "email": "mars@lenog.com.my",
        "contact_image_path": "Mars"
    },
    "Jason Ng": {
        "Contact title": "Jason Ng",
        "no": "+60 13-908 9808",
        "email": "jasonng@lenog.com.my",
        "contact_image_path": "Jason"
    },
   
}

USE_NAS_SIGNATURES = False  # Toggle this to switch between local and NAS paths

def resolve_signature_path(name):
    # If USE_NAS_SIGNATURES is True, use the NAS directory
    if USE_NAS_SIGNATURES:
        base_dir = "Z:\\Technical\\Engineering\\Lenog\\QAQC\\Report\\Signatures"
    else:
        base_dir = resource_path("Signature")  # Local directory
    
    # Try different image formats (.jpg, .png) for the signature
    for ext in [".jpg", ".png"]:
        full_path = os.path.join(base_dir, name + ext)
        if os.path.exists(full_path):  # Check if file exists
            return full_path

    return None  # Return None if no signature image is found


def create_data(reference_no, contract_title, subject, documents, contact_name, designation):
    """Create a data dictionary for the contract with contact information."""
    contact_info = CONTACTS.get(contact_name, {})
    # Get the signature path based on the flag (local or NAS)
    contact_image_path = resolve_signature_path(contact_info.get("contact_image_path", contact_name))
    
    return {
        "REFERENCE NO": reference_no,
        "CONTRACT TITLE": contract_title,
        "SUBJECT": subject,
        "documents": documents,
        "Contact title": contact_info.get("Contact title", contact_name),
        "no": contact_info.get("no", ""),
        "email": contact_info.get("email", ""),
        "contact_image_path": contact_image_path if contact_image_path else "Default/SignatureNotFound.jpg",  # Fallback image if not found
        "designation": designation
    }

# Example usage:
"""
data = create_data(
        reference_no="REF-2025-001", 
        contract_title="Flange Joint Management",
        subject="Proposal for Flange Joint Integrity Work",
        documents=[
            "Cover Letter",
            "Scope of Work",
            "Company Profile",
            "Insurance & Certifications",
        ],
        contact_name="Dwayne Marshall Labangka",
        designation="Project Engineer"
    )  
"""

# Generate all document types
#generate_pdf(data, document_type='ack', output_path="acknowledgement_letter.pdf")
#generate_pdf(data, document_type='cl', output_path="cover_letter.pdf")
#generate_pdf(data, document_type='scope', output_path="scope_letter.pdf")
#generate_pdf(data, document_type='toc', output_path="toc_letter.pdf")    