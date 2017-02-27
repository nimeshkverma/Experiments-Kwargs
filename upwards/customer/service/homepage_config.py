ELIGIBILITY_TITLE = "Eligibility & Credit Limit Check"
KYC_TITLE = "KYC & Document Upload"

USER_STATES_WITH_ELIGIBILITY_AMOUNT = [
    'eligibility_result_approved',
    'aadhaar_submit',
    'aadhaar_detail_submit',
    'personal_contact_submit',
    'document_submit_email_unverified',
    'document_submit_email_verified',
    'kyc_submit',
    'kyc_result_approved',
    'kyc_result_rejected',
    'bank_detail_submit',
    'loan_amount_submit',
    'loan_application_proccessing',
    'loan_application_errored',
    'loan_application_proccessed',
]

BORROWER_STATES = [
    'bank_detail_submit',
    'loan_amount_submit',
    'loan_application_proccessing',
    'loan_application_errored',
    'loan_application_proccessed',
]

USER_STATE_MESSAGES = {
    'unknown': {
        'eligibility': {
            'message': 'Please start your application by completing this section',
            'completion_percentage': 0,
        },
        'kyc': {
            'message': 'Please start your application by completing this section',
            'completion_percentage': 0,
        },
    },
    'sign_up': {
        'eligibility': {
            'message': 'Please start your application by completing this section',
            'completion_percentage': 0,
        },
        'kyc': {
            'message': "Please complete the 'Eligibility & Credit Limit Check' section prior to this section",
            'completion_percentage': 0,
        },
    },
    'pan_submit': {
        'eligibility': {
            'message': 'Please provide your employment details to continue',
            'completion_percentage': 20,
        },
        'kyc': {
            'message': "Please complete the 'Eligibility & Credit Limit Check' section prior to this section",
            'completion_percentage': 0,
        },
    },
    'professional_submit': {
        'eligibility': {
            'message': 'Please provide your educational details to continue',
            'completion_percentage': 50,
        },
        'kyc': {
            'message': "Please complete the 'Eligibility & Credit Limit Check' section prior to this section",
            'completion_percentage': 0,
        },
    },
    'education_submit': {
        'eligibility': {
            'message': 'Please complete the last section to finish your eligibility check',
            'completion_percentage': 70,
        },
        'kyc': {
            'message': "Please complete the 'Eligibility & Credit Limit Check' section prior to this section",
            'completion_percentage': 0,
        },
    },
    'finance_submit_email_unverified': {
        'eligibility': {
            'message': "Please verify your 'Company Email' to continue",
            'completion_percentage': 90,
        },
        'kyc': {
            'message': "Please complete the 'Eligibility & Credit Limit Check' section prior to this section",
            'completion_percentage': 0,
        },
    },
    'finance_submit_email_verified': {
        'eligibility': {
            'message': 'Please do a final review of the information to proceed',
            'completion_percentage': 95,
        },
        'kyc': {
            'message': "Please complete the 'Eligibility & Credit Limit Check' section prior to this section",
            'completion_percentage': 0,
        },
    },
    'eligibility_submit': {
        'eligibility': {
            'message': 'Please wait while we process your application',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Please wait for approval/reject decision in the previous section',
            'completion_percentage': 0,
        },
    },
    'eligibility_result_approved': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats, please proceed to the next section',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Please complete your application by filling this section',
            'completion_percentage': 0,
        },
    },
    'eligibility_result_rejected': {
        'eligibility': {
            'message': 'Unfortunately, you are not eligible. Please reapply after sometime or contact us.',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Unfortunately, you are not eligible',
            'completion_percentage': 0,
        },
    },
    'aadhaar_submit': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats, please complete the next section',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Please provide your KYC details to continue',
            'completion_percentage': 20,
        },
    },
    'aadhaar_detail_submit': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats, please complete the next section',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Please provide your personal contact details to continue',
            'completion_percentage': 40,
        },
    },
    'personal_contact_submit': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats, please complete the next section',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'We need some basic documents to finalize your application. Please upload to continue',
            'completion_percentage': 60,
        },
    },
    'document_submit_email_unverified': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats, please complete the next section',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Please verify your personal email to continue',
            'completion_percentage': 90,
        },
    },
    'document_submit_email_verified': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats, please complete the next section',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Please do a final review of the information to proceed',
            'completion_percentage': 95,
        },
    },
    'kyc_submit': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats!',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'All done! Please wait while we verify all details and get back.',
            'completion_percentage': 100,
        },
    },
    'kyc_result_approved': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats!',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': "Bingo, Your KYC verification is done! Please press the 'Get Cash' button at the bottom of the screen to start availing credit",
            'completion_percentage': 100,
        },
    },
    'kyc_result_rejected': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats!',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Unfortunately, we were not able to verify your KYC details. Please reapply later or contact us.',
            'completion_percentage': 100,
        },
    },
    'bank_detail_submit': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats!',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Credit Information will be notified to you, soon!',
            'completion_percentage': 100,
        },
    },
    'loan_amount_submit': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats!',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Credit Information will be notified to you, soon!',
            'completion_percentage': 100,
        },
    },
    'loan_application_proccessing': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats!',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Credit Information will be notified to you, soon!',
            'completion_percentage': 100,
        },
    },
    'loan_application_proccessed': {
        'eligibility': {
            'message': 'Credit Information will be notified to you, soon!',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats!',
            'completion_percentage': 100,
        },
    },
    'loan_application_errored': {
        'eligibility': {
            'message': 'You have been approved for credit limit of Rs {amount}. Congrats!',
            'completion_percentage': 100,
        },
        'kyc': {
            'message': 'Credit Information will be notified to you, soon!',
            'completion_percentage': 100,
        },
    },
}
