import sys

from aadhaar.models import Aadhaar
from activity.models import Activity, CustomerState
from common.models import College, Company, OrganisationType, SalaryPaymentMode
from customer.models import BankDetails, Customer
from documents.models import DocumentType, Documents
from eligibility.models import Education, Finance, Profession
from loan.models import Installment, Loan, LoanType
from messenger.models import EmailVerification, Otp
from pan.models import Pan
from participant.models import Borrower, BorrowerType, Lender
from social.models import LinkedinProfile, Login, SocialProfile


def delete_user_all_data(customer_id):
    response = ""
    loan_objects = Loan.objects.filter(customer_id=customer_id)
    for loan_object in loan_objects:
        response += str(Installment.objects.filter(loan_id=loan_object.id).delete())
    model_list = [Loan, Borrower, BankDetails, Otp, EmailVerification, Documents, Aadhaar, Finance, Education, Profession,
                  Pan, CustomerState, Activity, LinkedinProfile, SocialProfile, Customer, Login]
    for model in model_list:
        try:
            response += str(model.objects.filter(customer_id=customer_id).delete())
        except Exception as e:
            print e
    return response


if __name__ == '__main__':

    identifier_type = sys.argv[1]
    identifier = sys.argv[2]

    customer_id = None

    if identifier_type in ['email', 'Email', 'Email_id', 'email_id', 'Email_Id']:
        customer_id = Login.objects.get(email_id=identifier).customer_id
    else:
        customer_id = identifier

    print delete_user_all_data(customer_id)
