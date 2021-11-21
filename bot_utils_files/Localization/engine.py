# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

import logging
import os
import yaml     
import pathlib
from database.localdb import check_lang
from main_startup.config_var import Config
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

language_string = {}

class Engine:
    def __init__(self):
        self.path = "./bot_utils_files/Localization/strings/"
        
    def get_all_files_in_path(self, path):
        path = pathlib.Path(path)
        return [i.absolute() for i in path.glob("**/*")]

    def load_language(self):
        all_files = self.get_all_files_in_path(self.path)
        for filepath in all_files:
            with open(filepath) as f:
                data = yaml.safe_load(f)
                language_to_load = data.get("language")
                logging.debug(f"Loading : {language_to_load}")
                language_string[language_to_load] = data
        logging.debug("Tüm diller Yüklendi.")
        
    def get_string(self, string):
        lang_ = Electron.selected_lang
        return (
            language_string.get(lang_).get(string)
            or f"**404_STRING_BULUNAMADI :** `Dize {string}, {lang} Dize Dosyasında Bulunamadı. - Lütfen @ElectronDestek`e Bildirin"
        )
