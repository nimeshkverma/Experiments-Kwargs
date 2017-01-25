from django.conf import settings

config_data = {
    "USER_STATE": {
        "KYC": {
            "personal": 75,
            "not_started": 0,
            "AADHAR": 25,
            "AADHAR_details": 50,
            "uploads": 100
        },
        "eligiblity": {
            "professional": 50,
            "not_started": 0,
            "education": 75,
            "miscellaneous": 100,
            "PAN": 25
        }
    },
    "BASE_URL": settings.BASE_URL
}
