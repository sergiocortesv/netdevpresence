import requests
import re
from collections import OrderedDict

class RouterInfoClient:
    """Router admin web interface client"""
    RAND_COUNT_END = "/asp/GetRandCount.asp"
    LOGIN_END = "/login.cgi"
    LANUSER_END = "/html/bbsp/common/GetLanUserDevInfo.asp"

    def __init__(self,config):
        self.service_host_url = config['DEFAULT']['servicehost']
        self.routerusername = config['DEFAULT']['routerusername']
        self.routerpassword = config['DEFAULT']['routerpassword']

    def get_rand_count(self):
        rand_req = requests.post(url = self.service_host_url + self.RAND_COUNT_END,data={})
        if rand_req.status_code == requests.codes.ok and len(rand_req.text) > 10:
            return rand_req.text[3:]

    def login(self):
        rand = self.get_rand_count()
        loginform = OrderedDict([('UserName', self.routerusername),
                                 ('PassWord', self.routerpassword),
                                 ('x.X_HW_Token', str(rand))])
        login_headers = {"Referer": self.service_host_url+ "/",
                         "Cookie": "Cookie=body:Language:english:id=-1"}
        login_req = requests.post(url=self.service_host_url + self.LOGIN_END, data=loginform, headers=login_headers)
        if login_req.status_code == requests.codes.ok:
            return login_req.headers["Set-cookie"]

    def get_lanuser_info(self):
        sec_cookie = self.login()
        lanuser_headers = {"cookie": sec_cookie}
        lan_req = requests.post(url=self.service_host_url + self.LANUSER_END,headers = lanuser_headers)
        if lan_req.status_code == requests.codes.ok:
            return re.findall(r'new USERDevice.*null', lan_req.text)


