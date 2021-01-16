from pathlib import Path

try:
    from sys import _MEIPASS
    _base_path = Path(_MEIPASS)
except:
    from sys import modules
    try:
        _base_path = Path(modules['__main__'].__file__).parent
    except:
        from os import getcwd
        _base_path = Path(getcwd())

def get_resource_path():
    return _base_path
