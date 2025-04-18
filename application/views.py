from django.shortcuts import render, redirect
from django.http import HttpResponse
from .mtrpath import run
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .api import RequestDataSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import time
from rest_framework.authentication import SessionAuthentication, BasicAuthentication  
 
class CsrfExemptSessionAuthentication(SessionAuthentication): 
 
    def enforce_csrf(self, request): 
        return  # To not perform the csrf check previously happening
        
# 缓存服务器 URL（新增服务器4）
SERVER_URL_MAP = {
    '1': 'http://leonmmcoset.jjmm.ink:25565',
    '2': 'http://leonmmcoset.jjmm.ink:8810',
    '3': 'http://leonmmcoset.jjmm.ink:8999',
    '4': 'http://zhuimeng.9666.fun:32870'  # 新增服务器配置
}

def get_selected_option(webis):
    """支持4个服务器的选中状态判断"""
    if webis == '1':
        return 'selected', '', '', ''       # 服务器1选中
    elif webis == '2':
        return '', 'selected', '', ''       # 服务器2选中
    elif webis == '3':
        return '', '', 'selected', ''       # 服务器3选中
    elif webis == '4':                    # 新增服务器4的判断
        return '', '', '', 'selected'       # 服务器4选中
    else:
        return '', '', '', ''               # 无选中状态

def get_start_end_value(value):
    """保持原有参数处理逻辑"""
    return f'value={value}' if value is not None else ''

def get_server_url(server_value):
    """保持原有URL获取逻辑，自动支持新服务器ID"""
    return SERVER_URL_MAP.get(server_value)

class MyAPIView(APIView):
    """API接口保持原有逻辑，自动支持新增的服务器ID=4"""
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ServerID': openapi.Schema(type=openapi.TYPE_STRING, description='服务器ID（支持1-4）'),
            'Start': openapi.Schema(type=openapi.TYPE_STRING, description='起始站'),
            'End': openapi.Schema(type=openapi.TYPE_STRING, description='终点站'),
        },
        required=['ServerID', 'Start', 'End']
    )

    @swagger_auto_schema(
        operation_summary="处理POST请求，返回图片ID",
        operation_description="接收ServerID（服务器ID）、Start（起始站）和End（终点站）参数，处理后返回图片ID。\n生成的图片会在<网址>/application/static/generate/generate-<返回ID>.jpg",
        request_body=request_body,
        responses={
            200: openapi.Response('成功返回图片ID', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='图片ID'),
                    'time': openapi.Schema(type=openapi.TYPE_STRING, description='输出结果的时间')
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
                timeapi = time.ctime()
                result_id = run(startapi, endapi, True, get_server_url(serveridapi), False)
                return Response({"id": result_id, "time": timeapi}, status=status.HTTP_200_OK)
            except ValueError as ve:
                return Response({"error": f"Value error: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
            except ConnectionError as ce:
                return Response({"error": f"Connection error: {str(ce)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as e:
                return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    """处理前端页面的服务器选择和表单提交"""
    webis = request.GET.get('s', '1')  # 默认选中服务器1（可根据需求调整）
    start = request.GET.get('start')
    end = request.GET.get('end')

    # 获取四个服务器的选中状态（新增isd对应服务器4）
    isa, isb, isc, isd = get_selected_option(webis)
    start = get_start_end_value(start)
    end = get_start_end_value(end)

    if request.method == 'POST':
        input1_value = request.POST.get('input1')
        input2_value = request.POST.get('input2')
        update_value = request.POST.get('input')  # 默认为不更新
        server_value = request.POST.get('server', '1')  # 默认为服务器1
        detail_value = request.POST.get('detail')  # 默认为不显示详细

        server_url = get_server_url(server_value)
        if not server_url:
            return redirect('error/?r=2')  # 无效服务器ID

        try:
            imageid2 = run(input1_value, input2_value, update_value == True, server_url, detail_value == True)
        except Exception as e:
            print(f"运行时错误: {e}")
            return redirect('error/?r=1')

        return redirect(f'image/?id={imageid2}')

    # 传递四个选中状态到模板（需确保模板包含四个服务器选项）
    return render(request, 'index.html', {
        'isa': isa,
        'isb': isb,
        'isc': isc,
        'isd': isd,  # 新增服务器4的选中状态
        'start': start,
        'end': end
    })

# 以下视图函数无需修改，自动支持新服务器逻辑
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
    errorimage = request.GET.get('r', '1')
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