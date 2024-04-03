from typing import List, Tuple, Union
from maa.define import RectType
from maa.library import Library
from maa.resource import Resource
from maa.controller import AdbController
from maa.instance import Instance
from maa.toolkit import Toolkit

from maa.custom_recognizer import CustomRecognizer
from maa.custom_action import CustomAction

import os
import asyncio
import time


async def init() -> Instance:
    version = Library.open("bin")
    print(f"MaaFw Version: {version}")

    Toolkit.init_config()

    resource = Resource()
    await resource.load("resource")

    device_list = await Toolkit.adb_devices()
    if not device_list:
        print("No ADB device found.")
        exit()

    controller = await ChooseAdbDevices(device_list)
    await controller.connect()

    maa_inst = Instance()
    maa_inst.bind(resource, controller)

    if not maa_inst.inited:
        print("Failed to init MAA.")
        exit()

    return maa_inst
    # await maa_inst.run_task("Combat")



async def ChooseAdbDevices(devices_list: list) -> AdbController:
    print("Adb 设备列表")
    for i in range(len(devices_list)):
        print(f"{i+1}. {devices_list[i]}")

    device_index=-1
    print("请输入编号；")

    while(device_index not in range(1,len(devices_list)+1)):
        while(True):
            try:
                device_index=int(input())
            except:
                print("输入有误，请重新输入")
            else:
                break

        if device_index not in range(1,len(devices_list)+1):
            print("输入范围有误，请重新输入")

    print(f"成功选择第{device_index}个设备")
    
    return AdbController(
        adb_path=devices_list[device_index-1].adb_path,
        address=devices_list[device_index-1].address,
    )

async def main():

    # 初始化资源
    print("正在初始化...")
    mra_inst=await init()
    print("初始化完毕")
    time.sleep(1)
    os.system("cls")
   
    

if __name__ == "__main__":
    asyncio.run(main())
