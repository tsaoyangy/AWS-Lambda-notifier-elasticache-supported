import requests
import json


class DingTalk:
    s = requests.session()
    secretURL = None

    def __init__(self, url):
        self.secretURL = url

    # Send text alarm
    def send_text_msg(self, dtAlarm):
        url = self.secretURL
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "msgtype": "text",
            "text": {
                "content": dtAlarm.description
            }
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        print(rep.text)
        if rep.status_code == 200:
            content = json.loads(rep.content)
            if content['errcode'] == 0:
                # Success
                # print('Message Sent.')
                pass
            else:
                raise Exception('Errcode: {} , Errmsg: {}'.format(content['errcode'], content['errmsg']))
        else:
            raise Exception('Request failed with status_code: {}'.format(rep.status_code))


if __name__ == '__main__':
    pass