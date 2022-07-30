from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, GroupMessageEvent
from nonebot.plugin import PluginMetadata
import pandas as pd
import random
from src.internal.jx3api import JX3API
from src.params import PluginConfig, cost_gold
from src.utils.log import logger
import re

__plugin_meta__ = PluginMetadata(
    name="餐点推荐",
    description="推荐吃什么。",
    usage="吃啥",
    config=PluginConfig(),
)


eat_regex = r"吃啥"
eat_suggest = on_regex(pattern=eat_regex, permission=GROUP, priority=5, block=True)


@eat_suggest.handle(parameterless=[cost_gold(gold=1)])
async def _(event: GroupMessageEvent):
    """舔狗日记"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求吃啥")
    eat_file_path = r'/workspace/AnanBot/src/plugins/unique_func/不知道吃什么就打开.xlsx'
    df = pd.read_excel(eat_file_path)
    food_list = df['都是档口啊'].to_list()
    res = random.sample(range(0, len(food_list)), 3)
    reply = '吃点什么呢？考虑一下这几个？\n'
    for i in range(3):
        reply = reply + '-' * 4 + food_list[res[i]] + '\n'
    await eat_suggest.finish(reply)
