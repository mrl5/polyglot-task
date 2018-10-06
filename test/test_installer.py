# -*- coding: utf-8 -*-

import pytest
import shutil
import os
from installer import Installer

__author__ = "mrl5"

"""
Scenario:
    - '_verify_python()' should return true if version 3
    - '_verify_python()' should return false if other version
    - '_verify_ruby()' should return true if version 2.4
    - '_verify_ruby()' should return true if version 2.3
    - '_verify_ruby()' should return false if other version
    - '_verify_go()' should return true if version 1.10
    - '_verify_go()' should return false if other version 
    - '_compile_api()' should compile 'api.go'
    - binary file created by 'compile_api()' should be in project's directory
    - 'set_permissions()' should set executable permissions to the files
    - 'set_permissions()' should throw 'OSError' when permission can't be set
"""


@pytest.fixture(scope="function")
def installer_instance():
    installer = Installer()
    return installer


def test_verify_python_success(installer_instance):
    python_version_major = installer_instance._dependencies["python"]["version"]
    assert installer_instance._verify_python(python_version_major) is True


def test_verify_python_fail(installer_instance):
    python_version_major = 2
    assert installer_instance._verify_python(python_version_major) is False


def test_verify_ruby_success(installer_instance):
    ruby_version = installer_instance._dependencies["ruby"]["version"][0]
    assert installer_instance._verify_ruby(ruby_version) is True


def test_verify_ruby_fail(installer_instance):
    ruby_version = "2.5"
    assert installer_instance._verify_ruby(ruby_version) is False


def test_verify_go_success(installer_instance):
    go_version = installer_instance._dependencies["go"]["version"]
    assert installer_instance._verify_go(go_version) is True


def test_verify_go_fail(installer_instance):
    go_version = "1.9"
    assert installer_instance._verify_go(go_version) is False


def test_if_versions_are_stored(installer_instance):
    python_version_major = 2
    ruby_version = "2.5"
    go_version = "1.9"
    installer_instance._verify_python(python_version_major)
    installer_instance._verify_ruby(ruby_version)
    installer_instance._verify_go(go_version)
    test_dict = {
        "python": python_version_major,
        "ruby": ruby_version,
        "go": go_version
    }
    expected_dict_slice = {}
    for k, v in installer_instance._dependencies.items():
        expected_dict_slice.update({k: v["present"]})
    assert test_dict == expected_dict_slice


def test_build_api(tmpdir, installer_instance):
    test_dir = tmpdir.mkdir("test_dir")
    main_dir = os.path.dirname(os.getcwd())
    binary_name = os.path.splitext(installer_instance._api_source)[0]
    api_src = os.path.join(main_dir, installer_instance._api_source)
    api_dest = os.path.join(str(test_dir), installer_instance._api_source)
    shutil.copyfile(api_src, api_dest)
    os.chdir(str(test_dir))
    installer_instance._build_api(api_dest)
    assert os.path.isfile(os.path.join(str(test_dir), binary_name))