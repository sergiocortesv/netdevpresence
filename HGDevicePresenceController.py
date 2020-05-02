"""DHCP Device presence service
   Provides a list of IPs of devices connected to the HG8245 Router
"""
import configparser
from RouterInfoClient import RouterInfoClient
from flask import Flask, json, render_template
from UserPresenceService import DevicePresenceService

config = configparser.ConfigParser(delimiters="=")
config.read("netdevpresence.ini")
rclient = RouterInfoClient(config)
devpre = DevicePresenceService(rclient,config)
api = Flask(__name__)

@api.route('/user_device',methods = ['GET'])
def get_user_devices():
    devices = devpre.get_devices()
    return json.dumps(devices)

@api.route('/user_device_online',methods = ['GET'])
def get_user_devices_online():
    devices = devpre.get_userdevices()
    devices = list(filter(lambda x: x["status"] == "Online",devices))
    return json.dumps(devices)

@api.route('/users_online',methods = ['GET'])
def get_userdevices_online():
    devices = devpre.get_userdevices()
    devices = list(filter(lambda x: x["status"] == "Online", devices))
    devices.sort(key= lambda d: d["userrel"])
    return render_template('users_online.html',users=devices)

if __name__ == '__main__':
    api.run(host=config['DEFAULT']['listenhost'])

