from flask import Flask,request
from httplib2 import Http
from json import dumps, loads
from logging.config import dictConfig
import os, pprint, traceback

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
chat_url = os.environ.get('GCHAT_URL')


@app.route('/alerts', methods=['POST'])
def index():
    try:
        if request.method == 'POST':
            post_data = request.get_json()
            send_to_chat(post_data)
    except Exception as e:
        app.logger.info(traceback.print_exc())
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
    # app.logger.warn(data['alerts'])
    for alert in data['alerts']:
        message = ''
        if 'description' in alert['annotations'].keys():
            message = alert['annotations']['description']
        else:
            message = alert['annotations']['message']
        status = alert['status']
        cluster = alert['labels']['cluster']
        msg = "*{}*: {} on {}".format(status, message, cluster)
        app.logger.warn("omg: " + msg)
        chat_message = {
            'text': msg
        }
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
            uri=chat_url,
            method='POST',
            headers=headers,
            body=dumps(chat_message),
        )
    
if __name__ == "__main__":
    app.run()
