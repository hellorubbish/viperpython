# -*- coding: utf-8 -*-
# @File  : postmoduleactuator.py
# @Date  : 2021/2/26
# @Desc  :
import importlib
import json
import time
import uuid

from Lib.Module.configs import BROKER
from Lib.api import data_return
from Lib.apsmodule import aps_module
from Lib.configs import PostModuleActuator_MSG
from Lib.log import logger
from Lib.msfmodule import MSFModule
from Lib.notice import Notice
from Lib.xcache import Xcache


class PostModuleActuator(object):
    """任务添加器"""

    def __init__(self):
        pass

    @staticmethod
    def create_post(loadpath=None, sessionid=None, hid=None, custom_param=None):
        module_config = Xcache.get_moduleconfig(loadpath)
        # 获取模块配置
        if module_config is None:
            context = data_return(305, PostModuleActuator_MSG.get(305), {})
            return context

        # 处理模块参数
        try:
            custom_param = json.loads(custom_param)
        except Exception as E:
            logger.warning(E)
            custom_param = {}

        # 获取模块实例
        class_intent = importlib.import_module(loadpath)
        post_module_intent = class_intent.PostModule(sessionid, hid, custom_param)

        # 格式化固定字段
        try:
            post_module_intent.AUTHOR = module_config.get("AUTHOR")
        except Exception as E:
            logger.warning(E)

        # 模块前序检查,调用check函数
        try:
            flag, msg = post_module_intent.check()
            if flag is not True:
                # 如果检查未通过,返回未通过原因(msg)
                context = data_return(405, msg, {})
                return context
        except Exception as E:
            logger.warning(E)
            context = data_return(301, PostModuleActuator_MSG.get(301), {})
            return context

        try:
            broker = post_module_intent.MODULE_BROKER
        except Exception as E:
            logger.warning(E)
            context = data_return(305, PostModuleActuator_MSG.get(305), {})
            return context

        if broker == BROKER.post_python_job:
            # 放入多模块队列
            if aps_module.putin_post_python_module_queue(post_module_intent):
                context = data_return(201, PostModuleActuator_MSG.get(201), {})
                return context
            else:
                context = data_return(306, PostModuleActuator_MSG.get(306), {})
                return context
        elif broker == BROKER.post_msf_job:
            # 放入后台运行队列
            if MSFModule.putin_post_msf_module_queue(post_module_intent):
                context = data_return(201, PostModuleActuator_MSG.get(201), {})
                return context
            else:
                context = data_return(306, PostModuleActuator_MSG.get(306), {})
                return context
        else:
            logger.warning("错误的broker")

    @staticmethod
    def create_bot(ipportlist=None, custom_param=None, loadpath=None):
        module_config = Xcache.get_moduleconfig(loadpath)
        # 获取模块配置
        if module_config is None:
            context = data_return(305, PostModuleActuator_MSG.get(305), {})
            return context

        # 处理模块参数
        try:
            custom_param = json.loads(custom_param)
        except Exception as E:
            logger.warning(E)
            custom_param = {}

        # 获取模块实例
        group_uuid = str(uuid.uuid1()).replace('-', "")
        class_intent = importlib.import_module(loadpath)
        for ipport in ipportlist:
            post_module_intent = class_intent.PostModule(ip=ipport.get("ip"), port=ipport.get("port"),
                                                         protocol=ipport.get("protocol"),
                                                         custom_param=custom_param)
            # 格式化固定字段
            try:
                post_module_intent.AUTHOR = module_config.get("AUTHOR")
            except Exception as E:
                logger.warning(E)

            # 模块前序检查,调用check函数
            try:
                flag, msg = post_module_intent.check()
                if flag is not True:
                    # 如果检查未通过,返回未通过原因(msg)
                    Notice.send_warning(f"模块:{post_module_intent.NAME} IP:{ipport.get('ip')} 检查未通过,原因:{msg}")
                    continue

            except Exception as E:
                logger.warning(E)
                Notice.send_warning(f"模块:{post_module_intent.NAME} IP:{ipport.get('ip')} 检查函数执行异常")
                continue

            tmp_self_uuid = str(uuid.uuid1())
            req = {
                'uuid': tmp_self_uuid,
                'group_uuid': group_uuid,
                'broker': post_module_intent.MODULE_BROKER,
                'module': post_module_intent,
                'time': int(time.time()),
            }
            Xcache.putin_bot_wait(req)

        context = data_return(201, PostModuleActuator_MSG.get(201), {})
        return context
