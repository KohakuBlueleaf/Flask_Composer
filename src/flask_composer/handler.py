from typing import *

import os

from flask import Flask, Response
from flask import make_response, send_file


__all__ = [
    'get_static_site_handler',
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
        route_path = dir_path[root_len:].strip('/')
        for file in f_list:
            f_route = os.path.join(route_path, file)
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