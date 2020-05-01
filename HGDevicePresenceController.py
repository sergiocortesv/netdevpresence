"""DHCP Device presence service
   Provides a list of IPs of devices connected to the HG8245 Router
"""
from RouterInfoClient import RouterInfoClient
from flask import Flask, json, render_template
from UserPresenceService import DevicePresenceService

api = Flask(__name__)
devpre = DevicePresenceService()

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
    api.run(host='0.0.0.0')
