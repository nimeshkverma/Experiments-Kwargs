import requests
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.


def create_test_file(path):
    f = open(path, 'rb')
    return f


def upload_file():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    # requests.get('https://httpbin.org/headers')
    url = 'http://ec2-35-163-209-76.us-west-2.compute.amazonaws.com:8000/customer/document/'
    # file_data = create_test_file('documents/aadhaar_dummy.jpg')
    requests_headers = {
        'Session-Token': 'upwards_4_QB9DiMSlukAnwTdFAWJX9O1FHlPqYfhL'
    }
    requests_data = {
        "customer_id": 4,
        "document_type_id": "1",
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
