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
import json


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

async def LoadJson() -> list:
    with open("./resource/interface.json","r",encoding='utf-8') as f:
        Interface=json.load(f)
        
    return Interface

async def GetTaskList(Inter_dict: list) -> list:
    Task_list=dict()
    for tasks in Inter_dict['task']:
        Task_list[tasks['name']]=tasks['entry']

    return Task_list

async def ChooseTask(Task_dict: dict) -> str :
    task_list=list(Task_dict.keys())

    print("任务列表")
    for i in range(len(task_list)):
        print(f"{i+1}. {task_list[i]}")

    task_index=-1
    print("请输入编号；")

    while(task_index not in range(1,len(task_list)+1)):
        while(True):
            try:
                task_index=int(input())
            except:
                print("输入有误，请重新输入")
            else:
                break

        if task_index not in range(1,len(task_list)+1):
            print("输入范围有误，请重新输入")

    print(f"成功选择第{task_index}个任务: {task_list[task_index-1]}")

    return Task_dict[task_list[task_index-1]]

async def main():

    # 初始化资源
    print("正在初始化...")

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
    
    interface= await LoadJson()
    task_dict=await GetTaskList(interface)
    print("初始化完毕")
    # time.sleep(1)
    os.system("cls")

    # 选择任务
    task = await ChooseTask(task_dict)
    await maa_inst.run_task("StartUp")
    
    
   
    

if __name__ == "__main__":
    asyncio.run(main())
