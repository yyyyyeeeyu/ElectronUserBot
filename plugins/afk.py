# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
from datetime import datetime

from pyrogram import filters

from database.afk import check_afk, go_afk, no_afk
from main_startup.config_var import Config
from main_startup.core.decorators import electron_on_cmd, listen
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.helper_func.logger_s import LogIt
afk_sanity_check: dict = {}


async def is_afk_(f, client, message):
    af_k_c = await check_afk()
    if af_k_c:
        return bool(True)
    else:
        return bool(False)


is_afk = filters.create(func=is_afk_, name="is_afk_")


@electron_on_cmd(
    ["afk"],
    propagate_to_next_handler=False,
    cmd_help={
        "help": "AFK olun!",
        "example": "{ch}afk",
    },
)
async def set_afk(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("İŞLENİYOR"))
    msge = None
    msge = get_text(message)
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    log = LogIt(message)
    if msge:
        msg = engine.get_string("AFK_1").format(msge)
        await log.log_msg(
            client,
            engine.get_string("AFK_2").format(msge)
        )
        await go_afk(afk_start, msge)
    else:
        msg = engine.get_string("AFK_3")
        await log.log_msg(
            client,
            engine.get_string("AFK_2").format("Belirtilmemiş.")
        )
        await go_afk(afk_start)
    await pablo.edit(msg)


@listen(
    is_afk
    & (filters.mentioned | filters.private)
    & ~filters.me
    & ~filters.bot
    & ~filters.edited
    & filters.incoming
)
async def afk_er(client, message):
    if not message:
        return
    if not message.from_user:
        return
    if message.from_user.id == client.me.id:
        return
    use_r = int(message.from_user.id)
    if use_r not in afk_sanity_check.keys():
        afk_sanity_check[use_r] = 1
    else:
        afk_sanity_check[use_r] += 1
    if afk_sanity_check[use_r] == 5:
        await message.reply_text(
            "`Size 5 Defa Sahibimin Müsait Olmadığını Söyledim Şimdi Cevap Vermeyeceğim. ;(`"
        )
        afk_sanity_check[use_r] += 1
        return
    if afk_sanity_check[use_r] > 5:
        return
    lol = await check_afk()
    reason = lol["reason"]
    if reason == "":
        reason = None
    back_alivee = datetime.now()
    afk_start = lol["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    message_to_reply = (
        f"Şu an [AFK]'yım. \n**Son Görülmem :** `{total_afk_time}`\n**Neden** : `{reason}`"
        if reason
        else f"Şu an [AFK]'yım. \n**Son Görülmem :** `{total_afk_time}`"
    )
    await message.reply(message_to_reply)


@listen(filters.outgoing & filters.me & is_afk)
async def no_afke(client, message):
    engine = message.Engine
    lol = await check_afk()
    back_alivee = datetime.now()
    afk_start = lol["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    kk = await message.reply(engine.get_string("AFK_4").format(total_afk_time))
    await kk.delete()
    await no_afk()
    log = LogIt(message)
    await log.log_msg(
        client,
        engine.get_string("AFK_5").format(total_afk_time)
    )
