# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

import os
import time
from datetime import datetime

import gtts
import requests
from google_trans_new import google_translator
from googletrans import LANGUAGES
from gtts import gTTS
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from langdetect import detect
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.bot_users import add_user, check_user, get_all_users
from main_startup import bot, start_time
from main_startup.config_var import Config
from main_startup.helper_func.assistant_helpers import (
    _check_admin,
    _check_owner_or_sudos,
)
from main_startup.helper_func.basic_helpers import get_all_pros, get_readable_time


@bot.on_message(filters.command(["start"]) & filters.incoming)
async def start(client, message):
    all_user_s = await get_all_pros()
    starkbot = client.me
    bot_name = starkbot.first_name
    bot_username = starkbot.username
    firstname = message.from_user.first_name
    user_id = message.from_user.id
    starttext = f"`Merhaba, {firstname}! Tanıştığımıza memnun oldum, \nBen {bot_name}, \nSahibim İçin Konuşacak ve Birçok Şey Yapacak Güçlü Bir Yardımcı Bot'um!`. \n\n[Electron Userbot](t.me/ElectronUserBot) tarafından destekleniyor"
    mypic = Config.ASSISTANT_START_PIC
    if user_id not in all_user_s:
        await client.send_photo(
            message.chat.id,
            mypic,
            starttext,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Bana yardım et ❓", url="t.me/ElectronUserBot")]]
            ),
        )
        kok = await check_user(user_id)
        if not kok:
            await add_user(user_id)
    else:
        message87 = f"Merhaba Sahip, Ben {bot_name}, Asistanınız! \Bugün ne yapmak istersin?"
        await client.send_photo(
            message.chat.id,
            mypic,
            message87,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Beni Gruba Ekle 👥",
                            url=f"t.me/{bot_username}?startgroup=true",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Asistan için Komutlar", callback_data="cmdgiv"
                        )
                    ],
                ]
            ),
        )


@bot.on_callback_query(filters.regex("cmdgiv"))
async def cmdgiv(client, cb):
    grabon = "Merhaba İşte Bazı Komutlar \n➤ /start - Hayatta olup olmadığımı kontrol edin \n➤ /ping - Pingimi gösterir \n➤ /tr (dil kodu) \n➤ /tts (dil kodu) \n➤ /promote - Bir kullanıcıya yetki verin \n➤ /broadcast - Bottaki Tüm Kullanıcılara Mesaj Gönderir \n➤ /id - Grup ve Kullanıcının İD'sini gösterir \n➤ /info - Kullanıcının INFO'sunu gösterir \n➤ /users - Kullanıcıların Listesini dB Olarak Al."
    await cb.edit_message_text(grabon)


@bot.on_message(filters.command(["alive"]) & filters.incoming)
@_check_owner_or_sudos
async def alive(client, message):
    lol = client.me
    await message.reply(
        f"`{message.from_user.first_name}, Yaşıyorum. Yardıma mı ihtiyacın var? Nasılsın? 🤟`"
    )


@bot.on_message(filters.command(["help"]) & filters.incoming)
@_check_owner_or_sudos
async def fuckinhelp(client, message):
    grabon = "Merhaba İşte Bazı Komutlar \n➤ /start - Hayatta olup olmadığımı kontrol edin \n➤ /ping - Pong! \n➤ /tr (lang kodu) \n➤ /tts (lang kodu) \n➤ /promote - Bir kullanıcıyı terfi ettir \n➤ /demote - Bir kullanıcıyı indirgeme \n➤ /broadcast - Tüm Kullanıcılara Mesaj Gönderir Bot \n➤ /id - Grubun ve Kullanıcının İD'sini gösterir \n➤ /info - Kullanıcının INFO'sunu gösterir \n➤ /users - Kullanıcıların Listesini dB Olarak Al."
    await message.reply(grabon)


@bot.on_message(filters.regex("users") & filters.incoming & filters.private)
@_check_owner_or_sudos
async def user_s(client, message):
    users_list = "Bottaki Toplam Kullanıcı Listesi. \n\n"
    total_users = await get_all_users()
    for starked in total_users:
        users_list += ("==> {} \n").format(int(starked.get("user_id")))
    with open("users.txt", "w") as f:
        f.write(users_list)
    await message.reply_document("users.txt", caption="dB'nizdeki Kullanıcılar")


@bot.on_message(filters.command(["promote"]) & filters.group)
@_check_admin
async def promote_me(client, message):
    pablo = await message.reply("İşleme...")
    if not message.reply_to_message:
        await pablo.edit("Lütfen Bir Kullanıcıya Cevap Verin")
        return
    lol = client.me
    user_s = await message.chat.get_member(lol.id)
    if user_s.status not in ("creator", "administrator"):
        await pablo.edit("`Yönetici yapmak için Yeterli İznim Yok!`")
        return
    text_to_return = message.text
    try:
        title = message.text.split(None, 1)[1]
    except IndexError:
        title = None
    await pablo.edit("`Bu Kullanıcıyı Yönetici yapıyorum!`")
    try:
        await client.promote_chat_member(
            message.chat.id, message.reply_to_message.from_user.id
        )
    except:
        await pablo.edit("`Yönetici yapmak için Yeterli İznim Yok!`")
        return
    await pablo.edit("`Kullanıcıyı Başarıyla Yönetici yaptım!`")
    if title:
        await client.set_administrator_title(
            message.chat.id, message.reply_to_message.from_user.id, title
        )


@bot.on_message(filters.command(["demote"]) & filters.group)
@_check_admin
async def demote_you(client, message):
    pablo = await message.reply("İşleniypr...")
    if not message.reply_to_message:
        await pablo.edit("Lütfen Bir Kullanıcıya Cevap Verin")
        return
    lol = client.me
    user_s = await message.chat.get_member(lol.id)
    if user_s.status not in ("creator", "administrator"):
        await pablo.edit("`Yetki almak için Yeterli İznim Yok!`")
        return
    await pablo.edit("`Kullanıcının yetkisi alındı!`") 
    try:
        await client.promote_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            is_anonymous=False,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        )
    except:
        await pablo.edit("`Yetki almak için Yeterli İznim Yok!`")
        return
    await pablo.edit("`Kullanıcının yetkisi alındı!`")


@bot.on_message(filters.command(["id"]) & filters.incoming)
async def id(client, message):
    if message.reply_to_message is None:
        await message.reply(f"Bu sohbetin İD'si: {message.chat.id}")
    else:
        test = f"Yanıtlanan Kullanıcının İD'si: {message.reply_to_message.from_user.id}\n\nBu sohbetin İD'si: {message.chat.id}"
        await message.reply(test)


@bot.on_message(filters.command(["info"]) & filters.incoming)
async def info(client, message):
    if message.reply_to_message:
        username = message.reply_to_message.from_user.username
        id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        user_link = message.reply_to_message.from_user.mention
    else:
        username = message.from_user.username
        id = message.from_user.id
        first_name = message.from_user.first_name
        user_link = message.from_user.mention
    if username:
        username = f"@{username}"
        text = f"""
<b>Kullanıcı bilgisi</b>:
İD: <code>{id}</code>
Ad: {first_name}
Kullanıcı adı: {username}
Kullanıcı bağlantısı: {user_link}"""
    else:
        text = f"""
<b>Kullanıcı bilgisi</b>:
İD: <code>{id}</code>
Ad: {first_name}
Kullanıcı bağlantısı: {user_link}"""
    await message.reply(text, parse_mode="HTML")


@bot.on_message(filters.command(["ping"]) & filters.incoming)
@_check_owner_or_sudos
async def ping(client, message):
    uptime = get_readable_time((time.time() - start_time))
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await client.send_message(
        message.chat.id,
        f"**█▀█ █▀█ █▄░█ █▀▀ █ \n█▀▀ █▄█ █░▀█ █▄█ ▄**\n ➲ `{ms}` \n ➲ `{uptime}`",
    )


@bot.on_message(filters.command(["tts"]) & filters.incoming)
@_check_owner_or_sudos
async def tts_(client, message):
    stime = time.time()
    text_to_return = message.text
    lol = await message.reply("İşleniyor....")
    try:
        lang = message.text.split(None, 1)[1]
    except IndexError:
        lang = "tr"
    if not message.reply_to_message:
        await lol.edit("`Metne Dönüştürmek İçin Metne Cevap Ver!`")
        return
    text = message.reply_to_message.text
    language = lang
    kk = gtts.lang.tts_langs()
    if not kk.get(language):
        await lol.edit("`Desteklenmeyen Dil!`")
        return
    await client.send_chat_action(message.chat.id, "record_audio")
    tts = gTTS(text, lang=language)
    tts.save(f"{kk.get(language)}.ogg")
    google_translator()
    dec_s = detect(text)
    etime = time.time()
    hmm_time = round(etime - stime)
    duration = 0
    metadata = extractMetadata(createParser(f"{kk.get(language)}.ogg"))
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    owoc = f"**TTS** \n**Algılanan Metin Dili :** `{dec_s.capitalize()}` \n**Konuşma Metni :** `{kk.get(language)}` \n**Alınan Zaman : ** `{hmm_time}s` \n__Powered By @ElectronUserBot__"
    await message.reply_audio(
        audio=f"{kk.get(language)}.ogg", caption=owoc, duration=duration
    )
    await client.send_chat_action(message.chat.id, action="cancel")
    os.remove(f"{kk.get(language)}.ogg")
    await lol.delete()


@bot.on_message(filters.command(["tr"]) & filters.incoming)
@_check_owner_or_sudos
async def tr(client, message):
    text_to_return = message.text
    try:
        lang = message.text.split(None, 1)[1]
    except IndexError:
        lang = "en"
    if not message.reply_to_message:
        await message.reply("Çevirilecek Metne Cevap Ver")
        return
    text = message.reply_to_message.text
    translator = google_translator()
    source_lan = detect(text)
    transl_lan = LANGUAGES[lang]
    translated = translator.translate(text, lang_tgt=lang)
    tr_text = f"""**Kaynak ({source_lan.capitalize()})**:
`{text}`
**Çeviri ({transl_lan.capitalize()})**:
`{translated}`"""
    if len(tr_text) >= 4096:
        url = "https://del.dog/documents"
        r = requests.post(url, data=tr_text.encode("UTF-8")).json()
        url2 = f"https://del.dog/{r['key']}"
        tr_text = (
            f"Çevrilmiş Metin Çok Büyüktü, O yüzden [burada]({url2}) bulabilirsiniz.."
        )
    await message.reply(tr_text)


@bot.on_message(filters.command(["broadcast"]) & filters.incoming)
@_check_owner_or_sudos
async def broadcast(client, message):
    msg = None
    lol = await message.reply("`İşleniyor!`")
    if message.reply_to_message:
        msg = True
    else:
        await lol.edit("`Lütfen Yayın İçin Mesajı Cevaplayınız!`")
        return
    if msg is None:
        await lol.edit("`Lütfen Yayın İçin Mesajı Cevaplayınız!`")
        return
    s = 0
    f = 0
    total_users = await get_all_users()
    tett = "**▶ Bir Yayın Mesajı Aldınız :**"
    for user in total_users:
        user_id = user.get("user_id")
        try:
            await client.send_message(user_id, tett)
            await message.reply_to_message.copy(user_id)
            s += 1
        except:
            f += 1
    if f > 0:
        await lol.edit(
            f"{s} kullanıcıya başarıyla yayınlandı. {f} kullanıcıya Yayınlanamadı. Belki Botu Engellemişlerdir"
        )
    else:
        await lol.edit(f"{s} kullanıcıya başarıyla mesaj yayınlandı.")
