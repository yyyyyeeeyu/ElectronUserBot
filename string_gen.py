import pyrogram
from pyrogram import Client

electron_ = """
╔══╗╔╗ ♡ ♡ ♡
╚╗╔╝║║╔═╦╦╦╔╗
╔╝╚╗║╚╣║║║║╔╣
╚══╝╚═╩═╩═╩═╝
Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
and is released under the "GNU v3.0 License Agreement".
Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
All rights reserved.
"""

print(electron_)

api_id = input("API İD'nizi Girin: \n")
api_hash = input("API HASH'inizi girin : \n")

with Client("ElectronUB", api_id=api_id, api_hash=api_hash) as bot_:
    first_name = (bot_.get_me()).first_name
    string_session_ = f"<b><u>{first_name}</b></u> için String Session \n<code>{bot_.export_session_string()}</code>"
    bot_.send_message("me", string_session_, parse_mode="html")
    print(f"Kayıtlı Mesajınıza String Gönderildi: {first_name}")
