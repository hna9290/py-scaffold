from behave import *

import requests
import json


@given('I have a csv file')
def csv_file_path(context):
    assert context.file_path is not None


@given('I have a uploaded a csv file')
@when('I upload the file')
def upload_file(context):
    with open(context.file_path, 'rb') as f:
        response = requests.post(context.upload_url, data=f).json()
        context.file_id = response["FileId"]
        context.message = response["message"]
    assert response is not None


@then('The uploaded is successful')
def upload_successful_check(context):
    assert context.file_id is not None
    assert context.message == "File uploaded successfully"


@when('I get the converted file')
def convert_file(context):
    context.converted_file = requests.get(context.convert_url(context.file_id)).json()['content']
    assert context.converted_file is not None


@then('The file is successfully converted')
def convert_file_success(context):
    with open(context.json_file_path, 'r') as json_file:
        output = json.loads(json_file.read())
        assert context.converted_file == output


@when('I delete the file')
def delete_file(context):
    status = requests.delete(context.delete_url(context.file_id)).status_code
    assert status == 200


@then('The file is deleted successfully')
def convert_file_success(context):
    status = requests.get(context.convert_url(context.file_id)).status_code
    assert status == 404