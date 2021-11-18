# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU AFFERO GENERAL PUBLIC LICENSE".
# Please see < hhttps://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

nowtime=$(date)
echo "
ElectronUserBot

(C) @ElectronUserBot
@AnossaTG tarafından desteklenmektedir.
Zaman : $nowtime
"
update_and_install_packages () {
    apt -qq update -y
    apt -qq install -y --no-install-recommends \
        git \
        ffmpeg \
        mediainfo \
        unzip \
        wget \
        gifsicle 
  }
  
# Chrome Sürümü Hecks için Userge'a Teşekkürler 
install_helper_packages () {
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && apt -fqqy install ./google-chrome-stable_current_amd64.deb && rm google-chrome-stable_current_amd64.deb
    wget https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && chmod +x chromedriver && mv -f chromedriver /usr/bin/ && rm chromedriver_linux64.zip
    wget -O opencv.zip https://github.com/opencv/opencv/archive/master.zip && unzip opencv.zip && mv -f opencv-master /usr/bin/ && rm opencv.zip
    wget https://people.eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel -P ./bot_utils_files/ai_helpers/
}

ech_final () {
    echo "
    
=+---------------------------------------------------------+=
Deploy Başarılı.
Docker Görselleri İtiliyor, Lütfen Bekleyiniz.
Electron'u Kurduğunuz İçin Teşekkür Ederiz.
(C) @ElectronUserBot
=+---------------------------------------------------------+=

    "
}

_run_all () {
    update_and_install_packages
    install_helper_packages
    pip3 install –upgrade pip
    pip3 install --no-cache-dir -r requirements.txt
    ech_final
}

_run_all
