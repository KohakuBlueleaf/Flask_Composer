from typing import *

from flask import Flask, Blueprint
from flask import request
from .handler import *


__all__ = [
    'Composer',
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
                    handler = get_static_site_handler(root)
                    if rest.get('before_request', False):
                        @self.app.before_request
                        def before_req_handler():
                            return handler(request.path.lstrip('/'))
                    else:
                        self.app.add_url_rule(
                            f'{loc.rstrip("/")}/',
                            f'static-site{loc}',
                            view_func = handler
                        )
                        self.app.add_url_rule(
                            f'{loc.rstrip("/")}/<path:route>',
                            f'static-site{loc}',
                            view_func = handler
                        )