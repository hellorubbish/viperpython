# -*- coding: utf-8 -*-
# @File  : SimplePostPythonModule.py
# @Date  : 2019/1/12
# @Desc  :

from Lib.ModuleAPI import *


class PostModule(PostMSFPythonModule):
    NAME = "执行自定义Python脚本"
    DESC = "主机内存中(Windows)或者系统Python解释器(Linux)执行自定义的Python脚本.\n" \
           "Python脚本只支持Python2.7及其自带的库.\n" \
           "执行的脚本可以通过文件列表 上传到服务器."
    MODULETYPE = TAG2CH.Defense_Evasion
    PLATFORM = ["Windows", "Linux"]  # 平台
    PERMISSIONS = ["User", "Administrator", "SYSTEM", "Root"]  # 所需权限
    ATTCK = ["T1055"]  # ATTCK向量
    README = ["https://www.yuque.com/funnywolfdoc/viperdoc/urco5z"]
    REFERENCES = ["https://attack.mitre.org/techniques/T1050/"]
    AUTHOR = "Viper"

    OPTIONS = register_options([
        OptionFileEnum(ext=['py', 'pyc']),
        OptionIntger(name='timeout', name_tag="脚本超时时间(秒)", desc="脚本执行的超时时间(5-3600)", required=True, default=60),
    ])

    def __init__(self, sessionid, hid, custom_param):
        super().__init__(sessionid, hid, custom_param)

    def check(self):
        """执行前的检查函数"""
        script = self.get_option_filename()
        if script is None:
            return False, "请选择执行的脚本,脚本后缀必须为py或pyc"
        self.set_script(script)

        timeout = self.param("timeout")
        # 检查timeout
        if timeout < 5 or timeout > 3600:
            return False, "输入的模块超时时间有误(最小值60,最大值3600),请重新输入"
        self.set_script_timeout(timeout)

        session = Session(self._sessionid)
        if session.is_alive:
            return True, None
        else:
            return False, "Session不可用"

    def callback(self, status, message, data):
        if status:
            self.log_good("脚本执行完成")
            self.log_raw(data)
        else:
            self.log_error("模块执行失败")
            self.log_error(message)
