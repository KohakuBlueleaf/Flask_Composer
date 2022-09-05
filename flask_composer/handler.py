from typing import *

import os

import requests

from flask import Flask, Response, request
from flask import make_response, send_file

from .utils import *


__all__ = [
    'get_static_site_handler',
    'get_reverse_proxy_handler'
]


def get_static_site_handler(
    root: str
) -> Callable[[str], Response]:
    root = os.path.expanduser(root)
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        raise ValueError('"root" option should be a path to a dir!')
    root_len = len(root)
    
    # use preloaded route_table to prevent some attack like:
    # GET /static-site/../../../../etc/ssh/ssh_host_ed25519_key
    route_table = {}
    for dir_path, _, f_list in os.walk(root):
        route_path = dir_path[root_len:].replace('\\','/').strip('/')
        for file in f_list:
            f_route = os.path.join(route_path, file).replace('\\','/')
            f_path = os.path.join(dir_path, file)
            route_table[f_route] = f_path
            
            if file in ('index.html', 'index.htm'):
                # for index file like /aaa/bbbb/index.html
                # add /aaa/bbbb/ and /aaa/bbbb as valid route for it
                route_table[route_path+'/'] = f_path
                route_table[route_path] = f_path
    
    def handler(route='') -> Response:
        if route in route_table:
            return send_file(route_table[route])
        return make_response("Object doesn't exist", 404)
    
    return handler


def get_reverse_proxy_handler(
    loc: str,
    proxy_server: str,
    ignore_loc: bool = False,
):
    print(loc, proxy_server)
    def handler(route='') -> Response:
        rq_headers, body = parse_flask_Request(request)
        if ignore_loc:
            url = os.path.join(
                proxy_server,
                route,
            ).replace('\\','/')
        else:
            url = os.path.join(
                proxy_server,
                loc.lstrip('/'),
                route,
            ).replace('\\','/')
        
        resp = requests.request(
            request.method.lower(),
            url,
            headers = rq_headers,
            data = body
        )
        status, headers, body = parse_rq_response(resp)
        return Response(body, status, headers)
    
    return handler


if __name__ == '__main__':
    handler = get_static_site_handler(
        '~/web/pixelart-generator/frontend/dist/'
    )
    
    app = Flask(__name__)
    app.add_url_rule(
        '/',
        'static_site',
        handler
    )
    app.add_url_rule(
        '/<path:route>',
        'static_site',
        handler
    )
    app.run()