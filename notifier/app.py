import boto3
import os
import json

from botocore.exceptions import ClientError

from dingtalk import DingTalk
from alarm import Alarm
from converse_api import converseApiCaller

secretArn = os.environ['SECRET_ARN']
enableDebug = os.environ['ENABLE_DEBUG']
enableLlm = os.environ['EnableLLM']
llmRegion = os.environ['LLM_REGION']
llmModelID = os.environ['LLM_MODEL_ID']
llmMaxTokens = os.environ['LLM_Max_Tokens']
systemPrompt = os.environ['System_Prompt']

# Get chat bot URL includes token from Secrets Manager
secret_manager_client = boto3.client('secretsmanager')
get_secret_value_response = secret_manager_client.get_secret_value(
    SecretId=secretArn
)
secretURL = get_secret_value_response['SecretString']

# Initial DingTalk handler
dingtalk = DingTalk(secretURL)

# Convert string to boolean
def str_to_bool(str):
    if str.lower() == 'true':
        return True
    elif str.lower() == 'false':
        return False
    else:
        return False
        
def lambda_handler(event, context):
    print(event)

    message = event['Records'][0]['Sns']['Message']
    
    if "ElastiCache:Failover" in message:
        msg = elasticache_msg_format(event)
        print("ElastiCache message:" + msg)
    elif "ElastiCache" in message:
        # 如果是其他的 ElastiCache 事件，不进行处理
        print("Other ElastiCache event, no formatting applied.")
        return {
            "statusCode": 200,
            "body": "No action taken for other ElastiCache events."
        }
    else:
        msg = msg_format(event)
        print("Original message:" + msg)

    enableLlmBool = str_to_bool(enableLlm)
    enableDebugBool = str_to_bool(enableDebug)

    if enableLlmBool:
        converseApi = converseApiCaller(region=llmRegion, model_id=llmModelID, max_tokens=int(llmMaxTokens),
                                        prompt=systemPrompt,
                                        enable_debug=enableDebugBool)

        try:
            llmRsp = converseApi.invoke_converse_api(input_text=msg)
            msg = llmRsp + "\n\n------------------\nOriginal message:\n" + msg
        except ClientError as err:
            print("Invoke Bedrock Converse API error:")
            print(err.response["Error"]["Code"])
            print(err.response["Error"]["Message"])

    dtAlarm = Alarm(
        description=msg,
    )

    dingtalk.send_text_msg(dtAlarm)

    response = {
        "statusCode": 200,
        "body": "Message Sent."
    }

    return response

def msg_format(event):
    try:
        # 消息来源是SNS，取 $.Records[0].Sns.Message，并对字符串进行一些处理，确保发送时可以正常显示
        msg = event['Records'][0]['Sns']['Message']

        # 进行字符串处理后返回，以确保IM客户端正确显示
        msg = msg.replace("\\n", "\n")
        if msg[0] == '\"' and msg[-1] == '\"':
            msg = msg[1:-1]

        return msg
    except:
        # 消息来源不是SNS，直接返回
        return event
        
# elasticache消息格式化函数        
def elasticache_msg_format(event):
    sns_msg = json.loads(event['Records'][0]['Sns']['Message'])
    event_time = event['Records'][0]['Sns']['Timestamp']
    event_region = event['Records'][0]['EventSubscriptionArn'].split(':')[3]
    formatted_msg = f"ElastiCache事件报警:\n事件发生时间: {event_time}\n区域: {event_region}\n事件详情：{sns_msg}"
    return formatted_msg
