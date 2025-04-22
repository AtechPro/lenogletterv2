from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        # Add the company header image if it exists
        if os.path.exists('icons/Company Header.jpg'):
            self.image('icons/Company Header.jpg', x=10, y=8, w=190)
        # Set the height of the header
        self.set_y(50)


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
        pdf.set_font("Arial", size=14, style='BU')
        pdf.cell(0, 10, 'COVER LETTER (TECHNICAL PROPOSAL)', align='C', ln=True)
        pdf.ln(10)
        
        # Reference, Contract Title, Subject
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'REFERENCE NO :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("REFERENCE NO", "").upper(), ln=True)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'CONTRACT TITLE :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("CONTRACT TITLE", "").upper(), ln=True)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'SUBJECT :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("SUBJECT", "").upper(), ln=True)

        pdf.ln(10)
        
        # Main body text
        pdf.set_font("Arial", size=12)
        pdf.write(10, "Dear Sir/Madam,\n")
        pdf.write(10, "We would like to thank PETRONAS for the opportunity to quote for the above tender. We are pleased to hereby submit our Technical Proposal for the ")
        
        pdf.set_font("Arial", style="BU", size=12)
        pdf.write(10, data.get("CONTRACT TITLE", "").upper())
        pdf.set_font("Arial", "", 12)  # Reset to normal font

        pdf.write(10, ". We hope our Technical Proposal and capabilities meet your requirement.\n")
        
        # List of documents
        pdf.set_font("Arial", "B", 12)  # Set to Bold
        pdf.write(10, "List of documents:\n")
        pdf.set_font("Arial", "", 12)  # Reset to normal font

        user_documents = data.get("documents", [])
        if not user_documents:
            pdf.write(10, "No documents provided.\n")
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
        pdf.set_font("Arial", size=14, style='BU')
        pdf.cell(0, 10, 'LETTER OF COMPLIANCE TO SCOPE OF WORKS', align='C', ln=True)
        pdf.ln(10)
        
        # Reference, Contract Title, Subject
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'REFERENCE NO :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("REFERENCE NO", "").upper(), ln=True)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'CONTRACT TITLE :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("CONTRACT TITLE", "").upper(), ln=True)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'SUBJECT :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("SUBJECT", "").upper(), ln=True)

        pdf.ln(10)
        
        # Main body text
        pdf.set_font("Arial", size=12)
        pdf.write(10, "Dear Sir/Madam,\n")
        pdf.write(10, "We are writing in response to the ")
        
        pdf.set_font("Arial", style="BU", size=12)
        pdf.write(10, data.get("REFERENCE NO", "").upper())
        pdf.set_font("Arial", "", 12)  # Reset to normal font

        pdf.write(10, " for ")

        pdf.set_font("Arial", style="BU", size=12)
        pdf.write(10, data.get("CONTRACT TITLE", "").upper())
        pdf.set_font("Arial", "", 12)  # Reset to normal font

        pdf.write(10, " After a thorough review of the documents, we are pleased to submit our letter of compliance with the scope of work outlined in the ATTACHMENT A - SCOPE OF WORKS.\n")
        pdf.write(10, "We would like to confirm our understanding of the requirements and specifications detailed in the tender documentation. Our team has carefully reviewed each section of Scope of Work, and we are fully committed to meet and comply with all the stipulated requirements, scopes, terms and conditions.\n")
        pdf.ln(2)

class ToCSection:
    @staticmethod
    def add(pdf, data):
        """Add the cover letter section to the PDF"""
        pdf.set_y(40)
        
        # Title
        pdf.set_font("Arial", size=14, style='BU')
        pdf.cell(0, 10, 'LETTER OF COMPLIANCE TO TERMS & CONDITIONS', align='C', ln=True)
        pdf.ln(10)
        
        # Reference, Contract Title, Subject
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'REFERENCE NO :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("REFERENCE NO", "").upper(), ln=True)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'CONTRACT TITLE :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("CONTRACT TITLE", "").upper(), ln=True)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'SUBJECT :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("SUBJECT", "").upper(), ln=True)

        pdf.ln(10)
        
        # Main body text
        pdf.set_font("Arial", size=12)
        pdf.write(10, "Dear Sir/Madam,\n")
        pdf.write(10, "We are writing in response to the ")
        
        pdf.set_font("Arial", style="BU", size=12)
        pdf.write(10, data.get("REFERENCE NO", "").upper())
        pdf.set_font("Arial", "", 12)  # Reset to normal font

        pdf.write(10, " for ")

        pdf.set_font("Arial", style="BU", size=12)
        pdf.write(10, data.get("CONTRACT TITLE", "").upper())
        pdf.set_font("Arial", "", 12)  # Reset to normal font

        pdf.write(10, " After a thorough review of the documents, we are pleased to submit our letter of compliance with the terms & conditions outlined in the Terms & Conditions.\n")
        pdf.write(10, "We would like to confirm our understanding of the requirements and specifications detailed in the tender documentation. Our team has carefully reviewed each section of Terms & Conditions, and we are fully committed to meet and comply with all the stipulated requirements, terms and conditions.\n")
        pdf.ln(5)

class AckSection:
    @staticmethod
    def add(pdf, data):
        """Add the cover letter section to the PDF"""
        pdf.set_y(40)
        
        # Title
        pdf.set_font("Arial", size=14, style='BU')
        pdf.cell(0, 10, 'LETTER OF ACKNOWLEDGEMENT TO EXHIBIT V', align='C', ln=True)
        pdf.ln(10)
        
        # Reference, Contract Title, Subject
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'REFERENCE NO :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("REFERENCE NO", "").upper(), ln=True)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'CONTRACT TITLE :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("CONTRACT TITLE", "").upper(), ln=True)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(60, 10, 'SUBJECT :')
        pdf.set_font("Arial", size=12, style='BU')
        pdf.cell(0, 10, data.get("SUBJECT", "").upper(), ln=True)

        pdf.ln(10)
        
        # Main body text
        pdf.set_font("Arial", size=12)
        pdf.write(10, "Dear Sir/Madam,\n")
        pdf.write(10, "We are writing this letter to acknowledge that we have read and understood the ")
        pdf.set_font("Arial", style="B", size=12)
        pdf.write(10, "EXHIBIT V - HEALTH, SAFETY AND ENVIRONMENT REQUIREMENTS")
        pdf.write(10, " for ")
        pdf.set_font("Arial", style="BU", size=12)
        pdf.write(10, data.get("REFERENCE NO", "").upper())
        pdf.write(10, " ")
        pdf.set_font("Arial", style="BU", size=12)
        pdf.write(10, data.get("CONTRACT TITLE", "").upper())
        pdf.set_font("Arial", "", 12)  # Reset to normal font
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
        pdf.multi_cell(0, 10, contact_info)


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
        pdf.multi_cell(0, 10, contact_info)


class SignatureSection:
    @staticmethod
    def add(pdf, data):
        """Add the signature section to the PDF"""
        # Thank you message
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, "Thank you and best regards,", align='L', ln=True)
        # Signature image
        contact_image = data.get('contact_image_path', '')
        if contact_image and os.path.exists(contact_image):
            SIGNATURE_WIDTH = 60
            SIGNATURE_HEIGHT = 20
            
            signature_x = 10
            signature_y = pdf.y
            
            pdf.image(
                contact_image, 
                x=signature_x, 
                y=signature_y, 
                w=SIGNATURE_WIDTH,
                h=SIGNATURE_HEIGHT
            )
            
            pdf.ln(SIGNATURE_HEIGHT + 5)
        else:
            pdf.cell(0, 10, "[Signature Not Available]", ln=True)
            pdf.ln(20)
        
        # Underline
        pdf.set_draw_color(0, 0, 0)  # Set color to black
        pdf.set_line_width(0.5)  # Set line width
        pdf.line(10, pdf.y, 70, pdf.y)  # Draw a line with predefined width of 60
        # Name and designation
        pdf.set_font("Arial", "B", 12)  
        pdf.cell(0, 6, data.get('Contact title', ''), ln=True)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 6, data.get("designation", ""), ln=True)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 6, "LENOG SDN BHD", ln=True)


def generate_pdf(data):
    """Generate a PDF document for a technical proposal based on the provided data."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # CV
    #CoverLetterSection.add(pdf, data)
    #ClarificationSection.add(pdf, data)


    # Scope of Work
    #ScopeSection.add(pdf, data)
    #CompClarificationSection.add(pdf, data)
    #

    # ToC
    #ToCSection.add(pdf, data)
    #CompClarificationSection.add(pdf, data)
    
    # Ack
    AckSection.add(pdf, data)
    ClarificationSection.add(pdf, data)


    SignatureSection.add(pdf, data)
    
    # Save the PDF
    pdf.output("ack.pdf")


# Example usage
data = {
    "REFERENCE NO": "REF-12345",
    "CONTRACT TITLE": "contract with something with something",
    "SUBJECT": "Technical Proposal for Exploration Services",
    "documents": [
        'Cover letter for technical proposal',
        'Exhibit I (Scope of Work)',
        'Exhibit III (Unpriced schedule of rates)',
        'HSE Documents',
        'Key Personnel CV / Resume',
        'Company Experience',
        'Letter of compliance to Scope of Work',
        'Letter of compliance to Terms and Condition of Contracts',
        'Agency Letter', 
        'Company Profile',
        'Company Organization Chart',
        'Company Registration Certificate',
    ],
    "Contact title": "Dwayne Marshall Labangka",
    "no": "+60 12-3456789",
    "email": "dwayne.marshall@company.com",
    "contact_image_path": "Signature/Dwayne Marshall Labangka.jpg",
    "signature_width": 40,
    "designation": "Project Manager"
}



# Generate PDF with user-provided data
generate_pdf(data)