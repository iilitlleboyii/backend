from user.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, renderer_classes

from utils.custom_renderer import CustomBinaryRenderer
from urllib.parse import unquote
from io import BytesIO

import os
import pandas as pd


# Create your views here.
class UploadFile(APIView):

    def post(self, request):
        return Response(data={'message': "上传成功!"}, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
@renderer_classes((CustomBinaryRenderer,))
class DownloadFile(APIView):

    def post(self, request):
        content_disposition = request.headers['Content-Disposition']
        content_type = request.headers['Content-Type']
        index = content_disposition.find("filename=")
        if index != -1:
            file_name = unquote(content_disposition[index + len("filename="):])
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                     'static', 'files', file_name)
            try:
                with open(file_path, 'rb') as f:
                    return Response(
                        data=f.read(),
                        status=status.HTTP_200_OK,
                        content_type=content_type,
                        headers={'Content-Disposition': content_disposition})
            except FileNotFoundError:
                return Response(data={'message': "文件不存在!"},
                                status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        data = User.objects.all().values()
        df = pd.DataFrame(list(data))

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return Response(
            data=output.getvalue(),
            content_type='application/octet-stream',
            headers={'Content-Disposition': 'attachment;filename="users.xlsx"'})
