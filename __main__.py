from typing import List, Tuple, Union
from maa.define import RectType
from maa.library import Library
from maa.resource import Resource
from maa.controller import AdbController
from maa.instance import Instance
from maa.toolkit import Toolkit

from maa.custom_recognizer import CustomRecognizer
from maa.custom_action import CustomAction

import asyncio


async def main():
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

    # maa_inst.register_recognizer("MyRec", my_rec)
    # maa_inst.register_action("MyAct", my_act)

    # await maa_inst.run_task("Combat")


""" class MyRecognizer(CustomRecognizer):
    def analyze(
        self, context, image, task_name, custom_param
    ) -> Tuple[bool, RectType, str]:
        return True, (0, 0, 100, 100), "Hello World!" """


""" class MyAction(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        return True

    def stop(self) -> None:
        pass """


# my_rec = MyRecognizer()
# my_act = MyAction()

async def ChooseAdbDevices(devices_list: list) -> AdbController:
    for i in range(len(devices_list)):
        print(f"{i+1}. {devices_list[i]}")

    device_index=-1

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

if __name__ == "__main__":
    asyncio.run(main())
