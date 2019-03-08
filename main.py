from feed import Feed
from feedback import Feedback
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, resp):
        def log_response(status, headers, *args):
            print('Response: {} {}'.format(status, headers))
            return resp(status, headers, *args)

        return self._app(environ, log_response)

app = Flask(__name__, static_folder='static')
api = Api(app)

@app.route('/')
def root():
    return app.send_static_file('index.html')

api.add_resource(Feed, '/feed')
api.add_resource(Feedback, '/feedback')

if __name__ == '__main__':
    print('Starting server')
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run()
