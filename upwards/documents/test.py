import requests


def create_test_file(path):
    f = open(path, 'rb')
    return f


def upload_file():
    url = 'http://127.0.0.1:8080/customer/document/'
    # file_data = create_test_file('documents/aadhaar_dummy.jpg')
    requests_headers = {
        'Session-Token': 'upwards_1_wtBjTeMpzVc6v75g92LTVt7jdCu4pCeB'
    }
    requests_data = {
        "customer_id": 1,
        "document_type_id": 1,
        "status": "uploaded",
    }
    requests_files = {
        "document_1": create_test_file('documents/aadhaar_dummy1.jpg'),
        "document_2": create_test_file('documents/aadhaar_dummy2.jpg'),
    }
    response = requests.put(
        url, headers=requests_headers, files=requests_files, data=requests_data)
    print response


def upload_file2():
    url = 'http://127.0.0.1:8080/customer/1/document/'
    requests_headers = {
        'Session-Token': 'upwards_1_wtBjTeMpzVc6v75g92LTVt7jdCu4pCeB'
    }
    requests_data = {
        "customer_id": 1,
        "document_type_id": 1,
        "status": "uploaded",
    }
    requests_files = {
        "document_1": create_test_file('documents/aadhaar_dummy2.jpg'),
        "document_2": create_test_file('documents/aadhaar_dummy1.jpg'),
    }
    response = requests.put(
        url, headers=requests_headers, files=requests_files, data=requests_data)
    print response
