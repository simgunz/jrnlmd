from pathlib import PurePath

import appdirs

DEFAULT_CONFIG_FILE = str(PurePath(appdirs.user_config_dir()) / "jrnlmdrc")
