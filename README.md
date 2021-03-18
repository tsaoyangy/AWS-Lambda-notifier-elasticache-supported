# WeChat-Notifier 微信告警通知

### 在 Serverless Application Repository 中部署此应用


- 登陆 AWS Console 并切换至 `Serverless Application Repository`服务
- 搜索 `WeChat-Notifier` 找到这个Serverless应用，点击进入部署页面
- 输入企业微信配置相关参数然后点击`部署`即可

### 使用

本应用会部署出一个Lambda函数用于将消息发送至企业微信，同时也部署一个SNS Topic并配置Lambda做为Subscription. 用户可以将消息发送至 SNS Topic 即可触发 Lambda 将消息发送给企业微信。 

EventBridge 中也可以创建 Rule ，将AWS相关的事件推送至企业微信。

### 致谢

本项目使用的企业微信对接代码是在 Niko Feng 之前[项目](https://github.com/nikosheng/wechat-lambda-layer-sam)的基础上增加了异常处理，在此对 Niko 表示感谢！