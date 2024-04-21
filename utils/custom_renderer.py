from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework import status
import json


class CustomJsonRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        default_code = renderer_context['response'].status_code
        default_message = '请求成功'

        # 实际请求状态码改成200，以data中的code为准
        if default_code < status.HTTP_200_OK or default_code >= status.HTTP_300_MULTIPLE_CHOICES:
            renderer_context['response'].status_code = status.HTTP_200_OK
            default_message = '请求失败'

        if renderer_context:
            code = default_code
            msg = default_message

            # 改造rest_framework本身的数据结构
            if isinstance(data, dict):
                if data.get('message') is not None:
                    msg = data.pop('message')
                elif data.get('detail') is not None:
                    msg = data.pop('detail')

                if data.get('code') is not None:
                    if isinstance(data.get('code'), int):
                        code = data.pop('code')

                ret = {
                    'code': code,
                    'msg': msg,
                    'data': data if len(data) else None
                }

                return super().render(ret, accepted_media_type,
                                      renderer_context)

        return super().render(data, accepted_media_type, renderer_context)


class CustomBinaryRenderer(BaseRenderer):
    media_type = "application/octet-stream"
    format = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 如果出错返回的是字典信息
        if isinstance(data, dict):
            ret = json.dumps(data)
            return ret.encode()

        return data
