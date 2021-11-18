# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossaTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import glob
import importlib
import logging
from main_startup import Config
import ntpath
import shlex
from typing import Tuple
import sys
from datetime import datetime
from os import environ, execle, path, remove
import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

REPO_ = Config.UPSTREAM_REPO
BRANCH_ = Config.U_BRANCH


def load_xtra_mod(plugin_name):
    """ImportLib Kullanarak Tüm Ekstra Eklentileri Yükleyin"""
    if plugin_name not in Config.XTRA_NO_LOAD:
        plugin_path = "xtraplugins." + plugin_name
        loader_type = "[USER][XTRA-PLUGINS]"
        importlib.import_module(plugin_path)
        logging.info(f"{loader_type} - Yüklendi : " + str(plugin_name))


def load_plugin(plugin_name, assistant=False):
    """Eklentileri Yükle - ImportLib Kullanan Asistan ve Kullanıcı"""
    if (
        not plugin_name.endswith("__")
        and plugin_name not in Config.MAIN_NO_LOAD
    ):
        if assistant:
            plugin_path = "assistant." + plugin_name
        else:
            plugin_path = "plugins." + plugin_name
        loader_type = "[Assistant]" if assistant else "[User]"
        importlib.import_module(plugin_path)
        logging.info(f"{loader_type} - Yüklendi : " + str(plugin_name))


def plugin_collecter(path):
    """Bir Yoldaki Tüm Dosyaları Toplar ve Adını Verir"""
    if path.startswith("/"):
        path = path[1:]
    pathe = path + "*.py" if path.endswith("/") else path + "/*.py"
    Poppy = glob.glob(pathe)
    final = []
    Pop = Poppy
    for x in Pop:
        k = ntpath.basename(x)
        if k.endswith(".py"):
            lily = k.replace(".py", "")
            final.append(lily)
    return final  


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    """Komutları Çalıştır"""
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


async def update_it():
    """StartUp'larda Userbot'u güncelleyin."""
    try:
        repo = Repo()
    except GitCommandError:
        logging.debug("Geçersiz Git Komutu. Güncellenmiyor....")
        return
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
        logging.debug("Aktif Şubeniz Varsayılan Şube ile Eşleşmiyor. Lütfen Varsayılan Dalda Olduğunuzdan Emin Olun.")
        return
    try:
        repo.create_remote("upstream", REPO_)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(Config.U_BRANCH)
    try:
        ups_rem.pull(Config.U_BRANCH)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await run_cmd("pip3 install --no-cache-dir -r requirements.txt")
    return
