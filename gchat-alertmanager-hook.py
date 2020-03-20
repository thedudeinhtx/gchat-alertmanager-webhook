from flask import Flask,request
from httplib2 import Http
from json import dumps
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
chat_url = 'https://chat.googleapis.com/v1/spaces/AAAA_BVY_zc/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=QYS1zOYHCPqDlOVQvrX_CE1smTYurXYvUe3X2Ba8-pE%3D&thread_key=alertthread'


@app.route('/alerts', methods=['POST'])
def index():
    try:
        if request.method == 'POST':
            post_data = request.get_json()
            send_to_chat(post_data)
    except Exception as e:
        app.logger.info(e)
        return "Error", 500
    return "OK", 200


def send_to_chat(data):
    # message = {
    #     'text': "Test message"
    # }
    # headers = {'Content-Type': 'application/json; charset=UTF-8'}
    # http_obj = Http()
    # response = http_obj.request(
    #     uri=chat_url,
    #     method='POST',
    #     headers=headers,
    #     body=dumps(message),
    # )
    # app.logger.info(response)
    app.logger.info(data)

if __name__ == "__main__":
    app.run()
