import requests


def create_test_file(path):
    f = open(path, 'rb')
    return f


def upload_file():
    url = 'http://127.0.0.1:8080/customer/document/'
    file_data = create_test_file('documents/aadhaar_dummy.jpg')
    requests_headers = {
        'Session-Token': 'upwards_1_4EXeIq0Ps79c6ffbHHlJuVoGDPTHT06G'
    }
    requests_data = {
        "customer_id": 1,
        "document_type_id": 1,
        "status": "uploaded",
    }
    requests_files = {
        "document": file_data
    }
    response = requests.post(
        url, headers=requests_headers, files=requests_files, data=requests_data)
    print response
