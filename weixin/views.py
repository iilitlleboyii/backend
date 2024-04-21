from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json


# Create your views here.
class WeixinLoginView(APIView):
    """
    微信小程序手机授权登录
    """

    grant_type = "client_credential"
    appid = "wx473037a848b5ef8b"
    secret = "f4ed59dcea7fa624e2a5e7fb82fb0c23"
    url1 = "https://api.weixin.qq.com/cgi-bin/token"
    url2 = "https://api.weixin.qq.com/wxa/business/getuserphonenumber"

    def post(self, request):
        params1 = {
            "grant_type": self.grant_type,
            "appid": self.appid,
            "secret": self.secret
        }
        params2 = {
            "access_token":
                requests.get(url=self.url1,
                             params=params1).json().get('access_token')
        }
        data2 = {"code": request.data.get('code')}

        ret = requests.post(url=self.url2,
                            params=params2,
                            data=json.dumps(data2)).json().get('phone_info')

        return Response(ret)
