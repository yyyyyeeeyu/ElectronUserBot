# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

import logging

from pyrogram import filters

from database.blacklistdb import (
    add_to_blacklist,
    blacklists_del,
    del_blacklist,
    get_chat_blacklist,
    is_blacklist_in_db,
)
from main_startup.core.decorators import electron_on_cmd, listen
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
)
from main_startup.helper_func.logger_s import LogIt


@electron_on_cmd(
    [
        "saveblacklist",
        "saveblockist",
        "addblacklist",
        "addblocklist",
        "blacklist",
        "textblacklist",
    ],
    cmd_help={
        "• __Açıklama__": "Metin Kara Listesini / Engellenen Listesini Ekler",
        "• __Kullanım__": "{ch}blacklist porno",
    },
)
async def addblacklist(client, message):
    engine = message.Engine
    messag_e_ = await edit_or_reply(message, engine.get_string("İŞLENİYOR"))
    blacklist = get_text(message)
    if not blacklist:
        await messag_e_.edit(engine.get_string("INPUT_REQ").format("KeyWord"))
        return
    if await is_blacklist_in_db(int(message.chat.id), blacklist):
        await messag_e_.edit(engine.get_string("BLACKLIST_1"))
        return
    blacklist = blacklist.lower()
    await add_to_blacklist(blacklist, int(message.chat.id))
    await messag_e_.edit(engine.get_string('BLACKLIST_2').format(blacklist))


@electron_on_cmd(
    ["listblacklist", "listblocklist"],
    cmd_help={"• __Açıklama__": "Kara Liste Listesini Kontrol Edin!", "• __Kullanım__": "{ch}listblocklist"},
)
async def listblacklist(client, message):
    engine = message.Engine
    messag_e_ = await edit_or_reply(message, engine.get_string("İŞLENİYOR"))
    if not await get_chat_blacklist(int(message.chat.id)):
        await messag_e_.edit(engine.get_string("BLACKLIST_3"))
        return
    OUT_STR = engine.get_string("BLACKLIST_4")
    for trigger_s_ in await get_chat_blacklist(int(message.chat.id)):
        OUT_STR += f"👉 `{trigger_s_['trigger']}` \n"
    await edit_or_send_as_file(OUT_STR, messag_e_, client, "Blacklist", "blacklist")


@electron_on_cmd(
    ["delblacklist", "rmblacklist", "delblockist", "rmblocklist"],
    cmd_help={
        "• __Açıklama__": "Kara Listeden / Engellenenler Listesinden Metni Kaldırın!",
        "• __Kullanım__": "{ch}delblacklist porno",
    },
)
async def delblacklist(client, message):
    engine = message.Engine
    messag_e_ = await edit_or_reply(message, engine.get_string("İŞLENİYOR"))
    blacklist = get_text(message)
    if not blacklist:
        await messag_e_.edit(engine.get_string("INPUT_REQ").format("KeyWord"))
        return
    if not await is_blacklist_in_db(int(message.chat.id), blacklist):
        await messag_e_.edit(engine.get_string("BLACKLIST_5"))
        return
    blacklist = blacklist.lower()
    await del_blacklist(blacklist, int(message.chat.id))
    await messag_e_.edit(engine.get_string("BLACKLIST_6").format(blacklist))


@listen(filters.incoming & ~filters.edited & filters.group)
async def activeblack(client, message):
    engine = message.Engine
    if not await get_chat_blacklist(int(message.chat.id)):
        return
    owo = message.text
    if owo is message.text:
        return
    owoo = owo.lower()
    tges = owoo.split(" ")
    for owo in tges:
        if await is_blacklist_in_db(int(message.chat.id), owo):
            try:
                await message.delete()
            except Exception as e:
                logging.error(f"[Blacklist] - {e}")
                log = LogIt(message)
                await log.log_msg(
                    client,
                    engine.get_strings("BLACKLIST_7").format(message.chat.title, e)
                )
    


@electron_on_cmd(
    ["delblacklists", "rmblacklists", "delblockists", "rmblocklists"],
    cmd_help={
        "• __Açıklama__": "Her Şeyi Engellenenler Listesinden Kaldırın!",
        "• __Kullanım__": "{ch}delblacklists",
    },
)
async def delblacklists(client, message):
    engine = message.Engine
    messag_e_ = await edit_or_reply(message, engine.get_string("İŞLENİYOR"))
    if not await get_chat_blacklist(int(message.chat.id)):
        await messag_e_.edit(engine.get_string("BLACKLIST_3"))
        return
    await blacklists_del(int(message.chat.id))
    await messag_e_.edit(engine.get_string("BLACKLIST_8"))
