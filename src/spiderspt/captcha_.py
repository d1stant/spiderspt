"""
对接验证码识别平台的模块

已完成的平台:
1. 云码
    邀请码: TG34946
    邀请注册链接: https://console.jfbym.com/register/TG34946
"""

from typing import Any, TypeAlias

import requests
from requests import Response

Base64Str: TypeAlias = str
ResponseJson: TypeAlias = dict


class YunMaError(Exception):
    pass


class OCRYunMa:
    ERROR_CODE: dict[str, str] = {
        # 10000: "识别成功",
        "10001": "参数错误",
        "10002": "余额不足",
        "10003": "无此访问权限",
        "10004": "无此验证类型",
        "10005": "网络拥塞",
        "10006": "数据包过载",
        "10007": "服务繁忙",
        "10008": "网络错误, 请稍后重试",
        "10009": "结果准备中, 请稍后再试",
        # 10010: "识别成功, 请求结束",
    }

    def __init__(self, token: str) -> None:
        self.token: str = token

    def __request_api(self, data: dict) -> ResponseJson:
        url = "http://api.jfbym.com/api/YmServer/customApi"
        heasders: dict[str, str] = {"Content-Type": "application/json"}
        data.update({"token": self.token})
        response: Response = requests.post(url, json=data, headers=heasders)
        result: ResponseJson = response.json()
        return result

    def __result_handle(self, result: ResponseJson) -> Any:
        code: str = str(result["code"])
        if code in self.ERROR_CODE:
            raise YunMaError(f"{code}: {self.ERROR_CODE[code]}, {result['msg']}")
        return result["data"]["data"]

    def custom_captcha(self, captcha_type: str, image: Base64Str) -> Any:
        data: dict[str, str] = {
            "type": captcha_type,
            "image": image,
        }
        result: ResponseJson = self.__request_api(data)
        return self.__result_handle(result)

    def slide_captcha(
        self, captcha_type: str, slide: Base64Str, background: Base64Str
    ) -> Any:
        data: dict[str, str] = {
            "type": captcha_type,
            "slide_image": slide,
            "background_image": background,
        }
        result: ResponseJson = self.__request_api(data)
        return self.__result_handle(result)

    def click_captcha(self, captcha_type: str, image: Base64Str, extra: str) -> Any:
        data: dict[str, str] = {
            "type": captcha_type,
            "image": image,
            "extra": extra,
        }
        result: ResponseJson = self.__request_api(data)
        return self.__result_handle(result)
