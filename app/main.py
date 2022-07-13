"""I am the entry point. Register Swagger UI, blueprint, start the app"""

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from app.converter import bp as api_bp
from app.constants import BaseConfig

app = Flask('MenuConverter')

SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    BaseConfig.SWAGGER_URL,
    BaseConfig.API_URL,
    config={
        'app_name': "MenuConverter"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=BaseConfig.SWAGGER_URL)
app.register_blueprint(api_bp, url_prefix='/api')


def main():
    app.run(port=8080)


if __name__ == '__main__':
    main()
