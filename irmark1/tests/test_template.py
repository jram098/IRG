# -*- coding: utf-8 -*-
import tempfile
from tempfile import gettempdir
import unittest
from irmark1.parts.datastore import TubWriter, Tub
from irmark1.parts.datastore import TubHandler
from irmark1.templates import complete
import irmark1 as m1
import os

import pytest

#fixtures
from .setup import tub, tub_path, on_pi, default_template, d2_path, custom_template

def test_config():
    path = default_template(d2_path(gettempdir()))
    cfg = m1.load_config(os.path.join(path, 'config.py'))
    assert(cfg != None)

def test_drive():
    path = default_template(d2_path(gettempdir()))
    myconfig = open(os.path.join(path, 'myconfig.py'), "wt")
    myconfig.write("CAMERA_TYPE = 'MOCK'\n")
    myconfig.write("DRIVE_TRAIN_TYPE = 'None'")
    myconfig.close()
    cfg = m1.load_config(os.path.join(path, 'config.py'))
    cfg.MAX_LOOPS = 10
    complete.drive(cfg=cfg)


def test_custom_templates():
    template_names = ["complete", "basic_web", "square"]
    for template in template_names:
        path = custom_template(d2_path(gettempdir()), template=template)
        cfg = m1.load_config(os.path.join(path, 'config.py'))
        assert(cfg != None)
        mcfg = m1.load_config(os.path.join(path, 'myconfig.py'))
        assert(mcfg != None)
