from requests import Request, Session
import base64
import json

def pull_table(bimage):
    url = 'http://www.ocrwebservice.com/restservices/processDocument?pagerange=1&getwords=true&outputformat=xls&newline=1'

    auth_string = str(base64.b64encode(b'BRUCEPARK:9ED1D4B6-1257-4D6C-9361-CAE285F7A032'), 'utf-8').replace('\n', '')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + auth_string,
        'Content-Length': str(len(bimage))
    }

    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    s = Session()
    req = Request('POST', url, headers=headers)
    prepped = s.prepare_request(req)
    prepped.body = bimage

    # resp = s.send(prepped, proxies=proxies)
    resp = s.send(prepped)
    d = json.loads(resp.text)

    return d['OutputFileUrl']