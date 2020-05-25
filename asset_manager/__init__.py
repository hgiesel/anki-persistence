from aqt import mw
from anki.hooks import addHook
from aqt.utils import showInfo

from .utils import find_addon_by_name

script_name = 'Anki Persistence'
file_name = 'script'
version = 'v0.5.3'
description = 'Allows for persisting data between front and back of Anki card.'

am = find_addon_by_name('Asset Manager')

if am:
    ami = __import__(am).src.lib.interface
    amr = __import__(am).src.lib.registrar

def setup_script():
    if not am:
        showInfo('Requires Asset Manager to be installed.')

    from pathlib import Path
    from os.path import dirname, realpath

    filepath = Path(f'{dirname(realpath(__file__))}', 'web', f'{file_name}.js')

    with open(filepath, 'r') as file:
        script = file.read().strip()

        amr.make_and_register_interface(
            tag = f"{script_name}_tag",

            getter = lambda id, storage: ami.make_script(
                script_name,
                storage.enabled if storage.enabled is not None else True,
                'js',
                version,
                description,
                'body',
                storage.conditions if storage.conditions is not None else [],
                script,
            ),

            setter = lambda id, script: True,
            store = ['enabled', 'conditions', 'position'],
            readonly = ['name', 'type', 'version', 'description', 'code'],
            reset = False,
            deletable = False,
        )

def install_script():
    # create the meta script which points to your interface
    if not am:
        return

    my_meta_script = ami.make_meta_script(
        f"{script_name}_tag",
        f"{script_name}_id",
    )

    # insert the script for every model
    for model_id in mw.col.models.ids():
        amr.register_meta_script(
            model_id,
            my_meta_script,
        )

def setup_hook():
    setup_script()
    addHook('profileLoaded', install_script)

setup_hook()
