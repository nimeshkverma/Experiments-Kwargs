import sys

from aadhaar.models import Aadhaar
from activity.models import Activity, CustomerState
from common.models import College, Company, OrganisationType, SalaryPaymentMode
from customer.models import BankDetails, Customer
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from documents.models import DocumentType, Documents
from eligibility.models import AmountEligible, Education, Finance, Profession
from messenger.models import EmailVerification, Otp
from pan.models import Pan
from social.models import LinkedinProfile, Login, SocialProfile


def delete_user_all_data(customer_id):
    model_list = [BankDetails, Otp, EmailVerification, Documents, Aadhaar, Finance, Education, Profession,
                  Pan, AmountEligible, CustomerState, Activity, LinkedinProfile, SocialProfile, Customer, Login]

    for model in model_list:
        try:
            print model.objects.filter(customer_id=customer_id).delete()
        except Exception as e:
            print e


if __name__ == '__main__':

    identifier_type = sys.argv[1]
    identifier = sys.argv[2]

    customer_id = None

    if identifier_type in ['email', 'Email', 'Email_id', 'email_id', 'Email_Id']:
        customer_id = Login.objects.get(email_id=identifier).customer_id
    else:
        customer_id = identifier

    delete_user_all_data(customer_id)
