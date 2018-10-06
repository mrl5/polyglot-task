# -*- coding: utf-8 -*-

import sys
import subprocess
import re

__author__ = "mrl5"


class Installer:
    """
    Class for installer
    """

    def __init__(self):
        self._dependencies = {
            "python": {"version": 3, "present": None},
            "ruby": {"version": ["2.3", "2.4"], "present": None},
            "go": {"version": "1.10", "present": None}
        }

    def _verify_python(self, sys_version_major):
        success_msg = "[OK]\tfound Python {}.{}.{}".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
        fail_msg = "[Error]\tfound Python {}.{}.{}. Run this script using 'python3' command.".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
        self._dependencies["python"]["present"] = sys_version_major
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
        success_msg = "[OK]\tfound Go {}".format(go_version)
        fail_msg = "[Error]\tfound Go {} ({} required).".format(
            go_version, self._dependencies["go"]["version"])
        self._dependencies["go"]["present"] = go_version
        verification = self._dependencies["go"]["version"] == go_version
        print(success_msg) if verification else print(fail_msg)
        return verification


def get_ruby_version():
    """
    :return: Ruby version
    """
    cmd = "ruby"
    ruby_version = None
    try:
        rv = subprocess.run([cmd, "--version"], stdout=subprocess.PIPE)
        stdout = bytes.decode(rv.stdout).strip()
        if re.match(r'''
                    ^       # start of string
                    \b      # start of whole word
                    ruby    # "ruby" string
                    \b      # end of whole word
                    ''', stdout, re.VERBOSE):
            ruby_version = re.sub(r'''
                                ^       # start of string
                                \b      # start of whole word
                                ruby    # "ruby" string
                                \b      # end of whole word
                                \s      # one whitespace
                                (       # start of grouping
                                [0-9]   # a digit
                                \.      # "." string
                                [0-9]   # a digit
                                )       # end of grouping
                                .*      # any character (except line break) zero or more times
                                ''', "\\1", stdout, 0, re.VERBOSE)
    except FileNotFoundError:
        print("[Error]\t`{}` command not found. Make sure that ruby is installed and added to the PATH".format(cmd))
    return ruby_version
