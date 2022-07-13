"""Helper methods which serves various routes. Makes unit tests easy to write"""

import uuid
from collections import defaultdict
from hashlib import md5
from typing import DefaultDict, Tuple, Dict, BinaryIO

from app.converter.converter import convert
from app.converter.logger import log_info
from app.converter.model import UploadedFiles

_files: DefaultDict[str, UploadedFiles] = defaultdict(UploadedFiles)


@log_info
def create_file(file_stream: BinaryIO) -> Tuple[Dict[str, str], int]:
    """
    Helper method to create file in memory.
    :param file_stream: Contents of file to be converted
    :returns Tuple with status code
    """
    try:
        chunk_size: int = 4096
        file_contents: str = ""
        while True:
            chunk = file_stream.read(chunk_size).decode('utf-8')
            if not chunk:
                break
            file_contents = file_contents + chunk
        converted_content = convert(file_contents)
        file_id: str = str(uuid.uuid4())
        _files[file_id].content = file_contents
        _files[file_id].hash = md5(file_contents.encode()).hexdigest()
        _files[file_id].converted_content = converted_content
        return {'message': 'File uploaded successfully',
                'FileId': file_id}, 201
    except TypeError:
        return {'message': 'Uploaded File format is incorrect. Only CSV accepted'}, 400


@log_info
def get_converted_file(file_id: str) -> Tuple[Dict[str, str], int]:
    """
   Helper method to return with converted file content of the requested file id.
   :param file_id: file whose contents to be returned
   :returns Tuple with status code
   """
    file = _files.get(file_id)
    if file:
        return {'content': file.converted_content}, 200
    return {'message': 'File not found. Please check'}, 404


@log_info
def delete_file(file_id: str) -> Tuple[Dict[str, str], int]:
    """
   Helper method to delete file with given file id.
   :param file_id: file to be deleted
   :returns Tuple with status code
   """
    if _files.get(file_id):
        _files.pop(file_id)
    return {'message': 'Deleted Successfully'}, 200
