from typing import *

from flask import Flask, Blueprint
from flask import request
from .handler import *
from .handler import get_reverse_proxy_handler


__all__ = [
    'Composer',
]
HTTP_METHODS = [
    'GET', 
    'HEAD', 
    'POST', 
    'PUT', 
    'DELETE', 
    'CONNECT', 
    'OPTIONS', 
    'TRACE', 
    'PATCH'
]


class Composer:
    app: Flask
    config: list[dict[str, Any]]
    
    def __init__(
        self, 
        app: Flask,
        config: list[dict[str, Any]],
    ):
        self.init_app(app, config)
    
    def init_app(
        self, 
        app: Flask, 
        config: list[dict[str, Any]],
    ):
        self.app = app
        self.config = config
        
        self.app.extensions['composer'] = self
        
        for sub_config in config:
            match sub_config:
                case {
                    'location': str() as loc, 
                    'blueprint': Blueprint() as bp,
                    **rest,
                }:
                    # register blueprint
                    bp.url_prefix = loc
                    self.app.register_blueprint(bp)
                
                case {
                    'location': str() as loc, 
                    'root': str() as root,
                    **rest
                }:
                    #static site handling
                    handler = get_static_site_handler(root, **rest)
                    if rest.get('before_request', False):
                        @self.app.before_request
                        def before_req_handler():
                            return handler(request.path.lstrip('/'))
                    else:
                        for rule in (loc, f'{loc}/', f'{loc}/<path:route>'):
                            self.app.add_url_rule(
                                rule,
                                f'static-site{loc}',
                                view_func = handler
                            )
                
                case {
                    'location': str() as loc,
                    'proxy_server': str() as proxy,
                    **rest
                }:
                    handler = get_reverse_proxy_handler(
                        loc, proxy,
                        **rest
                    )
                    loc = loc.rstrip('/')
                    if 'methods' in rest:
                        methods = rest['methods']
                    else:
                        methods = HTTP_METHODS
                    
                    for rule in (loc, f'{loc}/', f'{loc}/<path:route>'):
                        if rule:
                            print(rule)
                            self.app.add_url_rule(
                                rule,
                                f'reverse-proxy{loc}',
                                view_func = handler,
                                methods = methods
                            )