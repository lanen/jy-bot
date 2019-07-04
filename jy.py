#!/usr/local/bin/python3
import os
import slack
import json
import logging
import yaml

class Command:

    def __init__(self, web_client, rtm_client, data): 
        self.web = web_client
        self.rtm = rtm_client
        self.data = data
        self.logger = logging.getLogger('command')
    #end def __init__

    def execute(self):
        pass
    # end def execute 
#end class Command


class ReplyHello(Command):


    def __init__(self, web_client, rtm_client, data): 
        Command.__init__(self, web_client, rtm_client, data)
    #end def __init__

    def execute(self):
        channel_id = self.data['channel']
        thread_ts = self.data['ts']
        user = self.data['user']
        self.logger.info("send post message to %r", user)
        self.web.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            thread_ts=thread_ts
        )
    # end def execute 
#end class ReplyHello



class ReplyStart(Command):

    def __init__(self, web_client, rtm_client, data): 
        Command.__init__(self, web_client, rtm_client, data)
    #end def __init__

    def execute(self):
        channel_id = self.data['channel']
        thread_ts = self.data['ts']
        user = self.data['user']
        self.logger.info("send post message to %r", user)
        self.web.chat_postMessage(
            channel=channel_id,
            text=f"Start",
            thread_ts=thread_ts
        )
    # end def execute 
#end class ReplyStart

@slack.RTMClient.run_on(event='message')
def received_message(**payload):
    data = payload['data']
    logging.info("receive message %s", json.dumps(data))

    mapping = {
        'hello' : ReplyHello,
        'start' : ReplyStart
    }

    def h(cmdKey, message):
        cmdClass = mapping[cmdKey]
        if cmdClass:
            cmd = cmdClass(web_client=payload['web_client'], rtm_client=payload['rtm_client'],data=data)
            cmd.execute()	
            
    for cmdKey in mapping.keys():
        if 'client_msg_id' in data:
            if cmdKey in data['text']:
                h(cmdKey,data)
        
    # end if
# end def received_message

def main():
    logging.basicConfig(filename='/var/run/log/jy-bot.log', level=logging.DEBUG)
    token=''
    filepath='/usr/local/etc/jy-bot/config.yml' 
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
            token = cfg['token']
    
    if '' == token :
        token = os.environ['SLACK_API_TOKEN']

    rtm_client = slack.RTMClient(token=token)
    rtm_client.start()

if __name__ == '__main__':
    main()

