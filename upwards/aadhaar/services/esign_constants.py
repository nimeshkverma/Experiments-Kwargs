from django.conf import settings

PDF_URL = "http://localhost:" + settings.BASE_PORT + \
    "/customer/{customer_id}/loan_agreement/"

UNSIGNED_PDF_PATH = "pdfs/customer_{customer_id}/customer_{customer_id}_unsigned_loan_agreement.pdf"
SIGNED_PDF_PATH = "pdfs/customer_{customer_id}/customer_{customer_id}_signed_loan_agreement.pdf"

PDF_DIRECTORY = "pdfs/customer_{customer_id}"
SIGN_DOCUMENT_COMMANDS = {
    "new_directory": "mkdir " + PDF_DIRECTORY,
    "make_unsigned_pdf": "wkhtmltopdf --zoom " + str(settings.PDF_CONVERSION['zoom']) + " " + PDF_URL + " " + UNSIGNED_PDF_PATH,
    "delete_directory": "rm -rf " + PDF_DIRECTORY,
}

UNSIGNED_PDF_NAME = "customer_{customer_id}_unsigned_loan_agreement.pdf"
