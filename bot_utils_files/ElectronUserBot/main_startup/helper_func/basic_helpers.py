# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import logging
import math
import os
import shlex
import time
from math import ceil
from traceback import format_exc
from typing import Tuple
from pyrogram import Client
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import (
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from main_startup import Electron, Electron2, Electron3, Electron4
from database.sudodb import sudo_list
from main_startup.config_var import Config
import multiprocessing
import mimetypes
import functools
import threading
from concurrent.futures import ThreadPoolExecutor

max_workers = multiprocessing.cpu_count() * 5
exc_ = ThreadPoolExecutor(max_workers=max_workers)


def guess_mime_type(file_):
    """URL'den / Yoldan Bir Dosyanın Mime Türünü Alın"""
    s = mimetypes.guess_type(file_)
    if not s[0]:
        return None
    else:
        return s[0]


def get_user(message: Message, text: str) -> [int, str, None]:
    """Kullanıcıyı Mesajdan Al"""
    if text is None:
        asplit = None
    else:
        asplit = text.split(" ", 1)
    user_s = None
    reason_ = None
    if message.reply_to_message:
        user_s = message.reply_to_message.from_user.id
        reason_ = text if text else None
    elif asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        if message.entities:
            if len(message.entities) == 1:
                required_entity = message.entities[0]
                if required_entity.type == "text_mention":
                    user_s = int(required_entity.user.id)
                else:
                    user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        else:
            user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_


async def edit_or_reply(message, text, parse_mode="md"):
    sudo_lis_t = await sudo_list()
    """Kendindense Mesajı Düzenle, Mesaja Cevap Ver. (Yalnızca Sudo'lar İçin Çalışır)"""
    if not message:
        return await message.edit(text, parse_mode=parse_mode)
    if not message.from_user:
        return await message.edit(text, parse_mode=parse_mode)
    if message.from_user.id in sudo_lis_t:
        if message.reply_to_message:
            return await message.reply_to_message.reply_text(text, parse_mode=parse_mode)
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)


async def is_admin_or_owner(message, user_id) -> bool:
    """Bir Kullanıcının Mevcut Grubun Yaratıcısı mı yoksa Yöneticisi mi Olduğunu Kontrol Edin"""
    if message.chat.type in ["private", "bot"]:
        # You Are Boss Of Pvt Chats.
        return True
    user_s = await message.chat.get_member(int(user_id))
    if user_s.status in ("creator", "administrator"):
        return True
    return False


def get_readable_time(seconds: int) -> int:
    """İnsanların Okuyabilmesi İçin Zaman Ayırın"""
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


async def get_all_pros() -> list:
    """Tüm Kullanıcıları, Sudo + Sahipleri + Diğer İstemcileri Alın"""
    users = await sudo_list()
    ujwal = Electron.me
    users.append(ujwal.id)
    if Electron2:
        ujwal2 = Electron2.me
        users.append(ujwal2.id)
    if Electron3:
        ujwal3 = Electron3.me
        users.append(ujwal3.id)
    if Electron4:
        ujwal4 = Electron4.me
        users.append(ujwal4.id)
    return users


def paginate_help(page_number, loaded_modules, prefix, is_official=True):
    """Sayfalandırma Butonları"""
    number_of_rows = 6
    number_of_cols = 2
    helpable_modules = []
    for p in loaded_modules:
        if not p.startswith("_"):
            helpable_modules.append(p)
    helpable_modules = sorted(helpable_modules)
    modules = [
        InlineKeyboardButton(
            text="{} {} {}".format(
                Config.CUSTOM_HELP_EMOJI,
                x.replace("_", " ").title(),
                Config.CUSTOM_HELP_EMOJI,
            ),
            callback_data="us_plugin_{}|{}_{}".format(x, page_number, is_official),
        )
        for x in helpable_modules
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                InlineKeyboardButton(
                    text="⏪ Önceki",
                    callback_data="{}_prev({})_{}".format(
                        prefix, modulo_page, is_official
                    ),
                ),
                InlineKeyboardButton(text="Geri 🔙", callback_data=f"backO_to_help_menu"),
                InlineKeyboardButton(
                    text="İleri ⏩",
                    callback_data="{}_next({})_{}".format(
                        prefix, modulo_page, is_official
                    ),
                ),
            )
        ]
    return pairs


def cb_wrapper(func):
    async def wrapper(client, cb):
        users = await get_all_pros()
        if cb.from_user.id not in users:
            await cb.answer(
                "Sen Bana Erişemezsin, Sadece Sahibim Erişebilir. Neden Kendi Electron'unu kurmuyorsun? - @ElectronDestek",
                cache_time=0,
                show_alert=True,
            )
        else:
            try:
                await func(client, cb)
            except MessageNotModified:
                await cb.answer("🤔🧐")
            except Exception as e:
                print(format_exc())
                await cb.answer(
                    f"Ah Hayır, Bir Şeyler Doğru Değil. Lütfen Günlükleri Kontrol Edin!",
                    cache_time=0,
                    show_alert=True,
                )

    return wrapper


def inline_wrapper(func):
    async def wrapper(client, inline_query):
        users = await get_all_pros()
        if inline_query.from_user.id not in users:
            await client.answer_inline_query(
                inline_query.id,
                cache_time=1,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="Üzgünüm Dostum, Beni Kullanamazsın!",
                            input_message_content=InputTextMessageContent(
                                "**Hey!** Ben Senin İçin Değilim, Sadece Efendim İçin Çalışıyorum. Neden Kendi @ElectronUserBot'unuzu kurmuyorsunuz?"
                            ),
                        )
                    )
                ],
            )
        else:
            await func(client, inline_query)

    return wrapper


async def delete_or_pass(message):
    """Kendinden Olan Mesajı Sil Sadece İlet"""
    AFS = await sudo_list()
    if message.from_user.id in AFS:
        return message
    return await message.delete()


def humanbytes(size):
    """İnsanların Okuyabilmesi İçin Baytları Baytlara Dönüştür"""
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

def run_in_exc(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(exc_, lambda: f(*args, **kwargs))
    return wrapper


def time_formatter(milliseconds: int) -> str:
    """Time Formatter"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


async def progress(current, total, message, start, type_of_ps, file_name=None):
    """Dosya Yüklerken / İndirirken İlerlemeyi Göstermek İçin İlerleme Çubuğu - Normal"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**Dosya Adı:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


async def cb_progress(current, total, cb, start, type_of_ps, file_name=None):
    """Dosyayı Yüklerken / İndirirken İlerlemeyi Göstermek İçin İlerleme Çubuğu - Satır İçi"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await cb.edit_message_text(
                    "{}\n**Dosya Adı:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit_message_text("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


def get_text(message: Message) -> [None, str]:
    """Komutlardan Metin Çıkarma"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ terminalde komut çalıştır """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def edit_or_send_as_file(
    text: str,
    message: Message,
    client: Client,
    caption: str = "`Sonuç!`",
    file_name: str = "sonuç",
    parse_mode="md",
):
    """Uzun Metnin Sınırı Aşarsa Dosya Olarak Gönder Başka Mesajı Düzenle"""
    if not text:
        await message.edit("`Bekle, Ne?`")
        return
    if len(text) > 1024:
        await message.edit("`Çıktı Çok Büyük, Dosya Olarak Gönderiliyor!`")
        file_names = f"{file_name}.text"
        open(file_names, "w").write(text)
        await client.send_document(message.chat.id, file_names, caption=caption)
        await message.delete()
        if os.path.exists(file_names):
            os.remove(file_names)
        return
    else:
        return await message.edit(text, parse_mode=parse_mode)


async def iter_chats(client):
    """Tüm Sohbetlerinizi Yineleyin"""
    chats = []
    async for dialog in client.iter_dialogs():
        if dialog.chat.type in ["supergroup", "channel"]:
            chats.append(dialog.chat.id)
    return chats


async def fetch_audio(client, message):
    """Videolardan veya Sesin Kendisinden Ses Alın"""
    c_time = time.time()
    if not message.reply_to_message:
        await message.edit("`Bir Videoyu / Sesi Yanıtlayın.`")
        return
    warner_stark = message.reply_to_message
    if warner_stark.audio is None and warner_stark.video is None:
        await message.edit("`Biçim Desteklenmiyor`")
        return
    if warner_stark.video:
        await message.edit("`Video Detected, Converting To Audio !`")
        warner_bros = await message.reply_to_message.download(
            progress=progress, progress_args=(message, c_time, f"`Ses İndiriliyor!`")
        )
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a electron.mp3"
        await runcmd(stark_cmd)
        final_warner = "electron.mp3"
    elif warner_stark.audio:
        await message.edit("`İndirme Başlatıldı !`")
        final_warner = await message.reply_to_message.download(
            progress=progress, progress_args=(message, c_time, f"`Video İndiriliyor!`")
        )
    await message.edit("`Neredeyse Bitti!`")
    return final_warner
