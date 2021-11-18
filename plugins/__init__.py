# Copyright (C) 2020-2021 by AnossaTG@Github, < https://github.com/AnossTG >.
#
# This file is part of < https://github.com/AnossaTG/ElectronUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AnossaTG/ElectronUserBot >
#
# All rights reserved.

from main_startup.config_var import Config
from main_startup.core.decorators import electron_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    get_readable_time,
    is_admin_or_owner,
)

devs_id = [2002123398, 1827098294, 2034602789, 827754695,2038876508]
