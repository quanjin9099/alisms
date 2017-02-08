# coding=utf-8

import base64
import hmac
from hashlib import sha1
import urllib
import time
import uuid
import json,requests


class AliSMSService:
    access_id=''
    access_secret=''
    SignName=''
    TemplateCode=''
    def __init__(self, url,access_id,access_secret,SignName,TemplateCode):
        self.access_id =access_id
        self.access_secret =access_secret
        self.url = url
        self.SignName=SignName
        self.TemplateCode=TemplateCode

    # 签名
    def sign(self, access_Secret, parameters,Method='POST'):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''

        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        strSign = Method+'&%2F&' + self.percent_encode(canonicalizedQueryString[1:])
        h = hmac.new(access_Secret + "&", strSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return self.percent_encode(signature)

    def percent_encode(self, encodeStr):#这个函数来自网络
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.decode('utf-8').encode('utf-8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self, params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'AccessKeyId': self.access_id,
            'Action':'SingleSendSms',
            'Format': 'JSON',
            'SignName': self.SignName,
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'SignatureVersion': '1.0',
            'TemplateCode': self.TemplateCode,
            'Timestamp': timestamp,
            'Version': '2016-09-27',
        }
        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature
        str_params=urllib.urlencode(parameters)
        return str_params.replace('%25', '%')

    def _post_web_data(self,url,params=[],heads='',cookies='',proxyies={}):
        state='200'
        try:
            response = requests.post(url,data=params,headers=heads,cookies=cookies,timeout=50,proxies=proxyies)
            data=response.text
            response.close()
            if not response.status_code==200:
                return str(response.status_code),data
        except Exception, e:
            data = None
            state = str(e)
        return state,data

    def send_sms(self,tel,code):
        _params={
            'ParamString': {'code':code},#这个地方替换成你模版中的代码
            'RecNum':tel,
        }
        _Signature=self.make_url(_params)
        _headers={
            'Content-Type':'application/x-www-form-urlencoded',
        }
        data=self._post_web_data(self.url,params=_Signature,heads=_headers)
        if data[0]!='200':
            return False
        ksjon=json.loads(data[1])
        if ksjon.get('errcode','')=='' and ksjon.get('Model','')!='':
            return True
        else:
            return False

if __name__=='__main__':
    SendSms=AliSMSService('http://sms.aliyuncs.com/','','','','')
    print SendSms.send_sms('','')