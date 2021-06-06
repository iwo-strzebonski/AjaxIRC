'''
Flask routing module
'''

import os
import mimetypes
import time
import secrets

import werkzeug
import flask_restful as restful

from flask import send_from_directory, make_response, request
from flask_cors import cross_origin

from app import app

api = restful.Api(app)

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
USERS = []

open(root + '\\..\\data.txt', 'w').write('')


class DataUpdate(restful.Resource):
    @classmethod
    def _is_updated(cls, request_time):
        '''Returns if resource is updated or it's the first time it has been requested

        Args:
            request_time: last request timestamp
        '''
        return os.stat(root + '\\..\\data.txt').st_mtime > request_time

    def get(self):
        '''Returns 'data.txt' content when the resource has changed after the request time
        '''

        request_time = time.time()

        while not self._is_updated(request_time):
            time.sleep(0.5)
        content = ''

        with open(root + '\\..\\data.txt') as data:
            content = data.read()
        return { "content": content }

api.add_resource(DataUpdate, '/data-update')


def add_user(form):
    #pylint: disable=global-statement
    global USERS

    boolean = False

    for i in USERS:
        if i['user'] == form['user']:
            boolean = True
            break

    if boolean:
        color = [ i['color'] for i in USERS if i['user'] == form['user'] ][0]
    else:
        color = (
            str(hex(secrets.randbelow(256))) +
            str(hex(secrets.randbelow(256))) +
            str(hex(secrets.randbelow(256)))
        ).replace('0x', '')

        color = '#' + color + (6 - len(color)) * '0'

        USERS.append({ 'user': form['user'], 'color': color })

    return color


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    '''Routing for main page (GET method)

    Returns:
        text/html: Main page (index.html)
    '''

    return make_response(send_from_directory(root, 'index.html'))


@app.route('/<path:path>', methods=['GET'])
@cross_origin()
def static_proxy(path):
    '''Routing for requested static element (GET method)

    Args:
        path (str): Absolute path to directory containing static files

    Returns:
        res (file <mimetype>): Requested file
    '''

    res = make_response(send_from_directory(root, path))

    return res


@app.route('/send', methods=['POST'])
@cross_origin()
def post():
    '''Routing for POST methods
    '''
    try:
        color = add_user(request.form)

        # pylint: disable=unused-variable
        file = open(root + '\\..\\data.txt', 'a').write(
            '{' + '"time":{},"user":"{}","color":"{}","message":"{}"'.format(
                time.time() * 1000,     # JS używa milisekund, Python używa sekund
                request.form['user'],
                color,
                request.form['message']
            ) + '}\n'
        )
    except werkzeug.exceptions.BadRequestKeyError:
        pass

    return make_response()


@app.route('/quit', methods=['POST'])
@cross_origin()
def quit_chat():
    #pylint: disable=global-statement
    global USERS

    for i, user in enumerate(USERS):
        if user['user'] == request.form['user']:
            del USERS[i]
            break

    return make_response()


@app.route('/color', methods=['POST'])
@cross_origin()
def change_color():
    #pylint: disable=global-statement
    global USERS

    for i, user in enumerate(USERS):
        if user['user'] == request.form['user']:
            USERS[i]['color'] = request.form['color']
            break

    return make_response()


@app.route('/nick', methods=['POST'])
@cross_origin()
def change_nick():
    #pylint: disable=global-statement
    global USERS

    for i, user in enumerate(USERS):
        if user['user'] == request.form['user']:
            USERS[i]['user'] = request.form['new']
            break

    return make_response()
