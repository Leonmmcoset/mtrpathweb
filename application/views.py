from django.shortcuts import render, redirect
from django.http import HttpResponse
from .mtrpath import run

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
            run(input1_value, input2_value, update_value == '是', server_url, detail_value == '是')
        except Exception as e:
            print(f"运行时出错: {e}")
            return redirect('error/?r=1')

        # 重定向到成功页面
        return redirect('formtest/')

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
    return render(request, 'image.html')

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