from functools import partial
import os

def _construct_url(*args):
    url: str = "/".join(args)
    return url


def before_all(context):
    context.file_path = "features/data/data.csv"
    context.json_file_path = "features/data/data.json"
    context.base_url = f"http://{os.getenv('DOCKER_IP', '0.0.0.0')}:8087"
    context.upload_url = _construct_url(context.base_url, 'api/upload')
    context.convert_url = partial(_construct_url,context.base_url, 'api/convert')
    context.delete_url = partial(_construct_url,context.base_url, 'api/delete')


