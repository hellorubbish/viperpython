# -*- coding: utf-8 -*-
# @File  : SimpleRewMsfModule.py
# @Date  : 2019/1/11
# @Desc  :

import re
from pathlib import PurePosixPath

from Lib.ModuleAPI import *


class PostModule(PostMSFRawModule):
    NAME = "下载文件"
    DESC = "模块用于下载Session所在主机文件到服务器.\n"
    REQUIRE_SESSION = True
    MODULETYPE = TAG2CH.internal

    def __init__(self, sessionid, hid, custom_param):
        super().__init__(sessionid, hid, custom_param)
        self.type = "post"
        self.mname = "multi/manage/file_system_operation_api"

    # opts = {'OPERATION': 'upload', 'SESSION': sessionid, 'SESSION_DIR': formatdir, 'MSF_FILE': filename}

    def deal_path(self, path=None):
        """处理成linux路径"""
        tmppath = path.replace('\\\\', '/').replace('\\', '/')

        if re.match("^/[a-zA-Z]:/", tmppath) is not None:
            tmppath = tmppath[1:]

        # 只支持最后加/..和/../
        if tmppath.startswith('/'):  # linux路径
            if tmppath.endswith('/..') or tmppath.endswith('/../'):
                parts = PurePosixPath(tmppath).parent.parent.parts
                if len(parts) == 1:
                    tmppath = '/'
                elif len(parts) == 0:
                    tmppath = '/'
                else:
                    tmppath = "/".join(parts)

        else:
            if tmppath.endswith('/..') or tmppath.endswith('/../'):
                parts = PurePosixPath(tmppath).parent.parent.parts
                if len(parts) == 1:
                    tmppath = parts[0] + '/'
                elif len(parts) == 0:
                    tmppath = '/'
                else:
                    tmppath = "/".join(parts)

        tmppath = tmppath.replace('//', '/')
        if tmppath == '' or tmppath is None:
            self.log_warning('输入错误字符')
            tmppath = '/'
        return tmppath

    def check(self):
        self.set_option("OPERATION", 'download')
        SESSION_FILE = self.deal_path(self.param("SESSION_FILE"))
        self.set_option("SESSION_FILE", SESSION_FILE)

        return True, None

    def callback(self, status, message, data):
        # 调用父类函数存储结果(必须调用)
        if status:
            self.log_good(f"{self.param('SESSION_FILE')} 下载完成.")
        else:
            self.log_error('下载失败')
            self.log_error(message)
