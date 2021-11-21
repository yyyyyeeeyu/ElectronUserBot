# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

import logging
import re
import string
from random import choice
import sys
#import datetime
from datetime import datetime
from os import environ, execle, path, remove
import platform
from bot_utils_files.Localization.engine import language_string
import re
import socket
import time
import uuid
import psutil
from pyrogram import __version__
import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
import requests
from bs4 import BeautifulSoup
from pyrogram import __version__, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)
from tinydb import Query, TinyDB
from main_startup.core.startup_helpers import run_cmd
from main_startup import CMD_LIST, XTRA_CMD_LIST, Electron, bot, electron_version
from main_startup.config_var import Config
from youtubesearchpython import SearchVideos
from main_startup.helper_func.basic_helpers import (
    cb_wrapper,
    humanbytes,
    get_all_pros,
    inline_wrapper,
    paginate_help,
)

import os
from main_startup.helper_func.assistant_helpers import _dl, download_yt
from pyrogram.types import InputMediaDocument, InputMediaVideo, InputMediaAudio
from googletrans import LANGUAGES

from database.localdb import set_lang

db_m = TinyDB("./main_startup/Cache/secret.json")
db_s = TinyDB("./main_startup/Cache/not4u.json")


REPO_ = Config.UPSTREAM_REPO
BRANCH_ = Config.U_BRANCH


@bot.on_inline_query()
@inline_wrapper
async def owo(client, inline_query):
    string_given = inline_query.query.lower()
    if string_given.startswith("not4u"):
        if ";" not in string_given:
            return
        ok = string_given.split(" ", maxsplit=1)[1]
        user, msg = ok.split(";")
        fu = int(user) if user.isdigit() else user
        try:
            ui = await Electron.get_users(fu)
        except BaseException as e:
            logging.error(str(e))
            return
        owo = (
            f"@{ui.username}"
            if ui.username
            else f"[{ui.first_name}](tg://user?id={ui.id})"
        )
        chars = string.hexdigits
        randomc = "".join(choice(chars) for _ in range(4))
        stark_data = {"secret_code": randomc, "id": ui.id, "msg": msg}
        db_s.insert(stark_data)
        texts = f"{owo} Hariç Herkes Bu Mesajı Okuyabilir. \nMesajı Kontrol Etmek İçin Aşağıya Tıklayın! \n**Not :** `Yalnızca O Açamaz!`"
        ok_s = [
            (
                results.append(
                    title="OwO! Senin için değil",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Mesajı Göster !", callback_data=f"nu_{randomc}"
                                )
                            ]
                        ]
                    ),
                    input_message_content=InputTextMessageContent(texts),
                )
            )
        ]
        await client.answer_inline_query(inline_query.id, cache_time=0, results=ok_s)
    elif string_given.startswith("yt"):
        results = []
        try:
            input = string_given.split(" ", maxsplit=1)[1]
        except:
            return
        search = SearchVideos(str(input), offset=1, mode="dict", max_results=50)
        rt = search.result()
        result_s = rt["search_result"]
        for i in result_s:
            url = i["link"]
            vid_title = i["title"]
            yt_id = i["id"]
            uploade_r = i["channel"]
            views = i["views"]
            thumb = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
            capt = f"""
**Video Başlığı :** `{vid_title}`
**Bağlantı :** `{url}`
**Yükleyici :** `{uploade_r}`
**Görüntülemeler :** `{views}`
            """
            results.append(
                InlineQueryResultPhoto(
                    photo_url=thumb,
                    title=vid_title,
                    caption=capt,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="İndir - Audio",
                                    callback_data=f"ytdl_{url}_audio"
                                ),
                                InlineKeyboardButton(
                                    text="İndir - Video",
                                    callback_data=f"ytdl_{url}_video"
                                )
                            ]
                        ]
                    ),
                )
            )
        await client.answer_inline_query(inline_query.id, cache_time=0, results=results)
    elif string_given.startswith("git"):
        try:
            input_ = string_given.split(" ", maxsplit=1)[1]
        except:
            return
        results = []
        r = requests.get("https://api.github.com/search/repositories", params={"q": input_})
        lool = r.json()
        if lool.get("total_count") == 0:
            return
        lol = lool.get("items")
        for X in lol:
            qw = X
            txt = f"""
<b>Ad :</b> <i>{qw.get("name")}</i>
<b>Tam Ad :</b> <i>{qw.get("full_name")}</i>
<b>Bağlantı :</b> {qw.get("html_url")}
<b>Fork Sayısı :</b> <i>{qw.get("forks_count")}</i>
<b>Açık Sorunlar :</b> <i>{qw.get("open_issues")}</i>
"""
            if qw.get("description"):
                txt += f'\n<b>Açıklama :</b> <code>{qw.get("description")}</code>'
            if qw.get("language"):
                txt += f'\n<b>Dil :</b> <code>{qw.get("language")}</code>'
            if qw.get("size"):
                txt += f'\n<b>Boyut :</b> <code>{qw.get("size")}</code>'
            if qw.get("score"):
                txt += f'\n<b>Skor :</b> <code>{qw.get("score")}</code>'
            if qw.get("created_at"):
                txt += f'\n<b>Oluşturulma Tarihi :</b> <code>{qw.get("created_at")}</code>'
            if qw.get("archived") == True:
                txt += f"\n<b>Bu Proje Arşivlendi</b>"

            results.append(
                InlineQueryResultArticle(
                   thumb_url="https://simpleicons.org/icons/github.svg",
                   url=qw.get("html_url"),
                   description=qw.get("description", "Açıklama yok"),
                   title = qw.get("name"),
                   input_message_content=InputTextMessageContent(txt, disable_web_page_preview=True)
                )
             )
        await client.answer_inline_query(inline_query.id, cache_time=0, results=results)
    elif string_given.startswith("whisper"):
        if ";" not in string_given:
            return
        ok = string_given.split(" ", maxsplit=1)[1]
        user, msg = ok.split(";")
        fu = int(user) if user.isdigit() else user
        try:
            ui = await Electron.get_users(fu)
        except BaseException as e:
            logging.error(str(e))
            return
        owo = (
            f"@{ui.username}"
            if ui.username
            else f"[{ui.first_name}](tg://user?id={ui.id})"
        )
        chars = string.hexdigits
        randomc = "".join(choice(chars) for _ in range(4))
        stark_data = {"secret_code": randomc, "id": ui.id, "msg": msg}
        db_m.insert(stark_data)
        texts = f"{owo} İçin Bir Fısıltı Gönderildi. \nMesajı Kontrol Etmek İçin Aşağıya Tıklayın! \n**Not :** `Yalnızca O Açabilir!`"
        ok_s = [
            (
                InlineQueryResultArticle(
                    title="Şşşt! Bu Gizli Bir Mesajdır",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Mesajı Göster !", callback_data=f"sc_{randomc}"
                                )
                            ]
                        ]
                    ),
                    input_message_content=InputTextMessageContent(texts),
                )
            )
        ]
        await client.answer_inline_query(inline_query.id, cache_time=0, results=ok_s)
    elif string_given.startswith("help"):
        total_ = len(CMD_LIST)
        bttn = [
            [
                InlineKeyboardButton(
                    text="Komut Yardımı", callback_data=f"make_cmd_buttons"
                )
            ],
            [
             InlineKeyboardButton(
                    text="UserBot'u yeniden başlatın", callback_data=f"restart_bot"
                )
            ],  
            [
             InlineKeyboardButton(
                    text="UserBot'u Güncelle", callback_data=f"updTe_bot"
                )
            ],
            [
             InlineKeyboardButton(
                    text="Sistem Bilgileri", callback_data=f"sys_info"
                )
            ],
            [
             InlineKeyboardButton(
                    text="UserBot Dilini Değiştir", callback_data=f"change_lang"
                )
            ],
        ]
        if Config.LOAD_UNOFFICIAL_PLUGINS:
            total_ = len(XTRA_CMD_LIST) + len(CMD_LIST)
        nice_text = f"**ElectronUserBot Komutları** \n**Electron Sürümü :** __{electron_version}__ \n**PyroGram Sürümü :** __{__version__}__ \n**Yüklenen Toplam Eklenti Sayısı:** __{total_}__"
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                (
                    InlineQueryResultArticle(
                        title="Yardım Yazısı!",
                        reply_markup=InlineKeyboardMarkup(bttn),
                        input_message_content=InputTextMessageContent(nice_text),
                    )
                )
            ],
        )

@bot.on_callback_query(filters.regex(pattern="set_lang_(.*)"))
@cb_wrapper
async def st_lang(client, cb):
    lang = cb.matches[0].group(1)
    await set_lang(lang)
    str_ = f"**Electron Dili Değiştirildi** `{LANGUAGES[lang].title()}` \n`Değişiklikleri Güncellemek İçin Lütfen Yeniden Başlatın!`"
    await cb.edit_message_text(str_)

@bot.on_callback_query(filters.regex(pattern="change_lang"))
@cb_wrapper
async def change_lang(client, cb):
    nice_text = "Aşağıdan Bir Dil Seçin:"
    bttns_d = [
        [
            InlineKeyboardButton(
                text=LANGUAGES[lang_].title(),
                callback_data=f"set_lang_{lang_}",
            )
        ]
        for lang_ in language_string.keys()
    ]

    await cb.edit_message_text(nice_text, reply_markup=InlineKeyboardMarkup(bttns_d))
    

@bot.on_callback_query(filters.regex(pattern="ytdl_(.*)_(video|audio)"))
async def yt_dl_video(client, cb):
    await cb.edit_message_text("`Feature Disabled Temp.`")
    """
    url = cb.matches[0].group(1)
    audio_or_video = cb.matches[0].group(2)
    if audio_or_video == "video":
        file_name, downloaded_thumb, name, dur, u_date, uploader, views = await download_yt(url, as_video=True)
    else:
        file_name, downloaded_thumb, name, dur, u_date, uploader, views = await download_yt(url, as_video=False)
    if not os.path.exists(file_name):
        await cb.edit_message_text(file_name)
        return
    await cb.edit_message_text(f"`Downloaded : {name} | Now Uploading....`")
    import datetime
    f_size = humanbytes(os.stat(file_name).st_size)
    if audio_or_video == "video":
        file_ = InputMediaVideo(file_name, thumb=downloaded_thumb, supports_streaming=True, duration=dur, caption=caption)
    else:
        file_ = InputMediaAudio(file_name, performer=uploader, title=name, thumb=downloaded_thumb, duration=dur, caption=caption)
    await cb.edit_message_media(file_)
    if os.path.exists(file_name):
        os.remove(file_name)
    """

@bot.on_callback_query(filters.regex(pattern="sc_(.*)"))
async def no_horny(client, cb):
    o = await get_all_pros()
    data_m = cb.matches[0].group(1)
    stark_moment = Query()
    sstark = db_m.search(stark_moment.secret_code == data_m)
    if sstark == []:
        await cb.answer(
            "OwO, Mesaj Sunucudan Silinmiş Görünüyor :(",
            cache_time=0,
            show_alert=True,
        )
        return
    id_s = sstark[0]["id"]
    o.append(int(id_s))
    if cb.from_user.id not in o:
        await cb.answer(
            "Bu Mesaj Sana Değil, Bu Bir Sır.!",
            cache_time=0,
            show_alert=True,
        )
        return
    await cb.answer(sstark[0]["msg"], cache_time=0, show_alert=True)


@bot.on_callback_query(filters.regex(pattern="nu_(.*)"))
async def nothing_here(client, cb):
    data_m = cb.matches[0].group(1)
    stark_moment = Query()
    sstark = db_s.search(stark_moment.secret_code == data_m)
    if sstark == []:
        await cb.answer(
            "OwO, Mesaj Sunucudan Silinmiş Görünüyor :(",
            cache_time=0,
            show_alert=True,
        )
        return
    id_s = sstark[0]["id"]
    if cb.from_user.id == int(id_s):
        await cb.answer(
            "Siz Hariç Herkes Bu Mesajı Okuyabilir. Hehe!",
            cache_time=0,
            show_alert=True,
        )
        return
    await cb.answer(sstark[0]["msg"], cache_time=0, show_alert=True)
    
    
@bot.on_callback_query(filters.regex(pattern="backO_to_help_menu"))
@cb_wrapper
async def black_menu(client, cb):
    total_ = len(CMD_LIST)
    bttn = [
            [
                InlineKeyboardButton(
                    text="Komut Yardımı", callback_data=f"make_cmd_buttons"
                )
            ],
            [
             InlineKeyboardButton(
                    text="UserBot'u yeniden başlatın", callback_data=f"restart_bot"
                )
            ],  
            [
             InlineKeyboardButton(
                    text="UserBot'u Güncelle", callback_data=f"updTe_bot"
                )
            ],
            [
             InlineKeyboardButton(
                    text="Sistem Bilgileri", callback_data=f"sys_info"
                )
            ],
        [
             InlineKeyboardButton(
                    text="UserBot Dilini Değiştir", callback_data=f"change_lang"
                )
            ],
        ]
    if Config.LOAD_UNOFFICIAL_PLUGINS:
        total_ = len(XTRA_CMD_LIST) + len(CMD_LIST)
    nice_text = f"**ElectronUserBot Komutları** \n**Electron Sürümü :** __{electron_version}__ \n**PyroGram Sürümü :** __{__version__}__ \n**Yüklenen Toplam Eklenti Sayısı:** __{total_}__"
    await cb.edit_message_text(nice_text, reply_markup=InlineKeyboardMarkup(bttn))

@bot.on_callback_query(filters.regex(pattern="make_cmd_buttons"))
@cb_wrapper
async def cmd_buutton(client, cb):
    bttn = [
            [
                InlineKeyboardButton(
                    text="Ana Komut Yardımı", callback_data=f"make_basic_button_True"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Geri 🔙", callback_data=f"backO_to_help_menu"
                )
            ]
        ]
    if Config.LOAD_UNOFFICIAL_PLUGINS:
        total_ = len(XTRA_CMD_LIST) + len(CMD_LIST)
        bttn = [
                [
                    InlineKeyboardButton(
                        text="Xtra Komutu Yardımı b ",
                        callback_data=f"make_basic_button_False",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Ana Komut Yardımı",
                        callback_data=f"make_basic_button_True",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Geri 🔙", callback_data=f"backO_to_help_menu"
                    )
                ]
            ]
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(bttn))

@bot.on_callback_query(filters.regex(pattern="restart_bot"))
@cb_wrapper
async def roaststart(client, cb):
    bttn = [
        [
                InlineKeyboardButton(
                    text="Geri 🔙", callback_data=f"backO_to_help_menu"
                )
            ]
    ]
    await cb.edit_message_text("`Lütfen Bekleyin, Yeniden Başlatılıyor... Bu Biraz Zaman Alabilir`", reply_markup=InlineKeyboardMarkup(bttn))
    args = [sys.executable, "-m", "main_startup"]
    execle(sys.executable, *args, environ)
    exit()

@bot.on_callback_query(filters.regex(pattern="updTe_bot"))
@cb_wrapper
async def update_it(client, cb):
    bttn = [
        [
                InlineKeyboardButton(
                    text="Geri 🔙", callback_data=f"backO_to_help_menu"
                )
            ]
    ]
    await cb.edit_message_text("`Güncelleniyor Lütfen Bekleyin!`", reply_markup=InlineKeyboardMarkup(bttn))
    try:
        repo = Repo()
    except GitCommandError:
        return await cb.edit_message_text(
            "Geçersiz Git Komutu. Lütfen Bu Hatayı `@ElectronUserBot` Adresine Bildirin",
            reply_markup=InlineKeyboardMarkup(bttn)
        )
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "upstream" in repo.remotes:
            origin = repo.remote("upstream")
        else:
            origin = repo.create_remote("upstream", REPO_)
        origin.fetch()
        repo.create_head(Config.U_BRANCH, origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    if repo.active_branch.name != Config.U_BRANCH:
        return await cb.edit_message_text(
            f"`Görünüşe göre Özel Dal Kullanıyorsunuz - {repo.active_branch.name}! Bu Güncelleyici İşlevini Yapmak İçin Lütfen {Config.U_BRANCH} Sürümüne Geçin!`", reply_markup=InlineKeyboardMarkup(bttn))
    try:
        repo.create_remote("upstream", REPO_)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(Config.U_BRANCH)
    if not Config.HEROKU_URL:
        try:
            ups_rem.pull(Config.U_BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await run_cmd("pip3 install --no-cache-dir -r requirements.txt")
        await cb.edit_message_text("`Başarıyla Güncellendi! Yeniden Başlamam İçin Bana Bir Dakika Verin!`", reply_markup=InlineKeyboardMarkup(bttn))
        args = [sys.executable, "-m", "main_startup"]
        execle(sys.executable, *args, environ)
        exit()
        return
    else:
        await cb.edit_message_text("`Heroku Tespit Edildi! İtiyor, Lütfen Durun!'", reply_markup=InlineKeyboardMarkup(bttn))
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(Config.HEROKU_URL)
        else:
            remote = repo.create_remote("heroku", Config.HEROKU_URL)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except BaseException as error:
            return await cb.edit_message_text(f"**Güncelleyici Hatası** \nTraceBack : `{error}`", reply_markup=InlineKeyboardMarkup(bttn))

@bot.on_callback_query(filters.regex(pattern="sys_info"))
@cb_wrapper
async def fuck_arch_btw(client, cb):
    bttn = [
        [
                InlineKeyboardButton(
                    text="Geri 🔙", callback_data=f"backO_to_help_menu"
                )
            ]
    ]
    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    ram = humanbytes(round(psutil.virtual_memory().total))
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    du = psutil.disk_usage(client.workdir)
    psutil.disk_io_counters()
    disk = f"{humanbytes(du.used)} / {humanbytes(du.total)} " f"({du.percent}%)"
    cpu_len = len(psutil.Process().cpu_affinity())
    neat_msg = f"""**Sistem bilgisi**
    
**PlatForm :** `{splatform}`
**PlatForm - Sürüm:** `{platform_release}`
**PlatFork - Sürüm :** `{platform_version}`
**Mimarlık :** `{architecture}`
**Ana bilgisayar adı :** `{hostname}`
**IP :** `{ip_address}`
**Mac :** `{mac_address}`
**İşlemci :** `{processor}`
**Ram : ** `{ram}`
**CPU :** `{cpu_len}`
**CPU FREK :** `{cpu_freq}`
**DİSK :** `{disk}`
    """
    await cb.edit_message_text(neat_msg, reply_markup=InlineKeyboardMarkup(bttn))



@bot.on_callback_query(filters.regex(pattern="make_basic_button_(True|False)"))
@cb_wrapper
async def wow_nice(client, cb):
    nice = cb.matches[0].group(1) != "False"
    if not nice:
        v_t = XTRA_CMD_LIST
        bttn = paginate_help(0, XTRA_CMD_LIST, "helpme", is_official=nice)
    else:
        v_t = CMD_LIST
        bttn = paginate_help(0, CMD_LIST, "helpme", is_official=nice)
    await cb.edit_message_text(
        f"Komut Listesi ve Yardım \n**Toplam Komutlar :** `{len(v_t)}` \n**(C) @ElectronUserBot**",
        reply_markup=InlineKeyboardMarkup(bttn),
    )


@bot.on_callback_query(filters.regex(pattern="cleuse"))
@cb_wrapper
async def close_it_please(client, cb):
    await cb.edit_message_text("**Yardım Menüsünü kapat**!")


@bot.on_callback_query(filters.regex(pattern="backme_(.*)_(True|False)"))
@cb_wrapper
async def get_back_vro(client, cb):
    page_number = int(cb.matches[0].group(1))
    is_official = cb.matches[0].group(2) != "False"
    cmd_list = CMD_LIST if is_official else XTRA_CMD_LIST
    buttons = paginate_help(page_number, cmd_list, "helpme", is_official=is_official)
    nice_text = f"**ElectronUserBot Komutları ve Yardım Menüsü!** \n\n**Electron:** __{electron_version}__ \n**PyroGram Sürümü :** __{__version__}__ \n**Yüklenen Toplam Plugin Sayısı :** __{len(CMD_LIST)}__"
    await cb.edit_message_text(nice_text, reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(pattern="us_plugin_(.*)_(True|False)"))
@cb_wrapper
async def give_plugin_cmds(client, cb):
    plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
    is_official = cb.matches[0].group(2) != "False"
    cmd_list = CMD_LIST if is_official else XTRA_CMD_LIST
    help_string = f"**💡 PLUGIN ADI 💡 :** `{plugin_name}` \n{cmd_list[plugin_name]}"
    help_string += "\n\n**(C) @ElectronUserBot** ".format(plugin_name)
    await cb.edit_message_text(
        help_string,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Geri dön",
                        callback_data=f"backme_{page_number}_{is_official}",
                    )
                ]
            ]
        ),
    )


@bot.on_callback_query(filters.regex(pattern="helpme_next\((.+?)\)_(True|False)"))
@cb_wrapper
async def give_next_page(client, cb):
    current_page_number = int(cb.matches[0].group(1))
    is_official = cb.matches[0].group(2) != "False"
    cmd_list = CMD_LIST if is_official else XTRA_CMD_LIST
    buttons = paginate_help(
        current_page_number + 1, cmd_list, "helpme", is_official=is_official
    )
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(pattern="helpme_prev\((.+?)\)_(True|False)"))
@cb_wrapper
async def give_old_page(client, cb):
    current_page_number = int(cb.matches[0].group(1))
    is_official = cb.matches[0].group(2) != "False"
    cmd_list = CMD_LIST if is_official else XTRA_CMD_LIST
    buttons = paginate_help(
        current_page_number - 1, cmd_list, "helpme", is_official=is_official
    )
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
