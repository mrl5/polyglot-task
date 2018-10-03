# -*- coding: utf-8 -*-

import pytest

__author__ = "mrl5"

"""
Scenario:
    - 'verify_python()' should return true if version 3
    - 'verify_python()' should return false if other version
    - 'verify_ruby()' should return true if version 2.4
    - 'verify_ruby()' should return true if version 2.3
    - 'verify_ruby()' should return false if other version
    - 'verify_go()' should return true if version 1
    - 'verify_go()' should return false if other version
    - 'verify_dir_access()' should return true if project's dir is writable
    - 'verify_dir_access()' should return false if project's dir is not writable
    - 'compile_api()' should compile 'api.go'
    - binary file created by 'compile_api()' should be in project's directory
    - 'verify_permission()' should return true if file is executable
    - 'verify_permission()' should return false if file is not executable 
    - 'set_executable_permission()' should set executable permission to the file
    - 'set_executable_permission()' should throw 'OSError' when permission can't be set
    - 'install()' should create a project with right structure
"""
