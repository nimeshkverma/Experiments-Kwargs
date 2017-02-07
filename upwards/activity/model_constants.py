from copy import deepcopy

UPWARDS = 'upwards'
CUSTOMER = 'customer'
NBFC = 'nbfc'
ACTOR_CHOICES = (
    (UPWARDS, 'upwards'),
    (CUSTOMER, 'customer'),
    (NBFC, 'nbfc'),
)


SIGN_UP = 'sign_up'
PAN_SUBMIT = 'pan_submit'
PROFESSIONAL_SUBMIT = 'professional_submit'
PROFESSIONAL_EMAIL_VERIFIED = 'professional_email_verified'
EDUCATION_SUBMIT = 'education_submit'
FINANCE_SUBMIT = 'finance_submit'
ELIGIBILITY_SUBMIT = 'eligibility_submit'
ELIGIBILITY_PROCCESSING = 'eligibility_proccessing'
ELIGIBILITY_APPROVED = 'eligibility_approved'
ELIGIBILITY_REJECTED = 'eligibility_rejected'
AADHAAR_SUBMIT = 'aadhaar_submit'
AADHAAR_DETAIL_SUBMIT = 'aadhaar_detail_submit'
PERSONAL_CONTACT_SUBMIT = 'personal_contact_submit'
PERSONAL_EMAIL_VERIFIED = 'personal_email_verified'
DOCUMENT_UPLOAD_SUBMIT = 'document_upload_submit'
KYC_SUBMIT = 'kyc_submit'
KYC_PROCCESSING = 'kyc_proccessing'
KYC_APPROVED = 'kyc_approved'
KYC_REJECTED = 'kyc_rejected'
BANK_DETAIL_SUBMIT = 'bank_detail_submit'
LOAN_AMOUNT_SUBMIT = 'loan_amount_submit'
LOAN_APPLICATION_PROCCESSING = 'loan_application_proccessing'
LOAN_APPLICATION_PROCCESSED = 'loan_application_proccessed'
LOAN_APPLICATION_ERRORED = 'loan_application_errored'


CUSTOMER_ACTIVITY_TYPE_CHOICES = (
    (SIGN_UP, 'sign_up'),
    (PAN_SUBMIT, 'pan_submit'),
    (PROFESSIONAL_SUBMIT, 'professional_submit'),
    (PROFESSIONAL_EMAIL_VERIFIED, 'professional_email_verified'),
    (EDUCATION_SUBMIT, 'education_submit'),
    (FINANCE_SUBMIT, 'finance_submit'),
    (ELIGIBILITY_SUBMIT, 'eligibility_submit'),
    (AADHAAR_SUBMIT, 'aadhaar_submit'),
    (AADHAAR_DETAIL_SUBMIT, 'aadhaar_detail_submit'),
    (PERSONAL_CONTACT_SUBMIT, 'personal_contact_submit'),
    (PERSONAL_EMAIL_VERIFIED, 'personal_email_verified'),
    (DOCUMENT_UPLOAD_SUBMIT, 'document_upload_submit'),
    (KYC_SUBMIT, 'kyc_submit'),
    (BANK_DETAIL_SUBMIT, 'bank_detail_submit'),
    (LOAN_AMOUNT_SUBMIT, 'loan_amount_submit'),
)

UPWARDS_TYPE_CHOICES = (
    (ELIGIBILITY_PROCCESSING, 'eligibility_proccessing'),
    (ELIGIBILITY_APPROVED, 'eligibility_approved'),
    (ELIGIBILITY_REJECTED, 'eligibility_rejected'),
    (KYC_PROCCESSING, 'kyc_proccessing'),
    (KYC_APPROVED, 'kyc_approved'),
    (KYC_REJECTED, 'kyc_rejected'),
    (LOAN_APPLICATION_PROCCESSING, 'loan_application_proccessing'),
    (LOAN_APPLICATION_PROCCESSED, 'loan_application_proccessed'),
    (LOAN_APPLICATION_ERRORED, 'loan_application_errored'),
)

ACTIVITY_TYPE_CHOICES = CUSTOMER_ACTIVITY_TYPE_CHOICES and UPWARDS_TYPE_CHOICES

UNKNOWN_STATE = 'unknown'
SIGN_UP_STATE = 'sign_up'
PAN_SUBMIT_STATE = 'pan_submit'
PROFESSIONAL_SUBMIT_STATE = 'professional_submit'
PROFESSIONAL_EMAIL_UNVERIFIED_STATE = 'professional_email_unverified'
EDUCATION_SUBMIT_STATE = 'education_submit'
FINANCE_SUBMIT_STATE = 'finance_submit'
ELIGIBILITY_SUBMIT_STATE = 'eligibility_submit'
AADHAAR_SUBMIT_STATE = 'aadhaar_submit'
AADHAAR_DETAIL_SUBMIT_STATE = 'aadhaar_detail_submit'
PERSONAL_CONTACT_SUBMIT_STATE = 'personal_contact_submit'
PERSONAL_EMAIL_UNVERIFIED_STATE = 'personal_email_unverified'
DOCUMENT_UPLOAD_SUBMIT_STATE = 'document_upload_submit'
KYC_SUBMIT_STATE = 'kyc_submit'
BANK_DETAIL_SUBMIT_STATE = 'bank_detail_submit'
LOAN_AMOUNT_SUBMIT_STATE = 'loan_amount_submit'
LOAN_APPLICATION_PROCCESSING_STATE = 'loan_application_proccessing'
LOAN_APPLICATION_PROCCESSED_STATE = 'loan_application_proccessed'
LOAN_APPLICATION_ERRORED_STATE = 'loan_application_errored'

CUSTOMER_STATE_CHOICES = (
    (UNKNOWN_STATE, 'unknown'),
    (SIGN_UP_STATE, 'sign_up'),
    (PAN_SUBMIT_STATE, 'pan_submit'),
    (PROFESSIONAL_SUBMIT_STATE, 'professional_submit'),
    (PROFESSIONAL_EMAIL_UNVERIFIED_STATE, 'professional_email_unverified'),
    (EDUCATION_SUBMIT_STATE, 'education_submit'),
    (FINANCE_SUBMIT_STATE, 'finance_submit'),
    (ELIGIBILITY_SUBMIT_STATE, 'eligibility_submit'),
    (AADHAAR_SUBMIT_STATE, 'aadhaar_submit'),
    (AADHAAR_DETAIL_SUBMIT_STATE, 'aadhaar_detail_submit'),
    (PERSONAL_CONTACT_SUBMIT_STATE, 'personal_contact_submit'),
    (PERSONAL_EMAIL_UNVERIFIED_STATE, 'personal_email_unverified'),
    (DOCUMENT_UPLOAD_SUBMIT_STATE, 'document_upload_submit'),
    (KYC_SUBMIT_STATE, 'kyc_submit'),
    (BANK_DETAIL_SUBMIT_STATE, 'bank_detail_submit'),
    (LOAN_AMOUNT_SUBMIT_STATE, 'loan_amount_submit'),
    (LOAN_APPLICATION_PROCCESSING_STATE, 'loan_application_proccessing'),
    (LOAN_APPLICATION_PROCCESSED_STATE, 'loan_application_proccessed'),
    (LOAN_APPLICATION_ERRORED_STATE, 'loan_application_errored'),
)

CUSTOMER_STATE_TREE = {
    UNKNOWN_STATE: {
        'from': [UNKNOWN_STATE],
        'to': [SIGN_UP_STATE]
    },
    SIGN_UP_STATE: {
        'from': [UNKNOWN_STATE],
        'to': [PAN_SUBMIT_STATE]
    },
    PAN_SUBMIT_STATE: {
        'from': [SIGN_UP_STATE],
        'to': [PROFESSIONAL_SUBMIT_STATE]
    },
    PROFESSIONAL_SUBMIT_STATE: {
        'from': [PAN_SUBMIT_STATE],
        'to': [EDUCATION_SUBMIT_STATE]
    },
    EDUCATION_SUBMIT_STATE: {
        'from': [PROFESSIONAL_SUBMIT_STATE],
        'to': [FINANCE_SUBMIT_STATE, PROFESSIONAL_EMAIL_UNVERIFIED_STATE]
    },
    FINANCE_SUBMIT_STATE: {
        'from': [EDUCATION_SUBMIT_STATE, PROFESSIONAL_EMAIL_UNVERIFIED_STATE],
        'to': [ELIGIBILITY_SUBMIT_STATE]
    },
    PROFESSIONAL_EMAIL_UNVERIFIED_STATE: {
        'from': [EDUCATION_SUBMIT_STATE],
        'to': [FINANCE_SUBMIT_STATE]
    },
    ELIGIBILITY_SUBMIT_STATE: {
        'from': [FINANCE_SUBMIT_STATE],
        'to': [AADHAAR_SUBMIT_STATE]
    },
    AADHAAR_SUBMIT_STATE: {
        'from': [ELIGIBILITY_SUBMIT_STATE],
        'to': [AADHAAR_DETAIL_SUBMIT_STATE],
    },
    AADHAAR_DETAIL_SUBMIT_STATE: {
        'from': [AADHAAR_SUBMIT_STATE],
        'to': [PERSONAL_CONTACT_SUBMIT_STATE]
    },
    PERSONAL_CONTACT_SUBMIT_STATE: {
        'from': [AADHAAR_DETAIL_SUBMIT_STATE],
        'to': [DOCUMENT_UPLOAD_SUBMIT_STATE]
    },
    DOCUMENT_UPLOAD_SUBMIT_STATE: {
        'from': [PERSONAL_CONTACT_SUBMIT_STATE],
        'to': [KYC_SUBMIT_STATE, PERSONAL_EMAIL_UNVERIFIED_STATE]
    },
    PERSONAL_EMAIL_UNVERIFIED_STATE: {
        'from': [DOCUMENT_UPLOAD_SUBMIT_STATE],
        'to': [KYC_SUBMIT_STATE]
    },
    KYC_SUBMIT_STATE: {
        'from': [DOCUMENT_UPLOAD_SUBMIT_STATE, PERSONAL_EMAIL_UNVERIFIED_STATE],
        'to': [BANK_DETAIL_SUBMIT_STATE]
    },
    BANK_DETAIL_SUBMIT_STATE: {
        'from': [KYC_SUBMIT_STATE],
        'to': [LOAN_AMOUNT_SUBMIT_STATE]
    },
    LOAN_AMOUNT_SUBMIT_STATE: {
        'from': [BANK_DETAIL_SUBMIT_STATE],
        'to': [LOAN_APPLICATION_PROCCESSING_STATE]
    },
    LOAN_APPLICATION_PROCCESSING_STATE: {
        'from': [LOAN_AMOUNT_SUBMIT_STATE],
        'to': [LOAN_APPLICATION_PROCCESSED_STATE, LOAN_APPLICATION_ERRORED_STATE]
    },
    LOAN_APPLICATION_PROCCESSED_STATE: {
        'from': [LOAN_APPLICATION_PROCCESSING_STATE],
        'to': []
    },
    LOAN_APPLICATION_ERRORED_STATE: {
        'from': [LOAN_APPLICATION_PROCCESSING_STATE],
        'to': []
    },
}


CUSTOMER_STATE_ORDER_LIST = [
    UNKNOWN_STATE,
    SIGN_UP_STATE,
    PAN_SUBMIT_STATE,
    PROFESSIONAL_SUBMIT_STATE,
    EDUCATION_SUBMIT_STATE,
    FINANCE_SUBMIT_STATE,
    PROFESSIONAL_EMAIL_UNVERIFIED_STATE,
    ELIGIBILITY_SUBMIT_STATE,
    AADHAAR_SUBMIT_STATE,
    AADHAAR_DETAIL_SUBMIT_STATE,
    PERSONAL_CONTACT_SUBMIT_STATE,
    DOCUMENT_UPLOAD_SUBMIT_STATE,
    PERSONAL_EMAIL_UNVERIFIED_STATE,
    KYC_SUBMIT_STATE,
    BANK_DETAIL_SUBMIT_STATE,
    LOAN_AMOUNT_SUBMIT_STATE,
    LOAN_APPLICATION_PROCCESSING_STATE,
    LOAN_APPLICATION_PROCCESSED_STATE,
    LOAN_APPLICATION_ERRORED_STATE,
]
