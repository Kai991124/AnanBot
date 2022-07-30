from typing import Optional

from httpx import AsyncClient

from src.utils.log import logger

from .jx3api import JX3API, Response
import random


class EAT:
    """
    吃东西封装类
    """

    client: AsyncClient
    """异步请求客户端"""
    jd_url: str
    """京东云接口地址"""

    def __init__(self):
        self.client = AsyncClient()
        self.api = JX3API()
        self.key = 'bdcd86b83410c65b0981a17367a352bd'
        self.jd_url = 'https://way.jd.com/jisuapi/search'

    async def get_recipe_jd(self, nickname: str, text: str) -> Optional[str]:
        """
        说明:
            使用京东云接口查询菜谱
            https://way.jd.com/jisuapi/search?keyword=白菜&num=10&start=0&appkey=您申请的APPKEY

        参数:
            * `nickname`：机器人昵称
            * `text`：聊天内容

        返回:
            * `str`：回复内容

            response format:

        """
        params = {"keyword": text, "num": 5, "start": 10, "appkey": self.key}
        try:
            req = await self.client.get(self.jd_url, params=params)
            req_json = req.json()
            ## print recipe
            ## 选择一个recipe

            if req_json["code"] == 10000:
                recipe_list = req_json['result']['result']['list']
                recipe_num = len(recipe_list)
                if recipe_num == 0:
                    msg = f'{nickname}也不知道有什么可以用{text}做的菜呜呜呜'
                    return msg
                ## choose one recipe
                recipe_sort = random.randint(0, recipe_num - 1)
                recipe = recipe_list[recipe_sort]
                name = recipe['name']
                material = recipe['material']
                tag = recipe['tag']
                process = recipe['process']
                # 原材料
                material_context = ''
                for i in range(len(material)):
                    amount = material[i]['amount']
                    mname = material[i]['mname']
                    temp_material_context = f'{amount}{mname}。' if i == 0 else f'{amount}{mname}、'
                    material_context = material_context + temp_material_context
                # 流程

                process_context = ''
                for i in range(len(process)):
                    pcontent = process[i]['pcontent']
                    temp_process_context = f'{i + 1}：{pcontent}\n'
                    process_context = process_context + temp_process_context
                # 消息替换
                msg = f'{nickname}给你推荐一道菜，菜名{name}，特点是{tag}。\n需要的原材料有：{material_context}\n制作流程是\n{process_context}\n希望你喜欢\n'
                logger.debug(f"京东云请求成功，返回：{msg}")
                return msg
            else:
                logger.debug(f"京东云请求失败，返回：{req_json['code']}")
                return None
        except Exception as e:
            logger.debug(f"京东云请求出错，返回：{str(e)}")
            return None

    async def get_recipe(self, nickname: str, text: str) -> Optional[str]:
        """
        说明:
            请求菜谱，使用京东云菜谱

        参数:
            * `nickname`：机器人昵称
            * `text`：聊天内容

        返回:
            * `str`：回复内容
        """
        return await self.get_recipe_jd(nickname, text)


eat = EAT()
"""
吃的聊天封装，用于自动回复
"""
