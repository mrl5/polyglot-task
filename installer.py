# -*- coding: utf-8 -*-

import sys

__author__ = "mrl5"


class Installer:
    """
    Class for installer
    """

    def __init__(self):
        self._dependencies = {
            "python": {"version": 3, "present": sys.version_info.major},
            "ruby": {"version": ["2.3", "2.4"], "present": None},
            "go": {"version": "1.10", "present": None}
        }

    def _verify_python(self, sys_version_major):
        success_msg = "[OK]\tfound Python {}.{}.{}".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
        fail_msg = "[Error]\tfound Python {}.{}.{}. Run this script using 'python3' command.".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
        verification = self._dependencies["python"]["version"] == sys_version_major
        print(success_msg) if verification else print(fail_msg)
        return verification

    def _verify_ruby(self, ruby_version):
        success_msg = "[OK]\tfound Ruby {}".format(ruby_version)
        fail_msg = "[Error]\tfound Ruby {}. Make sure that `ruby` command leads to the {} version".format(
            ruby_version, " or ".join(self._dependencies["ruby"]["version"]))
        self._dependencies["ruby"]["present"] = ruby_version
        verification = ruby_version in self._dependencies["ruby"]["version"]
        print(success_msg) if verification else print(fail_msg)
        return verification

    def _verify_go(self, go_version):
        pass