# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

bsdb = db_x["bot_sdb"]

default_text = """<b>Merhaba, {user_firstname}!
Bu, {boss_firstname} Kullanıcı Botu.</b>
<i>Efendim Şimdilik Meşgul, Bir Ara Bekleyebilirsiniz
Sizinle Konuşması Gerekirse Sizi Onaylayacaktır!</i>
<b><u>{warns} Uyarınız Var.</b></u>
"""
default_bloco_text = "'İşte bu! Size {int(pm_warns)} Uyarı Verdim.\nArtık Rapor Edildiniz ve Engellendiniz`\n**Nedeni:** `SPAM LİMİTİ AŞILDI!`"

default_thumb = "https://icon-icons.com/downloadimage.php?id=106660&root=1527/PNG/512/&file=shield_106660.png"


async def add_pm_text(text=default_text):
    ujwal = await bsdb.find_one({"_id": "PM_START_MSG"})
    if ujwal:
        await bsdb.update_one({"_id": "PM_START_MSG"}, {"$set": {"pm_msg": text}})
    else:
        await bsdb.insert_one({"_id": "PM_START_MSG", "pm_msg": text})

async def add_block_text(text=default_bloco_text):
    _ = await bsdb.find_one({"_id": "PM_BLOCK_MSG"})
    if _:
        await bsdb.update_one({"_id": "PM_BLOCK_MSG"}, {"$set": {"msg": text}})
    else:
        await bsdb.insert_one({"_id": "PM_BLOCK_MSG", "msg": text})

async def add_pm_thumb(thumb=default_thumb):
    ujwal = await bsdb.find_one({"_id": "PM_START_THUMB"})
    if ujwal:
        await bsdb.update_one({"_id": "PM_START_THUMB"}, {"$set": {"pm_img": thumb}})
    else:
        await bsdb.insert_one({"_id": "PM_START_THUMB", "pm_img": thumb})


async def get_thumb():
    ujwal = await bsdb.find_one({"_id": "PM_START_THUMB"})
    if ujwal:
        return ujwal["pm_img"]
    else:
        return None 


async def get_pm_text():
    ujwal = await bsdb.find_one({"_id": "PM_START_MSG"})
    if ujwal:
        return ujwal["pm_msg"]
    else:
        return default_text
    
async def get_block_text():
    __ = await bsdb.find_one({"_id": "PM_BLOCK_MSG"})
    if __:
        return __["msg"]
    else:
        return default_bloco_text


async def set_pm_spam_limit(psl=3):
    stark = await bsdb.find_one({"_id": "LIMIT_PM"})
    if stark:
        await bsdb.update_one({"_id": "LIMIT_PM"}, {"$set": {"psl": int(psl)}})
    else:
        await bsdb.insert_one({"_id": "LIMIT_PM", "psl": int(psl)})


async def get_pm_spam_limit():
    meisnub = await bsdb.find_one({"_id": "LIMIT_PM"})
    if meisnub:
        return int(meisnub["psl"])
    else:
        return 3
