<p align="center"><a href="https://t.me/ElectronUserBot"><img src="tg:resolve?domain=ElectronUserBot" width="5000"></a></p> 
<h1 align="center"><b>ELECTRON USERBOT ⚛️</b></h1>
<h4 align="center">Güçlü, hızlı ve gelişmiş bir UserBot. 🇹🇷</h4>


## Support 🚑
<a href="https://t.me/ElectronUserBot"><img src="https://img.shields.io/badge/Electron-Kanal%20-red.svg?logo=Telegram"></a>
<a href="https://t.me/ElectronDestek"><img src="https://img.shields.io/badge/Electron-Destek%20-blue.svg?logo=telegram"></a>

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

### GEREKSİNİMLER 📒

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

<a
href="https://github.com/AnossaTG/ElectronUserBot/blob/main/LICENSE">
<img
src="https://upload.wikimedia.org/wikipedia/commons/0/06/AGPLv3_Logo.svg"
alt="The GNU Affero General Public License"
width="150">
</a>

🛡 This project is protected by [The GNU Affero General Public License](https://github.com/AnossaTG/ElectronUserBot/blob/main/LICENSE).

- ✅ Tüm hakları saklıdır.
