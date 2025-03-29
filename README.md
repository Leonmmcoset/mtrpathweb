![mtrpathweb](https://socialify.git.ci/leonmmcoset/mtrpathweb/image?custom_description=Leon%E5%BC%80%E6%9C%8D%E7%BD%91%E5%AF%BC%E8%88%AA%E7%B3%BB%E7%BB%9F%E6%BA%90%E7%A0%81&description=1&font=Source+Code+Pro&forks=1&issues=1&language=1&logo=https%3A%2F%2Flogospng.org%2Fdownload%2Fdjango%2Fdjango-1536.png&name=1&owner=1&pattern=Signal&pulls=1&stargazers=1&theme=Light)
# Leon开服网导航系统
[Leon开服网导航系统](http://leonmmcoset.jjmm.ink:8010)的源代码

## 简介
Leon开服网导航系统的源代码，内含两站之间导航、查找站点等功能

## 搭建教程
#### 1.下载源代码
使用
``` shell
git clone https://github.com/leonmmcoset/mtrpathweb.git
```
或在发行页面下载源代码压缩包
#### 2.下载第三方库
用
``` shell
pip install -r requirements.txt
```
进行下载（Python环境必须为`>=3.6`，`<3.13`）
#### 3. 搭建网站
##### Windows
编辑`start.bat`，将里面的`10.0.0.10:8010`更改为适用于你自己的IP和端口（如`localhost:80`等）
##### Linux
运行命令
``` shell
python manage.py runserver <你自己的IP和端口> --insecure
```
即可
#### 4. 更改源代码
根据你的需求，自由更改源代码

如有问题，可在[Discussions](https://github.com/Leonmmcoset/mtrpathweb/discussions)问我。