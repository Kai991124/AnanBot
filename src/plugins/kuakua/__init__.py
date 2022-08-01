from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, Bot, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from src.params import PluginConfig
from src.utils.log import logger
import re

__plugin_meta__ = PluginMetadata(
    name="夸夸",
    description="夸夸我的hxd",
    usage="参考帮助",
    config=PluginConfig(),
)

'matchers'

hxd_kuakua = on_regex(pattern=r'(西西|老糖|青蛙|托尼|点苍|大少爷|咩人|我哥们儿)?是', permission=GROUP, priority=5, block=True)
td_kuakua = on_regex(pattern=r'(泡芙|生发丸|千机|泡泡)?是', permission=GROUP, priority=5, block=True)
sf_kuakua = on_regex(pattern=r'(安安|槐安安|唐一墨|师父)+是', permission=GROUP, priority=5, block=True)
lp_kuakua = on_regex(pattern=r'(jerry|Jerry+)?是', permission=GROUP, priority=5, block=True)


@hxd_kuakua.handle()
async def _(event: GroupMessageEvent):
    '夸夸我的好兄弟'
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求夸夸")
    message = event.get_plaintext()
    if (re.search(r'(西西|老糖|青蛙|托尼|点苍|大少爷|哥们儿)?是', message)):
        bro_dic = {
            '西西': '犀利奶歌、完美奶秀',
            '老糖': '冷静奶花、绝代奶毒',
            '青蛙': '最强花椒油',
            '大少爷': '最强花椒油',
            '托尼': '毒经神',
            '点苍': '超硬苍云',
            '咩人': '全能神',
            '我哥们儿': '犀利大哥'
        }
        name = re.search(r'(西西|老糖|青蛙|托尼|点苍|大少爷|哥们儿)?是', message).group(1)
        honor = bro_dic[name]
        message=f'{name}是{honor}！'
    await hxd_kuakua.finish(message)


@td_kuakua.handle()
async def _(event: GroupMessageEvent):
    '夸夸我的好徒弟'
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求夸夸")
    message = event.get_plaintext()
    name = re.search(r'(泡芙|生发丸|千机|泡泡)?是', message).group(1)
    message = f'{name}是主人的好徒弟，看到这条消息快去练手法！！'
    await td_kuakua.finish(message)


@sf_kuakua.handle()
async def _(event: GroupMessageEvent):
    '夸夸我'
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求夸夸")
    message = event.get_plaintext()
    name = re.search(r'(安安|槐安安|唐一墨|师父)?是', message).group(1)
    message = f'{name}是我的主人，是世界上最好的主人！！！！！'
    await sf_kuakua.finish(message)


@lp_kuakua.handle()
async def _(event: GroupMessageEvent):
    '夸夸我lp'
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求夸夸")
    message = event.get_plaintext()
    name = re.search(r'(Jerry|jerry)?是', message).group()
    message = f'{name}是我的主人的宝贝，是世界上最好的宝！！！！！'
    await lp_kuakua.finish(message)
