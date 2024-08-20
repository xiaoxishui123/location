# encoding:utf-8

import requests
import plugins
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *

@plugins.register(
    name="IPLocation",
    desire_priority=66,
    hidden=False,
    desc="获取IP地址的地理位置。",
    version="1.0",
    author="你的名字",
)
class IPLocation(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.handlers[Event.ON_COMMAND] = self.on_command
            logger.info("[IPLocation] inited.")
        except Exception as e:
            logger.warn("[IPLocation] init failed, ignore.")
            raise e

    def on_command(self, e_context: EventContext):
        command = e_context["command"]
        if command.startswith("获取IP位置"):
            ip_address = command.split(" ")[1] if len(command.split(" ")) > 1 else "8.8.8.8"
            logger.info(f"[IPLocation] fetching location for IP: {ip_address}")
            self.call_ip_location_api(ip_address, e_context)

    def call_ip_location_api(self, ip_address, e_context):
        base_url = "https://app.ipdatacloud.com/v2/free_query"
        request_url = f"{base_url}?ip={ip_address}"
        
        try:
            response = requests.get(request_url)
            if response.status_code == 200:
                data = response.json()
                location_info = (
                    f"IP地理位置定位结果：\n"
                    f"城市: {data['data'].get('city', '未知')}\n"
                    f"国家: {data['data'].get('country', '未知')}\n"
                    f"国家英文名称: {data['data'].get('country_english', '未知')}\n"
                    f"IP地址: {data['data'].get('ip', '未知')}\n"
                    f"互联网服务提供商: {data['data'].get('isp', '未知')}\n"
                    f"省份: {data['data'].get('province', '未知')}"
                )
                e_context["reply"] = Reply(ReplyType.TEXT, location_info)
            else:
                logger.warn(f"[IPLocation] request failed, status code: {response.status_code}")
                e_context["reply"] = Reply(ReplyType.TEXT, f"请求失败，状态码：{response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warn(f"[IPLocation] request error: {e}")
            e_context["reply"] = Reply(ReplyType.TEXT, f"请求过程中发生错误: {e}")

    def get_help_text(self, **kwargs):
        return "获取IP地址的地理位置。使用方法：获取IP位置 <IP地址>。"
