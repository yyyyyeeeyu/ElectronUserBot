<p align="center"><a href="https://t.me/ElectronUserBot"><img src="tg:resolve?domain=ElectronUserBot" width="5000"></a></p> 
<h1 align="center"><b>ELECTRON USERBOT ⚛️</b></h1>
<h4 align="center">Güçlü, hızlı ve gelişmiş bir UserBot. 🇹🇷</h4>

## **💠 Bɪʟɢɪ**

```
    Electron UserBot,
-   Telegram'da hesabınızı,
-   gruplarınızı & kanallarınızı
-   yönetmenize yardımcı olur.
-   Telegram'ı eğlenceli hale getirmek
-   ve kullanımını kolaylaştırmak içindir.
```
```
💡  Electron UserBot sebebiyle;
🚫  Telegram hesabınız kısıtlanabilir.
🔔  AYRICA:
-   Gruplara spam gönderip,
-   Telegram'a şikayet edildiğinizde
-   ve hesabınız silindiğinde
-   BİZİ SUÇLAMAYIN!
⛔️  Electron UserBot ve yöneticileri,
-   hesabınız için hiçbir sorumluluk kabul etmemektedir.
📍  Electron UserBot kurarak,
-   tüm bu sorumlulukları kabul etmiş olursunuz.
```
## Support 🚑
<a href="https://t.me/ElectronUserBot"><img src="https://img.shields.io/badge/Electron-Kanal%20-red.svg?logo=Telegram"></a>
<a href="https://t.me/ElectronDestek"><img src="https://img.shields.io/badge/Electron-Destek%20-blue.svg?logo=telegram"></a>


### GEREKSİNİMLER

```
[+] Tüm Bu Zorunlu Varsları Eklediğinizden Emin Olun.
    [-] API_ID: Bu değeri https://my.telegram.org adresinden alabilirsiniz.
    [-] API_HASH : Bu değeri https://my.telegram.org adresinden alabilirsiniz.
    [-] STRINGSESSION : Dize Oturumunuz, Bunu Repl'it der alabilirsiniz
    [-] MONGO_DB : Mongo DB Database URL'niz
    [-] LOG_GRP: Günlük Grubunuz/Kanal Sohbet İD. Bu Çok Önemlidir ve Bu Olmadan Bazı Modüller İyi Çalışmaz!
[+] ElectronUserBot tüm zorunlu değişkenleri ayarlamadan çalışmayacaktır.
```

 # Örnekler - Pluginler 👊
 
### Pluginler 🔧
 
 ```python3
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply
@electron_on_cmd(['selam'],
    cmd_help={
    "help": "Bu bir test",
    "example": "{ch}selam"
    })
async def hello_world(client, message):
    mg = await edit_or_reply(message, "'Selam Dünya!`")
```
### Özel Filtreler 📣

```python3
from main_startup.core.decorators import listen
@listen(filters.mentioned)
async def mentioned_(client, message):
    await message.reply_text("`Selam Dünya! Bu arada neden benden bahsettiniz?`")
```
# Licence 📋

[![GNU GPLv3 Image](https://www.gnu.org/graphics/gplv3-127x51.png)](http://www.gnu.org/licenses/gpl-3.0.en.html)  

* Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.

English | Electron is Free Software: You can use, study share and improve it at your
will. Specifically you can redistribute and/or modify it under the terms of the
[GNU General Public License](https://www.gnu.org/licenses/gpl.html) as
published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. 

Türkce | Electron Özgür Bir Yazılımdır: İstediğiniz zaman kullanabilir, paylaşabilir ve geliştirebilirsiniz.
niyet. Özellikle, onu yeniden dağıtabilir ve/veya aşağıdaki koşullar altında değiştirebilirsiniz:
[GNU Genel Kamu Lisansı](https://www.gnu.org/licenses/gpl.html) olarak
Özgür Yazılım Vakfı tarafından yayınlanan, Lisansın 3. sürümü veya
(isteğe bağlı olarak) herhangi bir sonraki sürüm.
