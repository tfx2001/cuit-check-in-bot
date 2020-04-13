# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

from .form import getFormValue

"""
登陆步骤说明

- 获取计算中心-计算平台的sessionID
- 获取跳转链接
- 获取登陆系统的sessionID
- 登陆
- 打卡
"""

urls = [
    "http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/mainMenu.asp",
    "",
    "http://login.cuit.edu.cn/Login/xLogin/Login.asp",
    "http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netKs/sj.asp?UTp=Xs&jkdk=Y",
    "http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netKs/",
    "http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netKs/editSjRs.asp",
]

commonHeaders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Upgrade-Insecure-Requests": "1",
}

headers = [
    {"Referer": "http://jszx.cuit.edu.cn/"},
    {"Referer": "http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp"},
    {
        "Referer": "http://login.cuit.edu.cn/Login/xLogin/Login.asp",
        "Cache-Control": "max-age=0",
    },
    {"Referer": "http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp"},
    {},
    {
        "Cache-Control": "max-age=0",
        "Referer": "http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netKs/editSjRs.asp",
    },
]


def checkIn(studentID, studentPassword):
    session = requests.session()

    # 获取计算中心-计算平台的sessionID
    resp = session.get(urls[0], headers={**headers[0], **commonHeaders})
    if resp.status_code != 200:
        raise Exception("获取计算平台的sessionID失败！")

    # 获取跳转链接
    bs = BeautifulSoup(resp.content.decode("GBK"), "html.parser")
    urls[1] = bs.meta.find_next().attrs["content"][6:]

    # 获取登陆系统sessionID
    resp = session.get(urls[1], headers={**headers[1], **commonHeaders})
    if resp.status_code != 200:
        raise Exception("获取登陆系统sessionID失败！")

    # 获取codeKey
    bs = BeautifulSoup(resp.content.decode("GBK"), "html.parser")
    codeKey = bs.find("input", attrs={"name": "codeKey"}).attrs["value"]

    # 登陆
    resp = session.post(
        urls[2],
        {
            "WinW": 1920,
            "WinH": "1040",
            "txtId": studentID,
            "txtMM": studentPassword,
            "verifycode": "不分大小写".encode("gb2312"),
            "codeKey": codeKey,
            "Login": "Check",
            "IbtnEnter.x": 26,
            "IbtnEnter.y": 26,
        },
        headers={**headers[2], **commonHeaders},
    )
    if resp.content.decode("gbk").find("用户名或密码错误") != -1:
        bs = BeautifulSoup(resp.content.decode("gbk"), "html.parser")
        raise Exception(bs.findAll("span")[0].text)

    # 获取打卡链接
    resp = session.get(urls[3], headers={**headers[3], **commonHeaders})
    bs = BeautifulSoup(resp.content.decode("GBK"), "html.parser")
    checkInLink = bs.find_all("a")[1].attrs["href"]

    # 获取前日打卡信息
    resp = session.get(urls[4] + checkInLink)
    bs = BeautifulSoup(resp.content.decode("GBK"), "html.parser")
    formValue = getFormValue(bs)

    # 更新表单
    formValue["sF21650_5"] = "1"
    formValue["sF21650_6"] = "5"
    formValue["sF21650_7"] = "1"
    formValue["sF21650_8"] = "1"
    formValue["sF21650_9"] = "1"

    formValue["wtOR_1"] = "\|/".join(
        [
            formValue["sF21648_1"],
            formValue["sF21648_2"],
            formValue["sF21648_3"],
            formValue["sF21648_4"],
            formValue["sF21648_5"],
            formValue["sF21648_6"],
        ]
    )

    formValue["wtOR_2"] = "\|/".join(
        [
            formValue["sF21649_1"],
            formValue["sF21649_2"],
            formValue["sF21649_3"],
            formValue["sF21649_4"],
        ]
    )

    formValue["wtOR_3"] = "\|/".join(
        [
            formValue["sF21650_1"],
            formValue["sF21650_2"],
            formValue["sF21650_3"],
            formValue["sF21650_4"],
            formValue["sF21650_5"],
            formValue["sF21650_6"],
            formValue["sF21650_7"],
            formValue["sF21650_8"],
            formValue["sF21650_9"],
        ]
    )

    for key in formValue:
        formValue[key] = formValue[key].encode("gbk")

    # 提交表单
    resp = session.post(
        urls[5],
        formValue,
        headers={**headers[5], **commonHeaders, "Referer": urls[4] + checkInLink},
    )
    bs = BeautifulSoup(resp.content.decode("GBK"), "html.parser")
    if resp.content.decode("GBK").find("提交打卡成功") != -1:
        print(f'学号：{studentID} {bs.findAll("span")[1].text}')
    else:
        raise Exception("打卡失败！")
