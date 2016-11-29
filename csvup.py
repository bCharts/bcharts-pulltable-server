from requests import Request, Session
import urllib


def uploade_csv(csv):
    enc_redirect_uri = urllib.parse.quote_plus('https://beta.bcharts.xyz/chartdesigner', safe='', encoding=None, errors=None)
    enc_csv = urllib.parse.quote_plus(csv, safe='', encoding=None, errors=None)
    body = 'redirect_uri=' + enc_redirect_uri + '&payload=' + enc_csv + '&redirect_type=redirect'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(body))
    }

    bcharts_url = 'https://i.beta.bcharts.xyz/integrations/requests/upload/csv'

    s = Session()
    req = Request('POST', bcharts_url, headers=headers)
    prepped = s.prepare_request(req)
    prepped.body = body

    proxies = {
      'http': 'http://127.0.0.1:8080',
      'https': 'http://127.0.0.1:8080'
    }

    # resp = s.send(prepped, proxies=proxies, verify=False, allow_redirects=False)
    resp = s.send(prepped, verify=False, allow_redirects=False)
    first_q = resp.text.index('"')
    seconde_q = resp.text.index('"', first_q + 1)
    redirect_url = resp.text[first_q+1:seconde_q]
    if redirect_url[0:4] != 'http':
        return 'error', ''

    return 'ok', redirect_url