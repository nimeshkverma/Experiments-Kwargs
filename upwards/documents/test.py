import requests


def create_test_file(path):
    f = open(path, 'rb')
    return f


def upload_file():
    url = 'http://127.0.0.1:8080/customer/document/'
    requests_headers = {
        'Session-Token': 'upwards_1_PtLdxI8bXc0yGrhh5obPOtape329YlqO'
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
    response = requests.post(
        url, headers=requests_headers, files=requests_files, data=requests_data)
    print response
    return response


def update_file():
    url = 'http://127.0.0.1:8080/customer/1/document/'
    requests_headers = {
        'Session-Token': 'upwards_1_PtLdxI8bXc0yGrhh5obPOtape329YlqO'
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
    return response


def delete_filte():
    url = 'http://127.0.0.1:8080/customer/1/document/'
    requests_headers = {
        'Session-Token': 'upwards_1_PtLdxI8bXc0yGrhh5obPOtape329YlqO'
    }
    requests_data = {
        "document_type_id": 1,
    }
    response = requests.delete(
        url, headers=requests_headers, data=requests_data)
    print response
    return response
