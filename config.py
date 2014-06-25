#!/usr/bin/env python

"""Read Yaml based configuration files.

This module provides a Config class and a load function as an alternate API to
create and itinitialize it from a Yaml config file. The confile file format
supports importing environment variables, defining local variables, and also
optionally exporting variables to the environment. Simple string based variable
substitution is also supported.

This module is meant to be imported into the target application, but can also
be run as a script to read and print the config file.

Classes:

    Config

Functions:

    load_yaml(file_name) -> object

Yaml config file example:
========================================
import:
- HOME
- PATH

local:
- APP_VERSION : "0.7"
- APP_PATH    : "{HOME}/myapp-{APP_VERSION}/bin"

export:
- PATH : "{PATH}:{APP_PATH}"
========================================

"""

__author__ = "Rohit Rathi"

import yaml
import os
from collections import OrderedDict

class Config(object):
    def __init__(self):
        # Raw variables
        self.imports = OrderedDict()
        self.locals = OrderedDict()
        self.exports = OrderedDict()

        # Evaluated variables
        self.ctx = OrderedDict()
        self.env = OrderedDict()

        self._file_name = None
        self._file_format = None

    def load_yaml(self, file_name):
        self._file_name = file_name
        self._file_format = "yaml"

        with open(file_name, "r") as fp:
            config = yaml.load(fp)

        for k in config['import']:
            if k is None: continue
            #print k
            v = os.environ[k]
            self.imports[k] = v
            self.ctx[k] = v

        for k_v in config['local']:
            if k_v is None: continue
            for k, v in k_v.items():
                #print k, v
                self.locals[k] = v
                self.ctx[k] = v.format(**self.ctx)

        for k_v in config['export']:
            if k_v is None: continue
            for k, v in k_v.items():
                #print k, v
                self.exports[k] = v
                self.ctx[k] = self.env[k] = v.format(**self.ctx)

    def export_env(self):
        for var, val in self.env.items():
            os.environ[var] = val

def load_yaml(file_name):
    config = Config()
    config.load_yaml(file_name)
    return config

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    import argparse

    argp = argparse.ArgumentParser(
        description="Read Yaml based configuration file.")
    argp.add_argument("file", help="config file")

    argns = argp.parse_args()

    print "Loading config file %s" % argns.file
    config = load_yaml(argns.file)


    print "imports:"
    for var in config.imports:
        print "  %s = %s" % (var, config.ctx[var])

    print "locals:"
    for var in config.locals:
        print "  %s = %s" % (var, config.ctx[var])

    print "exports:"
    for var in config.exports:
        print "  %s = %s" % (var, config.ctx[var])
