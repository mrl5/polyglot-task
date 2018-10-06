#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

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
            "go": {"version": "1.10", "present": None, "status": False}
        }
        self._api_source = "api.go"
        self._work_files = ["worker.py", "endpoint.rb", os.path.splitext(self._api_source)[0]]

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
        self._dependencies["go"]["status"] = verification
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
        print("\nBuilding {} ...".format(self._api_source))
        build_cmd = ["go", "build", path_to_api_src]
        go_build = subprocess.run(build_cmd)
        return go_build.returncode

    def _set_executable_permission(self, path_to_file):
        """
        Sets execute permission for the owner and for a group
        """
        octal_permission = 0o750 # rwxr-x---
        try:
            os.chmod(path_to_file, octal_permission)
            print("[OK]\t{}".format(path_to_file))
            ret_code = 0
        except OSError as oe:
            print("[Error]\t{}: {}".format(oe.filename, oe.strerror))
            ret_code = 1
        return ret_code

    def _quit_msg(self, deps_err, perms_err):
        """
        Prints quit message
        :param deps_err: dependencies error (True/False)
        :param perms_err: permissions error (True/False)
        """
        if not(deps_err | perms_err):
            sleep(0.5)
            print("\nSuccess. Application is ready to use.")
        else:
            sleep(0.5)
            sys.stderr.write("\nNot all dependencies were met. Application might not work properly") if deps_err else False
            sys.stderr.write("\nNot all files have execute permissions.") if perms_err else False
            sys.exit(1)

    def install(self):
        """
        Creates environment for the polyglot-task
        """
        this_file_dir = os.path.dirname(os.path.realpath(__file__))
        path_to_api_src = os.path.join(this_file_dir, self._api_source)
        deps_err = not self._verify_deps()
        if self._dependencies["go"]["status"]:
            sleep(0.5)
            go_build_return_code = self._build_api(path_to_api_src)
        else:
            if self._dependencies["go"]["present"]:
                build_anyways = query_yes_no(
                    "Do you want to compile sources using Go {}?".format(self._dependencies["go"]["present"]))
                go_build_return_code = self._build_api(path_to_api_src) if build_anyways else sys.exit("Aborting.")
            else:
                sleep(2)
                sys.exit("Could not call `go` from the console. Aborting.")
        print("Done.") if go_build_return_code == 0 else sys.exit("\nBuilding {} failed. Aborting.".format(self._api_source))

        print("\nSetting execute permissions ...")
        os.chdir(this_file_dir)
        perms_err = 0
        for f in self._work_files:
            sleep(0.5)
            perms_err = perms_err | self._set_executable_permission(f)
        self._quit_msg(deps_err, bool(perms_err))


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
    :param question: question to be answered
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
            print("Try again.")


def main(args):
    allowed_no_of_args = 0
    sys.exit("Installer is written for Python 3. Aborting.") if sys.version_info.major < 3 else False
    sys.exit("Script doesn't accept any arguments.") if len(args) != allowed_no_of_args else False
    installer = Installer()
    installer.install()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
