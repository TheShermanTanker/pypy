import sys
import py
from rpython.config.translationoption import get_combined_translation_config
from rpython.config.translationoption import set_opt_level
from rpython.config.translationoption import get_translation_config
from rpython.config import translationoption
from rpython.config.config import ConflictConfigError, ConfigError
from rpython.translator.platform import platform as compiler


def test_get_translation_config():
    from rpython.translator.interactive import Translation
    from rpython.config import config
    def f(x):
        config = get_translation_config()
        if config is not None:
            return config.translating
        return False

    t = Translation(f, [int])
    config = t.config

    # do the patching
    t.annotate()
    retvar = t.context.graphs[0].returnblock.inputargs[0]
    assert t.context.annotator.binding(retvar).const

    assert get_translation_config() is config # check during import time
