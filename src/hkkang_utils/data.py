import sys

# Import dataclasses according to Python version
sys_version = sys.version_info
if sys_version[0] == 3 and sys_version[1] >= 7:
    import dataclasses
else:
    try:
        import dataclasses
    except:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "dataclasses"])
    finally:
        import dataclasses

from typing import *

import dacite


def asdict(obj: any, skip_none: bool = False) -> Dict:
    def custom_dict_factory(items):
        dict = {}
        for key, value in items:
            if dataclasses.is_dataclass(value):
                dict[key] = asdict(value, skip_none=skip_none)
            else:
                if skip_none and value is None:
                    continue
                dict[key] = value
        return dict

    return dataclasses.asdict(obj, dict_factory=custom_dict_factory)


def from_dict(data_class: dataclasses.dataclass, data: Dict) -> dataclasses.dataclass:
    return dacite.from_dict(data_class, data)
