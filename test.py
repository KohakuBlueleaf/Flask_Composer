from flask import Flask
from flask_composer import Composer


config = [
    {
        'location': '/',
        'root': '~/web/pixelart-generator/frontend/dist/',
        'before_request': True,
    }
]

app = Flask(__name__)
Composer(app, config)


if __name__ == '__main__':
    app.run(debug=False)