import json
import boto3
import os
from wechat import Wechat
from alarm import Alarm

corpId = os.environ['CORPID']
corpSecret = os.environ['CORPSECRET']
agentId = os.environ['AGENTID']

#初始化，并连接企业微信接口获取 Access Token
wechat = Wechat(corpId, corpSecret)

def lambda_handler(event, context):
    #消息来源是SNS，取 $.Records[0].Sns.Message，并对字符串进行一些处理，确保发送至微信时可以正常显示
    msg = event['Records'][0]['Sns']['Message']
    msg = msg.replace("\\n", "\n")
    msg = msg[1:-1]
    
    wxAlarm = Alarm(
        toUser = "@all",  #成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
        toParty = "",     #部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
        toTag = "",       #标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
        agentId = agentId,
        description = msg,
    )
    
    wechat.send_text_msg(wxAlarm)
    
    response = {
        "statusCode": 200,
        "body": "Message Sent to WeChat."
    }

    return response