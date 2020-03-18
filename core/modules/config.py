# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, doudoudzj
# Copyright (c) 2012, VPSMate development team
# All rights reserved.
#
# InPanel is distributed under the terms of the New BSD License.
# The full license can be found in 'LICENSE'.

'''Module for Configurations Management.'''

import os

from lib.filelock import FileLock

try:
    from ConfigParser import ConfigParser  # python 2.x
except:
    from configparser import ConfigParser  # python 3.x


class Config(object):

    def __init__(self, inifile=None, configs=None):
        self.inifile = 'data/config.ini' if inifile is None else inifile
        self.cfg = ConfigParser()

        with FileLock(self.inifile):
            if os.path.exists(self.inifile):
                self.cfg.read(self.inifile)

            # initialize configurations
            if configs is None:
                default_configs = {
                    'server': {
                        'ip': '*',
                        'port': '8888',
                        'forcehttps': 'off', # force use https
                        'lastcheckupdate': 0,
                        'updateinfo': ''
                    },
                    'auth': {
                        'username': 'admin',
                        'password': '',         # empty password never validated
                        'passwordcheck': 'on',
                        'accesskey': '',        # empty access key never validated
                        'accesskeyenable': 'off',
                    },
                    'runtime': {
                        'mode': '',             # format: demo | dev | prod
                        'loginlock': 'off',
                        'loginfails': 0,
                        'loginlockexpire': 0,
                    },
                    'file': {
                        'lastdir': '/root',
                        'lastfile': '',
                    },
                    'time': {
                        'timezone': '' # format: timezone = Asia/Shanghai
                    },
                    'ecs': {
                        'accounts': ''
                    },
                    'inpanel': {
                        'Instance Name': 'Access key'
                    }
                }
            else:
                default_configs = configs

            needupdate = False
            for sec, secdata in default_configs.items():
                if not self.cfg.has_section(sec):
                    self.cfg.add_section(sec)
                    needupdate = True
                for opt, val in secdata.items():
                    if not self.cfg.has_option(sec, opt):
                        self.cfg.set(sec, opt, val)
                        needupdate = True

            # update ini file
            if needupdate:
                self.update(False)

    def update(self, lock=True):
        if lock:
            flock = FileLock(self.inifile)
            flock.acquire()

        try:
            inifp = open(self.inifile, 'w')
            self.cfg.write(inifp)
            inifp.close()
            if lock:
                flock.release()
            return True
        except:
            if lock:
                flock.release()
            return False

    def has_option(self, section, option):
        return self.cfg.has_option(section, option)

    def get(self, section, option):
        return self.cfg.get(section, option)

    def getboolean(self, section, option):
        return self.cfg.getboolean(section, option)

    def getint(self, section, option):
        return self.cfg.getint(section, option)

    def has_section(self, section):
        return self.cfg.has_section(section)

    def add_section(self, section):
        return self.cfg.add_section(section)

    def remove_option(self, section, option):
        return self.cfg.remove_option(section, option)

    def set(self, section, option, value):
        try:
            self.cfg.set(section, option, value)
        except:
            return False
        return self.update()
