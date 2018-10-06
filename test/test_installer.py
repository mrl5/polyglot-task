# -*- coding: utf-8 -*-

import pytest
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
    - 'verify_permission()' should return true if file is executable
    - 'verify_permission()' should return false if file is not executable 
    - 'set_executable_permission()' should set executable permission to the file
    - 'set_executable_permission()' should throw 'OSError' when permission can't be set
    - 'install()' should create a project with right structure
"""


@pytest.fixture(scope="function")
def installer_instance():
    installer = Installer()
    return installer


def test_verify_python_success(installer_instance):
    python_version_major = installer_instance._dependencies["python"]["version"]
    assert installer_instance._verify_python(python_version_major) is True
