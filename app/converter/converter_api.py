"""All the API endpoints are here"""

from flask import request

from app.converter import bp
from app.converter.helpers import create_file, get_converted_file, delete_file


@bp.route('/ping', methods=['GET'])
def ping():
    """Health checks of Service"""
    return {'message': 'Healthy'}


@bp.route('/upload', methods=['POST'])
def upload():
    """Gets file from request stream. Stores the contents in memory and converts it."""
    return create_file(request.stream)


@bp.route('/convert/<file_id>', methods=['GET'])
def send_converted_file(file_id: str):
    """Responds with converted file content of the requested file id"""
    return get_converted_file(file_id)


@bp.route('/delete/<file_id>', methods=['DELETE'])
def delete(file_id: str):
    """deletes the file based on file id"""
    return delete_file(file_id)
