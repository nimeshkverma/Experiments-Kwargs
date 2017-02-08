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
FINANCE_SUBMIT_EMAIL_UNVERIFIED = 'finance_submit_email_unverified'
EDUCATION_SUBMIT = 'education_submit'
FINANCE_SUBMIT_EMAIL_VERIFIED = 'finance_submit_email_verified'
ELIGIBILITY_SUBMIT = 'eligibility_submit'
ELIGIBILITY_RESULT_PROCCESSING = 'eligibility_result_proccessing'
ELIGIBILITY_RESULT_APPROVED = 'eligibility_result_approved'
ELIGIBILITY_RESULT_REJECTED = 'eligibility_result_rejected'
AADHAAR_SUBMIT = 'aadhaar_submit'
AADHAAR_DETAIL_SUBMIT = 'aadhaar_detail_submit'
PERSONAL_CONTACT_SUBMIT = 'personal_contact_submit'
DOCUMENT_SUBMIT_EMAIL_UNVERIFIED = 'document_submit_email_unverified'
DOCUMENT_SUBMIT_EMAIL_VERIFIED = 'document_submit_email_verified'
KYC_SUBMIT = 'kyc_submit'
KYC_RESULT_PROCCESSING = 'kyc_result_proccessing'
KYC_RESULT_APPROVED = 'kyc_result_approved'
KYC_RESULT_REJECTED = 'kyc_result_rejected'
BANK_DETAIL_SUBMIT = 'bank_detail_submit'
LOAN_AMOUNT_SUBMIT = 'loan_amount_submit'
LOAN_APPLICATION_PROCCESSING = 'loan_application_proccessing'
LOAN_APPLICATION_PROCCESSED = 'loan_application_proccessed'
LOAN_APPLICATION_ERRORED = 'loan_application_errored'


CUSTOMER_ACTIVITY_TYPE_CHOICES = (
    (SIGN_UP, 'sign_up'),
    (PAN_SUBMIT, 'pan_submit'),
    (PROFESSIONAL_SUBMIT, 'professional_submit'),
    (FINANCE_SUBMIT_EMAIL_UNVERIFIED, 'finance_submit_email_unverified'),
    (EDUCATION_SUBMIT, 'education_submit'),
    (FINANCE_SUBMIT_EMAIL_VERIFIED, 'finance_submit_email_verified'),
    (ELIGIBILITY_SUBMIT, 'eligibility_submit'),
    (AADHAAR_SUBMIT, 'aadhaar_submit'),
    (AADHAAR_DETAIL_SUBMIT, 'aadhaar_detail_submit'),
    (PERSONAL_CONTACT_SUBMIT, 'personal_contact_submit'),
    (DOCUMENT_SUBMIT_EMAIL_UNVERIFIED, 'document_submit_email_unverified'),
    (DOCUMENT_SUBMIT_EMAIL_VERIFIED, 'document_submit_email_verified'),
    (KYC_SUBMIT, 'kyc_submit'),
    (BANK_DETAIL_SUBMIT, 'bank_detail_submit'),
    (LOAN_AMOUNT_SUBMIT, 'loan_amount_submit'),
)

UPWARDS_TYPE_CHOICES = (
    (ELIGIBILITY_RESULT_PROCCESSING, 'eligibility_result_proccessing'),
    (ELIGIBILITY_RESULT_APPROVED, 'eligibility_result_approved'),
    (ELIGIBILITY_RESULT_REJECTED, 'eligibility_result_rejected'),
    (KYC_RESULT_PROCCESSING, 'kyc_result_proccessing'),
    (KYC_RESULT_APPROVED, 'kyc_result_approved'),
    (KYC_RESULT_REJECTED, 'kyc_rresult_ejected'),
    (LOAN_APPLICATION_PROCCESSING, 'loan_application_proccessing'),
    (LOAN_APPLICATION_PROCCESSED, 'loan_application_proccessed'),
    (LOAN_APPLICATION_ERRORED, 'loan_application_errored'),
)

ACTIVITY_TYPE_CHOICES = CUSTOMER_ACTIVITY_TYPE_CHOICES and UPWARDS_TYPE_CHOICES

UNKNOWN_STATE = 'unknown'
SIGN_UP_STATE = 'sign_up'
PAN_SUBMIT_STATE = 'pan_submit'
PROFESSIONAL_SUBMIT_STATE = 'professional_submit'
FINANCE_SUBMIT_EMAIL_UNVERIFIED_STATE = 'finance_submit_email_unverified'
EDUCATION_SUBMIT_STATE = 'education_submit'
FINANCE_SUBMIT_EMAIL_VERIFIED_STATE = 'finance_submit_email_verified'
ELIGIBILITY_SUBMIT_STATE = 'eligibility_submit'
ELIGIBILITY_RESULT_APPROVED_STATE = 'eligibility_result_approved'
ELIGIBILITY_RESULT_REJECTED_STATE = 'eligibility_result_rejected'
AADHAAR_SUBMIT_STATE = 'aadhaar_submit'
AADHAAR_DETAIL_SUBMIT_STATE = 'aadhaar_detail_submit'
PERSONAL_CONTACT_SUBMIT_STATE = 'personal_contact_submit'
DOCUMENT_SUBMIT_EMAIL_UNVERIFIED_STATE = 'document_submit_email_unverified'
DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE = 'document_submit_email_verified'
KYC_SUBMIT_STATE = 'kyc_submit'
KYC_RESULT_APPROVED_STATE = 'kyc_result_approved'
KYC_RESULT_REJECTED_STATE = 'kyc_result_rejected'
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
    (FINANCE_SUBMIT_EMAIL_UNVERIFIED_STATE, 'finance_submit_email_unverified'),
    (EDUCATION_SUBMIT_STATE, 'education_submit'),
    (FINANCE_SUBMIT_EMAIL_VERIFIED_STATE, 'finance_submit_email_verified'),
    (ELIGIBILITY_SUBMIT_STATE, 'eligibility_submit'),
    (ELIGIBILITY_RESULT_APPROVED_STATE, 'eligibility_result_approved'),
    (ELIGIBILITY_RESULT_REJECTED_STATE, 'eligibility_result_rejected'),
    (AADHAAR_SUBMIT_STATE, 'aadhaar_submit'),
    (AADHAAR_DETAIL_SUBMIT_STATE, 'aadhaar_detail_submit'),
    (PERSONAL_CONTACT_SUBMIT_STATE, 'personal_contact_submit'),
    (DOCUMENT_SUBMIT_EMAIL_UNVERIFIED_STATE, 'document_submit_email_unverified'),
    (DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE, 'document_submit_email_verified'),
    (KYC_SUBMIT_STATE, 'kyc_submit'),
    (KYC_RESULT_APPROVED_STATE, 'kyc_result_approved'),
    (KYC_RESULT_REJECTED_STATE, 'kyc_result_rejected'),
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
        'to': [FINANCE_SUBMIT_EMAIL_VERIFIED_STATE, FINANCE_SUBMIT_EMAIL_UNVERIFIED_STATE]
    },
    FINANCE_SUBMIT_EMAIL_VERIFIED_STATE: {
        'from': [EDUCATION_SUBMIT_STATE, FINANCE_SUBMIT_EMAIL_UNVERIFIED_STATE],
        'to': [ELIGIBILITY_SUBMIT_STATE]
    },
    FINANCE_SUBMIT_EMAIL_UNVERIFIED_STATE: {
        'from': [EDUCATION_SUBMIT_STATE],
        'to': [FINANCE_SUBMIT_EMAIL_VERIFIED_STATE]
    },
    ELIGIBILITY_SUBMIT_STATE: {
        'from': [FINANCE_SUBMIT_EMAIL_VERIFIED_STATE],
        'to': [ELIGIBILITY_RESULT_APPROVED, ELIGIBILITY_RESULT_REJECTED]
    },
    ELIGIBILITY_RESULT_APPROVED_STATE: {
        'from': [ELIGIBILITY_SUBMIT_STATE],
        'to': [AADHAAR_SUBMIT_STATE]
    },
    ELIGIBILITY_RESULT_REJECTED_STATE: {
        'from': [ELIGIBILITY_SUBMIT_STATE],
        'to': [ELIGIBILITY_SUBMIT_STATE]
    },
    AADHAAR_SUBMIT_STATE: {
        'from': [ELIGIBILITY_RESULT_APPROVED_STATE],
        'to': [AADHAAR_DETAIL_SUBMIT_STATE],
    },
    AADHAAR_DETAIL_SUBMIT_STATE: {
        'from': [AADHAAR_SUBMIT_STATE],
        'to': [PERSONAL_CONTACT_SUBMIT_STATE]
    },
    PERSONAL_CONTACT_SUBMIT_STATE: {
        'from': [AADHAAR_DETAIL_SUBMIT_STATE],
        'to': [DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE, DOCUMENT_SUBMIT_EMAIL_UNVERIFIED_STATE]
    },
    DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE: {
        'from': [PERSONAL_CONTACT_SUBMIT_STATE, DOCUMENT_SUBMIT_EMAIL_UNVERIFIED_STATE],
        'to': [KYC_SUBMIT_STATE]
    },
    DOCUMENT_SUBMIT_EMAIL_UNVERIFIED_STATE: {
        'from': [PERSONAL_CONTACT_SUBMIT_STATE],
        'to': [DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE]
    },
    KYC_SUBMIT_STATE: {
        'from': [DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE],
        'to': [KYC_RESULT_APPROVED_STATE, KYC_RESULT_REJECTED_STATE]
    },
    KYC_RESULT_APPROVED_STATE: {
        'from': [KYC_SUBMIT_STATE],
        'to': [BANK_DETAIL_SUBMIT_STATE]
    },
    KYC_RESULT_REJECTED_STATE: {
        'from': [KYC_SUBMIT_STATE],
        'to': [KYC_SUBMIT_STATE]
    },
    BANK_DETAIL_SUBMIT_STATE: {
        'from': [KYC_RESULT_APPROVED_STATE],
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
    FINANCE_SUBMIT_EMAIL_VERIFIED_STATE,
    FINANCE_SUBMIT_EMAIL_UNVERIFIED_STATE,
    ELIGIBILITY_SUBMIT_STATE,
    ELIGIBILITY_RESULT_APPROVED_STATE,
    ELIGIBILITY_RESULT_REJECTED_STATE,
    AADHAAR_SUBMIT_STATE,
    AADHAAR_DETAIL_SUBMIT_STATE,
    PERSONAL_CONTACT_SUBMIT_STATE,
    DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE,
    DOCUMENT_SUBMIT_EMAIL_UNVERIFIED_STATE,
    KYC_SUBMIT_STATE,
    KYC_RESULT_APPROVED_STATE,
    KYC_RESULT_REJECTED_STATE,
    BANK_DETAIL_SUBMIT_STATE,
    LOAN_AMOUNT_SUBMIT_STATE,
    LOAN_APPLICATION_PROCCESSING_STATE,
    LOAN_APPLICATION_PROCCESSED_STATE,
    LOAN_APPLICATION_ERRORED_STATE,
]
