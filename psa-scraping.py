#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup

_config_filename = 'settings.json'

class Nsvdn:


    def __init__(self, domain= "", sub="", type="", status=False, ttl=3600, data="", comment=""):
        self.domain = domain
        self.sub = sub
        self.type = type
        self.status = status
        self.ttl = ttl
        self.data = data
        self.comment = comment
    
    def is_active(self):
        return self.status
    
    def is_cname(self):
        if "CNAME" in self.type:
            return True
        else:
            return False

def load_config(filename):
    """Load config from file

    :param filename: json config file name

    :return: dict of json config
    """
    return json.loads(open(filename).read())


if __name__ == '__main__':

    config = load_config(_config_filename)

    _post_login_url = 'https://{}/login'.format(config['pwdns_site'])
    _request_url = 'https://{}/domain/'.format(config['pwdns_site'])

    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'username': config['pwdns_username'],
        'password': config['pwdns_password']
    }

    with requests.Session() as session:
        r = session.get(_post_login_url)

        if 'csrftoken' in session.cookies:
            csrftoken = session.cookies['csrftoken']
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            csrfToken = soup.find('input',attrs = {'name':'_csrf_token'})['value']
            payload['_csrf_token'] = csrfToken
            print(payload)

        post = session.post(_post_login_url, headers=header, data=payload)
        #print(post)

        ns_list = []

        # Get information of noumea.nc and ville-noumea.nc
        for domain in config['dns_domains']:
            r = session.request("GET", _request_url + domain)
            soup = BeautifulSoup(r.text, 'html.parser')
            dns_table = soup.find('table',attrs = {'id':'tbl_records'})
            rows = list()
            data = []
            for row in dns_table.findAll("tr"):
                cols = row.find_all('td')
                cols = [ ele.text.strip() for ele in cols ]
                data.append([ele for ele in cols if ele])

            print("===> Domain : " + domain + " - number of entries : "+ str(len(data)))
            # create a list of dict {'cname': '', 'sub': ''}
            for elt in data:
                if len(elt) > 0:
                    ns_list.append(Nsvdn(
                        domain=domain,
                        sub=elt[0],
                        type=elt[1],
                        status=elt[2],
                        ttl=int(elt[3]),
                        data=elt[4],
                        comment=elt[5]))
                #if len(elt) > 0:
                #    if "CNAME" in elt[1]: 
                #        entry = {
                #            'sub': elt[0],
                #            'cname': elt[]
                #        }
                #    if elt[4] in "noumea.nc." or elt[4] in []:
                #        print("| {sub: <46} | {type: <6} | {value} | Redirection 301 |".format(sub=elt[0], type=elt[1], value=elt[4]))
        
        # Print CNAME
        import operator
        ns_list.sort(key=operator.attrgetter('data'))
        for ns in ns_list:
            if ns.is_cname():
                print("| {domain: <15} | {sub: <25} | {value: <30} |".format(domain=ns.domain, sub=ns.sub, value=ns.data))
