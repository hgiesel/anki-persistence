from pathlib import Path
from os.path import dirname, realpath

from aqt import mw
from anki.hooks import addHook
from aqt.utils import showInfo

from .utils import find_addon_by_name

script_name = 'Anki Persistence'

script_tag = 'AnkiPersistenceTag'
script_id = 'AnkiPersistenceId'

version = 'v0.5.3'

description = '''Allows for persisting data between front and back of an Anki card.
For more on this script, see https://github.com/SimonLammer/anki-persistence.
For more on this add-on, see https://github.com/hgiesel/anki-persistence.'''

am = find_addon_by_name('Asset Manager')

if am:
    ami = __import__(am).src.lib.interface
    amr = __import__(am).src.lib.registrar

def get_script():
    filepath = Path(f'{dirname(realpath(__file__))}', 'web', 'script.js')

    with open(filepath, 'r') as file:
        return file.read().strip()

def setup_script():
    if not am:
        showInfo('Anki Persistence requires Asset Manager to be installed.')
        return

    script = get_script()

    amr.make_and_register_interface(
        tag = script_tag,
        label = lambda _id, _tag: script_name,

        getter = lambda id, storage: ami.make_script(
            script_name,
            storage.enabled if storage.enabled is not None else True,
            'js',
            version,
            description,
            storage.position if storage.position is not None else 'into_template',
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
        script_tag,
        script_id,
    )

    # insert the script for every model
    for model_id in mw.col.models.ids():
        amr.register_meta_script(
            model_id,
            my_meta_script,
        )
