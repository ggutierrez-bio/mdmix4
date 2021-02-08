import os


def test_import():
    import pymdmix_core
    assert pymdmix_core is not None
    assert os.getenv("MDMIX_HOME") is not None
    import pymdmix_core.settings
