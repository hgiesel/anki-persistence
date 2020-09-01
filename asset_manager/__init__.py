from aqt.gui_hooks import profile_did_open

from .script import setup_script, install_script


def setup_hook():
    setup_script()
    profile_did_open.append(install_script)

setup_hook()
