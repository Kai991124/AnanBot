from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, Bot, GroupMessageEvent
from nonebot.plugin import PluginMetadata
import pandas as pd
import random
from src.internal.eat import eat
from src.params import PluginConfig, cost_gold
from src.utils.log import logger
import re

__plugin_meta__ = PluginMetadata(
    name="吃",
    description="人以食为天",
    usage="参考帮助",
    config=PluginConfig(),
)

'matchers'


eat_suggest = on_regex(pattern=r"吃啥", permission=GROUP, priority=5, block=True)
recipe_suggest = on_regex(pattern=r"做啥吃", permission=GROUP, priority=5, block=True)


@eat_suggest.handle()
async def _(event: GroupMessageEvent):
    '吃啥推荐'
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求吃啥")
    eat_file_path = r'/workspace/AnanBot/src/plugins/eat/不知道吃什么就打开.xlsx'
    df = pd.read_excel(eat_file_path)
    food_list = df['都是档口啊'].to_list()
    res = random.sample(range(0, len(food_list)), 3)
    reply = '吃点什么呢？考虑一下这几个？\n'
    for i in range(3):
        reply = reply + '-' * 4 + food_list[res[i]] + '\n'
    await eat_suggest.finish(reply)

@recipe_suggest.handle()
async def _(bot: Bot,event: GroupMessageEvent, name: str):
    """菜谱查询"""
    nickname = list(bot.config.nickname)[0]
    message = event.get_plaintext()
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求：{message}")
    msg = await eat.get_recipe_jd(nickname, message)
    await recipe_suggest.finish(msg)



