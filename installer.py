# -*- coding: utf-8 -*-

import sys
import subprocess
import re
import os
from time import sleep

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
        self._api_source = "api.go"

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
        if ruby_version:
            print(success_msg) if verification else print(fail_msg)
        return verification

    def _verify_go(self, go_version):
        success_msg = "[OK]\tfound Go {}".format(go_version)
        fail_msg = "[Error]\tfound Go {} ({} required).".format(
            go_version, self._dependencies["go"]["version"])
        self._dependencies["go"]["present"] = go_version
        verification = self._dependencies["go"]["version"] == go_version
        if go_version:
            print(success_msg) if verification else print(fail_msg)
        return verification

    def _verify_deps(self):
        print("Checking for dependencies ...")
        sleep(0.5)
        p = self._verify_python(sys.version_info.major)
        sleep(0.5)
        r = self._verify_ruby(get_ruby_version())
        sleep(0.5)
        g = self._verify_go(get_go_version())
        return p and r and g

    def _build_api(self, path_to_api_src):
        os.chdir(os.path.dirname(path_to_api_src))
        print("\nBuilding {} ...\n".format(self._api_source))
        build_cmd = ["go", "build", path_to_api_src]
        go_build = subprocess.run(build_cmd)
        return go_build.returncode

    def install(self):
        """
        Creates environment for the polyglot-task
        """
        this_file_dir = os.path.dirname(os.path.realpath(__file__))
        path_to_api_src = os.path.join(this_file_dir, self._api_source)
        if self._verify_deps():
            sleep(0.5)
            go_build_return_code = self._build_api(path_to_api_src)
        else:
            if self._dependencies["go"]["present"]:
                build_anyways = query_yes_no(
                    "Do you want to compile sources using Go {}?".format(self._dependencies["go"]["present"]))
                sleep(0.5)
                go_build_return_code = self._build_api(path_to_api_src) if build_anyways else False
            else:
                sleep(2)
                sys.exit("Could not call `go` from the console. Aborting.")
        print("Done.") if go_build_return_code == 0 else sys.exit("\nBuilding {} failed. Aborting.".format(self._api_source))



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


def get_go_version():
    """
    :return: Go version
    """
    cmd = "go"
    go_version = None
    try:
        rg = subprocess.run([cmd, "version"], stdout=subprocess.PIPE)
        stdout = bytes.decode(rg.stdout).strip()
        if re.match(r'''
                    ^           # start of string
                    go          # "go" string
                    \s          # one whitespace
                    version     # "version" string
                    \s          # one whitespace
                    ''', stdout, re.VERBOSE):
            go_version = re.sub(r'''
                                ^           # start of string
                                go          # "go" string
                                \s          # one whitespace
                                version     # "version" string
                                \s          # one whitespace
                                go          # "go" string
                                (           # start of grouping
                                [0-9]       # a digit
                                \.          # "." string
                                [0-9]+      # one or more digits
                                )           # end of grouping
                                .*          # any character (except line break) zero or more times
                                ''', "\\1", stdout, 0, re.VERBOSE)
    except FileNotFoundError:
        print("[Error]\t`{}` command not found. Make sure that go is installed and added to the PATH".format(cmd))
    return go_version


def query_yes_no(question):
    """
    :param question: Question to be answered
    :return: answer
    """
    valid = {"yes": True, "y": True,
             "no": False, "n": False}

    while True:
        sys.stdout.write("{}: [yes/no] ".format(question))
        choice = input().lower()
        if choice == '':
            return True
        elif choice in valid:
            return valid[choice]
        else:
            print("Try again")
