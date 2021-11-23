# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

import inspect
import logging
import os
from datetime import datetime
from traceback import format_exc
import asyncio
import pytz
from pyrogram import ContinuePropagation, StopPropagation, filters
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    MessageEmpty,
    UserNotParticipant
)
from pyrogram.handlers import MessageHandler

from main_startup import (
    CMD_LIST,
    XTRA_CMD_LIST,
    Config,
    Electron,
    Electron2,
    Electron3,
    Electron4,
    bot
)
from main_startup.config_var import Config
from main_startup.helper_func.basic_helpers import is_admin_or_owner
from main_startup.core.helpers import edit_or_reply
from database.sudodb import sudo_list

from bot_utils_files.Localization.engine import Engine as engin_e

Engine = engin_e()


sudo_list_ = Electron.loop.create_task(sudo_list())

async def _sudo(f, client, message):
    if not message:
        return bool(False)
    if not message.from_user:
        return bool(False)
    if not message.from_user.id:
        return bool(False)
    if message.from_user.id in sudo_list_.result():
        return bool(True)
    return bool(False)

_sudo = filters.create(func=_sudo, name="_sudo")

def electron_on_cmd(
    cmd: list,
    group: int = 0,
    pm_only: bool = False,
    group_only: bool = False,
    chnnl_only: bool = False,
    only_if_admin: bool = False,
    ignore_errors: bool = False,
    propagate_to_next_handler: bool = True,
    disable_sudo: bool = False,
    file_name: str = None,
    is_official: bool = True,
    cmd_help: dict = {"__Açıklama__": "Sana Kimse Yardımcı Olmayacak", "__Kullanım__": "{ch}what"},
):
    """- Komutları Kaydetmek İçin Ana Dekoratör. -"""
    if disable_sudo:
        filterm = (
        filters.me
        & filters.command(cmd, Config.COMMAND_HANDLER)
        & ~filters.via_bot
        & ~filters.forwarded
    )
    else:
        filterm = (
            (filters.me | _sudo)
            & filters.command(cmd, Config.COMMAND_HANDLER)
            & ~filters.via_bot
            & ~filters.forwarded)
    cmd = list(cmd)
    add_help_menu(
        cmd=cmd[0],
        stack=inspect.stack(),
        is_official=is_official,
        cmd_help=cmd_help["help"],
        example=cmd_help["example"],
    )
    def decorator(func):
        async def wrapper(client, message):
            message.Engine = Engine
            message.client = client
            chat_type = message.chat.type
            if only_if_admin and not await is_admin_or_owner(
                message, (client.me).id
            ):
                await edit_or_reply(
                    message, "`Bu Komut Sadece Sohbetin Adminiyseniz Çalışır!`"
                )
                return
            if group_only and chat_type != "supergroup":
                await edit_or_reply(message, "`Bunun bir grup olduğuna emin misin?`")
                return
            if chnnl_only and chat_type != "channel":
                await edit_or_reply(message, "Bu Komut Sadece Kanalda Çalışır!")
                return
            if pm_only and chat_type != "private":
                await edit_or_reply(message, "`Bu Cmd Sadece PM'de Çalışır!`")
                return
            if ignore_errors:
                await func(client, message)
            else:
                try:
                    await func(client, message)
                except StopPropagation:
                    raise StopPropagation
                except KeyboardInterrupt:
                    pass
                except MessageNotModified:
                    pass
                except MessageIdInvalid:
                    logging.warning(
                        "İşlem Yapılırken Lütfen Komutları Silmeyin.."
                    )
                except UserNotParticipant:
                    pass
                except ContinuePropagation:
                    raise ContinuePropagation
                except BaseException:
                    logging.error(
                        f"İstisna - {func.__module__} - {func.__name__}"
                    )
                    TZ = pytz.timezone(Config.TZ)
                    datetime_tz = datetime.now(TZ)
                    text = "**!HATA RAPORU!**\n\n"
                    text += f"\n**Geri iz : ** `{str(format_exc())}`"
                    text += f"\n**Plugin Adı :** `{func.__module__}`"
                    text += f"\n**Fonksiyon adı :** `{func.__name__}` \n"
                    text += datetime_tz.strftime(
                        "**Tarih :** `%Y-%m-%d` \n**Zaman :** `%H:%M:%S`"
                    )
                    text += "\n\n__Bunun Bir Hata Olduğunu Düşünüyorsanız Bunu @ElectronDestek'e İletebilirsiniz!__"
                    try:
                        await client.send_message(Config.LOG_GRP, text)
                    except BaseException:
                        logging.error(text)
        add_handler(filterm, wrapper, cmd)
        return wrapper
    return decorator


def listen(filter_s):
    """Özel Filtreleri Kullanmak İçin Basit Dekoratör"""
    def decorator(func):
        async def wrapper(client, message):
            message.Engine = Engine
            try:
                await func(client, message)
            except StopPropagation:
                raise StopPropagation
            except ContinuePropagation:
                raise ContinuePropagation
            except UserNotParticipant:
                pass
            except MessageEmpty:
                pass
            except BaseException:
                logging.error(f"İstisna - {func.__module__} - {func.__name__}")
                TZ = pytz.timezone(Config.TZ)
                datetime_tz = datetime.now(TZ)
                text = "**!GÜNCELLEMELER İŞLENİRKEN HATA OLUŞTU!**\n\n"
                text += f"\n**Geri iz : ** `{str(format_exc())}`"
                text += f"\n**Plugin-Adı :** `{func.__module__}`"
                text += f"\n**Fonksiyon adı :** `{func.__name__}` \n"
                text += datetime_tz.strftime(
                    "**Tarih :** `%Y-%m-%d` \n**Zaman :** `%H:%M:%S`"
                )
                text += "\n\n__Bunun Bir Hata Olduğunu Düşünüyorsanız Bunu @ElectronDestek'e İletebilirsiniz!__"
                try:
                    await client.send_message(Config.LOG_GRP, text)
                except BaseException:
                    logging.error(text)
            message.continue_propagation()
        Electron.add_handler(MessageHandler(wrapper, filters=filter_s), group=0)
        if Electron2:
            Electron2.add_handler(MessageHandler(wrapper, filters=filter_s), group=0)
        if Electron3:
            Electron3.add_handler(MessageHandler(wrapper, filters=filter_s), group=0)
        if Electron4:
            Electron4.add_handler(MessageHandler(wrapper, filters=filter_s), group=0)
        return wrapper

    return decorator


def add_help_menu(
    cmd,
    stack,
    is_official=True,
    cmd_help="Sana Kimse Yardımcı Olmayacak",
    example="{ch}what",
    file_name=None,
):
    if not file_name:
        previous_stack_frame = stack[1]
        if "xtraplugins" in previous_stack_frame.filename:
            is_official = False
        file_name = os.path.basename(previous_stack_frame.filename.replace(".py", ""))
    cmd_helpz = example.format(ch=Config.COMMAND_HANDLER)
    cmd_helper = f"**Modül Adı :** `{file_name.replace('_', ' ').title()}` \n\n**Komut :** `{Config.COMMAND_HANDLER}{cmd}` \n**Yardım :** `{cmd_help}` \n**Örnek :** `{cmd_helpz}`"
    if is_official:
        if file_name not in CMD_LIST.keys():
            CMD_LIST[file_name] = cmd_helper
        else:
            CMD_LIST[
                file_name
            ] += f"\n\n**Komut :** `{Config.COMMAND_HANDLER}{cmd}` \n**Yardım :** `{cmd_help}` \n**Örnek :** `{cmd_helpz}`"
    elif file_name not in XTRA_CMD_LIST.keys():
        XTRA_CMD_LIST[file_name] = cmd_helper
    else:
        XTRA_CMD_LIST[
            file_name
        ] += f"\n\n**Komut :** `{Config.COMMAND_HANDLER}{cmd}` \n**Yardım :** `{cmd_help}` \n**Örnek :** `{cmd_helpz}`"
            

def add_handler(filter_s, func_, cmd):
    d_c_l = Config.DISABLED_SUDO_CMD_S
    if d_c_l:
        d_c_l = d_c_l.split(" ")
        d_c_l = list(d_c_l)
        if "dev" in d_c_l:
            d_c_l.extend(['eval', 'bash', 'install']) 
        if any(item in list(d_c_l) for item in list(cmd)): 
            filter_s = (filters.me & filters.command(cmd, Config.COMMAND_HANDLER) & ~filters.via_bot & ~filters.forwarded)
    Electron.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if Electron2:
        Electron2.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if Electron3:
        Electron3.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if Electron4:
        Electron4.add_handler(MessageHandler(func_, filters=filter_s), group=0)      
