"""Constants file. Each environment constants can extend BaseConfig class"""


class BaseConfig:
    LEVEL = "Level "
    LEVEL_ID = " - ID"
    NAME = " - Name"
    URL = " - URL"
    LEVEL_REGEX = "[0-9]+"
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    LOGGING_LEVEL = "INFO"
