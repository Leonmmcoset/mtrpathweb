from django.shortcuts import render, redirect
from django.http import HttpResponse
from .mtrpath import run
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .api import RequestDataSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# 缓存服务器 URL
SERVER_URL_MAP = {
    '1': 'http://leonmmcoset.jjmm.ink:25565',
    '2': 'http://leonmmcoset.jjmm.ink:8810',
    '3': 'http://leonmmcoset.jjmm.ink:8999'
}

def get_selected_option(webis):
    """根据传入的参数返回对应的选中状态"""
    if webis == '1':
        return 'selected', '', ''
    elif webis == '2':
        return '', 'selected', ''
    elif webis == '3':
        return '', '', 'selected'
    return '', '', ''

def get_start_end_value(value):
    """根据传入的值返回格式化后的字符串"""
    return f'value={value}' if value is not None else ''

def get_server_url(server_value):
    """根据传入的服务器选项返回对应的 URL"""
    return SERVER_URL_MAP.get(server_value)

class MyAPIView(APIView):
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ServerID': openapi.Schema(type=openapi.TYPE_STRING, description='服务器 ID'),
            'Start': openapi.Schema(type=openapi.TYPE_STRING, description='起始值'),
            'End': openapi.Schema(type=openapi.TYPE_STRING, description='结束值'),
        },
        required=['ServerIDapi', 'Startapi', 'Endapi']
    )

    @swagger_auto_schema(
        operation_summary="处理POST请求，返回图片ID",
        operation_description="接收ServerID（服务器ID）、Start（起始站）和End（终点站）参数，处理后返回图片ID。\n生成的图片会在<网址>/application/static/generate/generate-<返回ID>.jpg",
        request_body=request_body,
        responses={
            200: openapi.Response('成功返回结果 ID', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='结果 ID')
                }
            )),
            400: openapi.Response('请求参数错误', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='错误信息')
                }
            ))
        }
    )
    def post(self, request):
        serializer = RequestDataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serveridapi = request.data.get('ServerID')
                startapi = request.data.get('Start')
                endapi = request.data.get('End')
                print(serveridapi)
                print(startapi)
                print(endapi)
                result_id = run(startapi, endapi, True, get_server_url(serveridapi), False)
                return Response({"id": result_id}, status=status.HTTP_200_OK)
            except ValueError as ve:
                return Response({"error": f"Value error: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
            except ConnectionError as ce:
                return Response({"error": f"Connection error: {str(ce)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as e:
                return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    # 接收查询符
    webis = request.GET.get('s')
    start = request.GET.get('start')
    end = request.GET.get('end')

    # 获取选中状态和格式化后的起始、结束值
    isa, isb, isc = get_selected_option(webis)
    start = get_start_end_value(start)
    end = get_start_end_value(end)

    if request.method == 'POST':
        # 获取输入框的值并转化为 Python 变量
        input1_value = request.POST.get('input1')
        input2_value = request.POST.get('input2')
        update_value = request.POST.get('input')
        server_value = request.POST.get('server')
        detail_value = request.POST.get('detail')

        # 获取服务器 URL
        server_url = get_server_url(server_value)
        if server_url is None:
            return redirect('error/?r=2')

        # 打印输入信息
        print(f"输入框 1 的值: {input1_value}")
        print(f"输入框 2 的值: {input2_value}")
        print(f'是否更新: {update_value}')
        print(f'服务器: {server_url}')
        print(f'是否显示详细信息：{detail_value}')

        try:
            imageid2 = run(input1_value, input2_value, update_value == '是', server_url, detail_value == '是')
        except Exception as e:
            print(f"运行时出错: {e}")
            return redirect('error/?r=1')

        # 重定向到成功页面
        return redirect(f'image/?id={imageid2}')

    return render(request, 'index.html', {'isa': isa, 'isb': isb, 'isc': isc, 'start': start, 'end': end})

def formtest(request):
    return redirect('../image/')

def stationlist(request):
    stationlist_origin = request.GET.get('s')
    stationlist_name = get_server_url(stationlist_origin)
    if stationlist_name:
        stationlist_name += '/data'

    print(f"""---
    STATION LIST PROGRAM
    ---
    s = {stationlist_name}""")
    return render(request, 'stationlist.html', {'stationlist_name': stationlist_name, 's': stationlist_origin})

def image(request):
    imageid = request.GET.get('id')
    return render(request, 'image.html', {'imageid': imageid})

def error(request):
    errorimage = request.GET.get('r')
    if errorimage == '1':
        errorimage = 'error'
    elif errorimage == '2':
        errorimage = 'error2'
    else:
        errorimage = '1'
    return render(request, 'error.html', {'errorimage': errorimage})

def include(request):
    return render(request, 'include.html')    

def release(request):
    return render(request, 'release.html')

def issue(request):
    return render(request, 'issue.html')