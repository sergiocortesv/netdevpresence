from RouterInfoClient import RouterInfoClient
import re

class DevicePresenceService:
    """Parses lanuserinfo from router"""

    def __init__(self,routerclient,config):
        self.rclient = routerclient
        self.config = config

    def get_devices(self):
        lanuser_str = self.rclient.get_lanuser_info()
        user_devices = re.split(r'new USERDevice', lanuser_str[0])
        user_devices_list = []
        for usr_dev in user_devices:
            if usr_dev != "":
                devmap = self.build_devmap(usr_dev)
                user_devices_list.append(devmap)
        return user_devices_list

    def get_userdevices(self):
        devices = self.get_devices()
        for device in devices:
            device["userrel"] = ""
            if device["macaddress"] in self.config['DEVICEREL']:
                device["userrel"] = self.config['DEVICEREL'][device["macaddress"]]
        return devices

    def build_devmap(self,userdevstr):
        userdevstr = userdevstr.replace("\\x2e",".").replace("\\x3a",":").replace("\\x2d","-")
        usrdev_comps = re.split(r',', userdevstr)
        device = {}
        device["ipaddress"] = re.sub(r"\"","",usrdev_comps[1])
        device["macaddress"] = re.sub(r"\"","",usrdev_comps[2])
        device["so"] = re.sub(r"\"","",usrdev_comps[5])
        device["status"] = re.sub(r"\"","",usrdev_comps[6])
        device["link"] = re.sub(r"\"","",usrdev_comps[7])
        device["name"] = re.sub(r"\"","",usrdev_comps[9])
        return device