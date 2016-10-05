# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#
# 导入ansible所需模块
# DataLoader, 负责数据解析
# VariableManager, 负责存储各类变量
# Inventory, 负责初始化hosts
# Play, 负责初始化playbook
# TaskQueueManager, 负责初始化执行对象, 其run()函数负责执行play
#
# '''
# TaskQueueManager(**, inventory=Inventory(**, host_list=hostsfile), options=options)
# .run(Play().load(dict, variable_manager=VariableManager(), loader=DataLoader())
# '''
#
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

#
# 用于执行结果的调用，使用示例如下
# TaskQueueManager(**, stdout_callback=results_callback, **).run(***)
#
class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for
        retrieval later
        """
        host = result._host
        print json.dumps({host.name: result._result}, indent=4)


class AnsibleRunner(object):
    def __init__(self, vault_pass, connection='local', module_path='',
                forks=100, become=None, become_method=None, become_user=None,
                check=False):
        """
        初始化ansible信息
        """
        Options = namedtuple('Options',
                    ['connection',
                    'module_path',
                    'forks',
                    'become',
                    'become_method',
                    'become_user',
                    'check']
                )
        self.options = Options(connection=connection,
                    module_path=module_path,
                    forks=forks,
                    become=become,
                    become_method=become_method,
                    become_user=become_user,
                    check=check
                )
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = dict(vault_pass=vault_pass)


    def init_inventory(self, host_list='localhost'):
        # 创建inventory
        # 把inventory传递给variable_manager管理
        self.inventory = Inventory(loader=loader,
                    variable_manager=variable_manager,
                    host_list=host_list
                )
        self.variable_manager.set_inventory(inventory)

#
# 结果回调类实例化
#
# Instantiate our ResultCallback for handling results as they come in
#
results_callback = ResultCallback()



#
# 创建playbook
#
# create play with tasks
#
play_source =  dict(
        name = "Ansible Play",
        hosts = 'localhost',
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='shell', args='ls'), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
         ]
    )
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

#
# 通过TaskQueueManager().run()执行ansible，具体语法如下
# "TaskQueueManager(指定inventory，loader，variable_manager, options，passwords, stdout_callback).run(play)"
#
# actually run it
#
tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
          )
    result = tqm.run(play)
finally:
    if tqm is not None:

        tqm.cleanup()
