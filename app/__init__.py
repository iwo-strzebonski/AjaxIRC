from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
config = {
    'DEBUG': True,
    'CORS_HEADERS': 'Content-Type'
}

app.config.from_mapping(config)

# pylint: disable=wrong-import-position
from app import routes
