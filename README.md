# 阿里云短信服务之python版本
  https://www.aliyun.com/product/sms

# 版权说明
  爱怎么用就怎么用，不用通知我^_^

# 这个东东很简单，但是我自己写的时候还是掉进了坑，为了节约有需求的程序猿的时间，还是开放出来使用。

# 用法
  SendSms=AliSMSService('http://sms.aliyuncs.com/',你的access_id,你的access_secret,你的SignName,你的TemplateCode)

  SendSms.send_sms(送达手机号码,你设置的模版中的变量对应的值)