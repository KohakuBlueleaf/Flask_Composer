from flask import Flask
from flask_composer import Composer


config = [
    {
        'location': '/',
        'proxy_server': 'http://127.0.0.1:17415',
        'no_headers': True,
        'return_header_black_list': {
            'Transfer-Encoding'
        }
    }
]


app = Flask(__name__)
Composer(app, config)


if __name__ == '__main__':
    app.run(debug=False)