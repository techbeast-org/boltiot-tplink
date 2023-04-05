import asyncio
import requests
import json
import os
from kasa import Discover
from kasa import SmartBulb
from kasa import SmartPlug
from kasa import SmartDevice

AK = os.getenv("AK")

async def list_devices():
    kasa_devices = await Discover.discover()
    kasa_list = []
    for ip in kasa_devices:
        dev = SmartDevice(ip)
        await dev.update()
        kasa_list.append(ip+":"+dev.alias)
    print(kasa_list)

async def get_light_value():
        url = "https://cloud.boltiot.com/remote/"+AK+"/analogRead?deviceName=BOLT925658&pin=A0"
        response = requests.request("GET", url)
        response = response.text
        light = json.loads(response)
        light = int(light["value"])
        return light

async def ldr_control():
    # while True:
        b = SmartBulb("192.168.1.46")
        await b.update()  # Request the update
        print(b.alias)  # Print out the alias
        print(b.emeter_realtime)  # Print out current emeter status
        light = await get_light_value()
        if light > 300:
            print("light is "+str(light))
            await b.turn_off()  # Turn the device off
        elif light >150 & light <300 :
             print("light is "+str(light))
             await b.set_brightness(15)
        elif light <150 & light > 80:
            print("light is "+str(light))
            await b.set_brightness(20)
        elif light < 80:
            print("light is "+str(light))
            await b.set_brightness(50)
#         # asyncio.sleep(2)
# async def normal_control():
#     b = SmartBulb("192.168.1.46")
#     await b.update()
#     print(b.alias)
#     await b.turn_off()

if __name__ == "__main__":
    asyncio.run(ldr_control())
