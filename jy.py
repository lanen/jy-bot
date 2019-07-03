#!/usr/local/bin/python3

import os
import slack
import json


class Command:

    def __init__(self, web_client, rtm_client): 
        self.web = web_client
        self.rtm = rtm_client
    #end def __init__

    def reply_hello(self, data):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        self.web.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            thread_ts=thread_ts
        )
    # end def reply_hello
#end class Command


@slack.RTMClient.run_on(event='message')
def received_message(**payload):
    data = payload['data']
    print(json.dumps(data))
    if 'user' in data and 'UEC439HAB' != data['user']:
        return
    if 'subtype' in data:
        return

    cmd = Command(web_client=payload['web_client'], rtm_client=payload['rtm_client'])
    if 'Hello' in data['text']:
        cmd.reply_hello(data=data)	
    # end if
# end def received_message

def main():
    rtm_client = slack.RTMClient(token=os.environ['SLACK_API_TOKEN'])
    rtm_client.start()

if __name__ == '__main__':
    main()

