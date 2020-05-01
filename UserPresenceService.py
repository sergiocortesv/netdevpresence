from RouterInfoClient import RouterInfoClient
import re

class DevicePresenceService:
    """Parses lanuserinfo from router"""

    def get_devices(self):
        rclient = RouterInfoClient()
        loginCookie = rclient.login("","")
        lanuser_str = rclient.get_lanuser_info(loginCookie)
        user_devices = re.split(r'new USERDevice', lanuser_str[0])
        user_devices_list = []
        for usr_dev in user_devices:
            if usr_dev != "":
                devmap = self.build_devmap(usr_dev)
                print(devmap)
                user_devices_list.append(devmap)
        return user_devices_list

    def get_userdevices(self):
        devices = self.get_devices()
        userdev_rel = self.load_userdev_rel()
        print(type(userdev_rel))
        for device in devices:
            if device["macaddress"] in userdev_rel:
                device["userrel"] = userdev_rel[device["macaddress"]]
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

    def load_userdev_rel(self):
        userdev_rel = {}
        with open("userdevice_rel.dat") as userdev_file:
            for userdev_line in userdev_file:
                (key, val) = userdev_line.split("=")
                userdev_rel[key] = val
        return userdev_rel
