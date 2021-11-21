# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

import logging
import os
import time
import motor.motor_asyncio
from pyrogram import Client

from .config_var import Config

# Note StartUp Time - To Capture Uptime.
start_time = time.time()
electron_version = "V1.0"

# Enable Logging For Pyrogram
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [ElectronUB] - %(levelname)s - %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)


mongo_client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_DB)

CMD_LIST = {}
XTRA_CMD_LIST = {}
sudo_id = Config.AFS

if not Config.STRINGSESSION:
    logging.error("String Session Bulunamadı! Electron Çıkıyor!")
    quit(1)

if not Config.API_ID:
    logging.error("API İD Bulunamadı! Electron Çıkıyor!")
    quit(1)

if not Config.API_HASH:
    logging.error("API HASH Bulunamadı! Electron Çıkıyor!")
    quit(1)

if not Config.LOG_GRP:
    logging.error("LOG Grubu İD'si Bulunamadı! Electron Çıkıyor!")
    quit(1)


# Müşteriler - 4 Müşteriye Kadar Desteklenir!
if Config.STRINGSESSION:
    Electron = Client(
        Config.STRINGSESSION,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=180,
    )
if Config.STRINGSESSION_2:
    Electron2 = Client(
        Config.STRINGSESSION_2,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=180,
    )
else:
    Electron2 = None
if Config.STRINGSESSION_3:
    Electron3 = Client(
        Config.STRINGSESSION_3,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=180,
    )
else:
    Electron3 = None
if Config.STRINGSESSION_4:
    Electron4 = Client(
        Config.STRINGSESSION_4,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=180,
    )
else:
    Electron4 = None

if Config.BOT_TOKEN:
    bot = Client(
        "Asistanım",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        sleep_threshold=180,
    )
else:
    bot = None
