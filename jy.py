#!/usr/local/bin/python3
import os
import slack
import json
import logging
import yaml


"""
2019-7-5 增加Session 支持
2019-7-5 增加Service 支持
2019-7-4 增加yaml 配置文件支持
2019-7-4 增加Command 模式支持

"""

# 全局变量，记录与slack服务器的会话
global session
global services


class Session:
    """
        与slack的会话对象
    """
    web_client = None

    rtm_client = None

    logger = None

    def __init__(self):
        self.logger = logging.getLogger('session')
    # end def __init__
    
    def open(self,token):
        self.rtm_client = slack.RTMClient(token=token)
        self.rtm_client.start()
    # end def open

    def talk(self, text, channel_id, thread_ts, user):
        self.logger.info("send post message to %r", user)
        self.web_client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts=thread_ts
        )
    #end def talk


class Service:
    """
    """
    def __init__(self, content):
        self.logger = logging.getLogger('service')
        self.names = content
    #end def __init__

    def support(self, name):
        if name in self.names:
            return True
        return False
    #end def support

    def start(self, name):
        self.logger.info('service start %r', name)
        self._os_command('start', name)
    #end def start

    def stop(self, name):
        self.logger.info('service stop %r', name)
        self._os_command('stop', name)

    #end def start

    def restart(self, name):
        self.logger.info('service restart %r', name)
        self._os_command('restart', name)

    #end

    def status(self, name):
        self.logger.info('service status %r', name)
        self._os_command('status', name)
    #end def status

    def _os_command(self, cmd, name):
        os.system("/usr/bin/systemctl %r %r" % (cmd, name)) 
        pass
    #end def _os_command

# end class Serivice


class Command:
    """
    提供一个基类，规范命令接口
    """
    def __init__(self, command_text): 
        self.command_text = command_text
        self.logger = logging.getLogger('command')
    #end def __init__

    def execute(self,callback):
        pass
    # end def execute 
#end class Command


class ReplyHelp(Command):
    """
       响应hello的命令
    """

    def __init__(self, command_text): 
        Command.__init__(self, command_text)
    #end def __init__

    def execute(self,callback):
        global services
        help_info = ','.join(services.names)
        callback(help_info) 
    # end def execute 
#end class ReplyHello


class ReplyService(Command):
    """
        响应启动的命令
    """
    def __init__(self,command_text): 
        Command.__init__(self,command_text)
    #end def __init__

    def execute(self, callback):
        global services
        parts = self.command_text.split(' ')
        method = {
            'start' : services.start,
            'stop' : services.stop,
            'status' : services.status,
            'restart' : services.restart
        }
        if parts[0] in method:
            if not services.support(parts[1]):
                callback('service not support ' + parts[1])
                return
            instance = method[parts[0]]
            instance(parts[1])
            callback('finish ' + self.command_text)
        else:
            callback('no method support ' + self.command_text)
            
       
    # end def execute 
#end class ReplyService


class CommandMapping:
    """
        命令映射
    """

    def __init__(self):
        self.mapping = {
            'help' : ReplyHelp,
            'start' : ReplyService,
            'stop' : ReplyService,
            'status' : ReplyService,
            'restart' : ReplyService
        }
    # end def __init__


    def handleCommand(self, cmdKey, message, callback):
        cmdClass = self.mapping[cmdKey]
        if cmdClass:
            cmd = cmdClass(command_text=message)
            cmd.execute(callback)	
    # end def handleCommand

    def receive_message(self, data, callback):
        for cmdKey in self.mapping.keys():
            if 'client_msg_id' in data:
                text = data['text']
                offset=text.find('>')
                text = text[offset+1:].strip()
                if text.startswith(cmdKey):
                    self.handleCommand(cmdKey,text, callback)
    #end def receive
# end class CommandMapping


@slack.RTMClient.run_on(event='message')
def received_message(**payload):
    """
       RTM 实时消息收发器
    """
    global session
    data = payload['data']
    session.web_client = payload['web_client']
    logging.info("receive message %s", json.dumps(data))

    def callback(reply):
        """
            回调函数，放这里，是因为data 上下文
        """
        if 'channel' not in data:
            channel_id = data['message']['channel']
        else:
            channel_id = data['channel']
        thread_ts = data['ts']
        if 'user' not in data:
            user = data['message']['user']
        else:
            user = data['user']

        session.talk(reply, channel_id, thread_ts, user)
    #end def callback

    mapping = CommandMapping()
    mapping.receive_message(data, callback)
        
# end def received_message


def main():
    global session
    global services
    logging.basicConfig(filename='/var/run/log/jy-bot.log', level=logging.DEBUG)
    token=''
    filepath='/usr/local/etc/jy-bot/config.yml' 
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
            token = cfg['token']
            services = Service(cfg['services'])
    
    if '' == token :
        token = os.environ['SLACK_API_TOKEN']
    
    session = Session()
    session.open(token)


if __name__ == '__main__':
    main()

