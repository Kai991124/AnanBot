"""
nlp聊天实现，用于自动回复
"""

from typing import Optional

from httpx import AsyncClient

from src.config import nlp_config, voice_config
from src.utils.log import logger

from .jx3api import JX3API, Response

import json
import time
import hashlib
class NLP:
    """
    nlp封装类
    """

    client: AsyncClient
    """异步请求客户端"""
    qingyunke_url: str
    """青云客接口地址"""

    def __init__(self):
        self.client = AsyncClient()
        self.api = JX3API()
        self.nlp_config = nlp_config
        self.voice_config = voice_config
        self.qingyunke_url = "http://api.qingyunke.com/api.php"

    def check_nlp_config(self) -> bool:
        """
        检查nlp配置
        """
        return self.nlp_config.secretId != "" and self.nlp_config.secretKey != ""

    def check_voice_config(self) -> bool:
        """
        检查voice配置
        """
        return self.voice_config.access != "" and self.voice_config.appkey != ""

    async def chat_with_tencent(self, nickname: str, text: str) -> Optional[str]:
        """
        说明:
            使用腾讯云接口聊天

        参数:
            * `nickname`：机器人昵称
            * `text`：聊天内容

        返回:
            * `str`：回复内容
        """
        try:
            req: Response = await self.api.transmit_chat(
                secretId=self.nlp_config.secretId,
                secretKey=self.nlp_config.secretKey,
                name=nickname,
                question=text,
            )
            if req.code == 200:
                msg: str = req.data["answer"]
                logger.debug(f"腾讯请求成功，返回：{msg}")
                return msg
            else:
                return None
        except Exception as e:
            logger.debug(f"腾讯云请求错误，返回：{str(e)}")
            return None

    async def chat_with_qingyunke(self, nickname: str, text: str) -> Optional[str]:
        """
        说明:
            使用青云客接口聊天

        参数:
            * `nickname`：机器人昵称
            * `text`：聊天内容

        返回:
            * `str`：回复内容
        """
        '''
        http://api.qingyunke.com/api.php?params={"key": "free", "appid": 0, "msg": "text"}
        http://api.qingyunke.com/api.php?key=free&appid=0&msg=%E6%88%91%E7%88%B1%E4%BD%A0
        req = await AsyncClient.get(self.qingyunke_url, params=params)
        '''
        params = {"key": "free", "appid": 0, "msg": text}
        try:
            req = await self.client.get(self.qingyunke_url, params=params)
            req_json = req.json()
            if req_json["result"] == 0:
                msg = str(req_json["content"])
                # 消息替换
                msg = msg.replace(r"{br}", "\n")
                msg = msg.replace("菲菲", nickname)
                logger.debug(f"青云客请求成功，返回：{msg}")
                return msg
            else:
                logger.debug(f"青云客请求失败，返回：{req_json['content']}")
                return None
        except Exception as e:
            logger.debug(f"青云客请求出错，返回：{str(e)}")
            return None

    async def chat_with_ali(self, nickname: str, text: str) -> Optional[str]:
        url = 'https://openapi.singularity-ai.com/api/v2/generateByKey'
        api_key = '6b10811b1b26005d8b0df042ca6bdb28'  # 这里需要替换你的APIKey
        api_secret = '9a83650dce0ec05d4beaa944d58b79624e7bfbcf19f908c9'  # 这里需要替换你的APISecret
        timestamp = str(int(time.time()))
        prompt = f'以下是一组问答。给出问题，ai会给出答案。\n问：{text}\n答：\n'
        model_version = 'benetnasch_common_gpt3'
        sign_content = api_key + api_secret + model_version + prompt + timestamp
        sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()
        headers = {
            "App-Key": "Bearer " + api_key,
            "timestamp": timestamp,
            "sign": sign_result,
            "Content-Type": "application/json"
        }
        data = {
            "data": {
                "prompt": prompt,
                "model_version": model_version,
                "param": {
                    "generate_length": 100,
                    "top_p": 0.1,
                    "top_k": 10,
                    "repetition_penalty": 1.3,
                    "length_penalty": 1,
                    "min_len": 2,
                    "temperature": 1,
                    "end_words": [
                        "[EOS]",
                        "\n"
                    ]
                }
            }
        }
        try:
            req = await self.client.post(url = 'https://openapi.singularity-ai.com/api/v2/generateByKey', headers=headers,json=data)
            req_json=req.json()
            if req_json["code_msg"] == 'Success':
                msg = req_json['resp_Data']['reply']
                print(msg)
                logger.debug(f"阿里云请求成功，返回：{msg}")
                return msg
            else:
                logger.debug(f"阿里云请求失败，返回：{req_json['code_msg']}")
                return None
        except Exception as e:
            logger.debug(f"阿里云请求出错，返回：{str(e)}")
            return None

    async def chat(self, nickname: str, text: str) -> Optional[str]:
        """
        说明:
            请求聊天，优先使用腾讯云接口

        参数:
            * `nickname`：机器人昵称
            * `text`：聊天内容

        返回:
            * `str`：回复内容
        """
        if self.check_nlp_config():
            if msg := await self.chat_with_tencent(nickname, text):
                return msg
        return await self.chat_with_ali(nickname, text)

    async def get_voice(self, text: str) -> Optional[str]:
        """
        说明:
            使用阿里云文字转语音

        参数:
            * `text`：转换语音内容

        返回:
            * `str`：语音url地址
        """
        logger.debug(f"请求语音合成：{text}")
        try:
            req: Response = await self.api.transmit_alitts(
                text=text, **self.voice_config
            )
            if req.code == 200:
                logger.debug("请求语音成功！")
                return req.data["url"]
            else:
                logger.debug(f"请求语音失败，返回：{req.data}")
                return None
        except Exception as e:
            logger.debug(f"语音合成出错，返回：{str(e)}")
            return None


chat = NLP()
"""
nlp聊天封装，用于自动回复
"""
