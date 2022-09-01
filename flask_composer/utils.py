import requests as rq
import flask


EXCLUDE_HEADERS = {
    'content-length',
    'content-encoding',
    'transfer-encoding',
    'connection'
}


def parse_flask_Request(
    rq: flask.Request
) -> tuple[dict[str, str], bytes]:
    rq_body = rq.get_data()
    headers = {
        k: v
        for k, v in rq.headers.items()
    }
    return headers, rq_body


def parse_rq_response(
    resp: rq.Response
) -> tuple[int, list[tuple[str, str]], bytes]:
    headers = [
        (k, resp.headers[k])
        for k in resp.headers
        if k not in EXCLUDE_HEADERS
    ]
    content = resp.content
    return resp.status_code, headers, content