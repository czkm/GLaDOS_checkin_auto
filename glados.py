import requests
import json
import os

if __name__ == '__main__':
    sckey = os.environ.get("PUSHPLUS_TOKEN", "")
    cookies = os.environ.get("GLADOS_COOKIE", "").split("&") if os.environ.get("GLADOS_COOKIE") else []
    
    if not cookies or cookies == [""]:
        print('未获取到COOKIE变量')
        exit(1)
    
    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload = {'token': 'glados.one'}
    send_content = ''
    
    for cookie in cookies:
        if not cookie.strip():
            print("跳过空cookie")
            continue
            
        try:
            # 发送签到请求
            checkin = requests.post(
                url,
                headers={
                    'cookie': cookie,
                    'referer': referer,
                    'origin': origin,
                    'user-agent': useragent,
                    'content-type': 'application/json;charset=UTF-8'
                },
                data=json.dumps(payload),
                timeout=10
            )
            # 调试：打印签到请求的响应
            print(f"签到请求状态码: {checkin.status_code}")
            print(f"签到请求响应: {checkin.text}")
            
            # 获取状态
            state = requests.get(
                url2,
                headers={
                    'cookie': cookie,
                    'referer': referer,
                    'origin': origin,
                    'user-agent': useragent
                },
                timeout=10
            )
            # 调试：打印状态请求的响应
            print(f"状态请求状态码: {state.status_code}")
            print(f"状态请求响应: {state.text}")
            
            # 尝试解析 JSON
            try:
                state_data = state.json()
            except json.JSONDecodeError:
                print("状态API返回非JSON格式")
                send_content += "状态API返回非JSON格式\n"
                continue
                
            # 检查响应结构
            if 'data' not in state_data:
                print(f"状态API未返回'data'键，完整响应: {state_data}")
                send_content += f"状态API未返回'data'键: {state_data}\n"
                continue
                
            time = str(state_data['data'].get('leftDays', '0')).split('.')[0]
            email = state_data['data'].get('email', 'Unknown')
            
            # 解析签到结果
            try:
                checkin_data = checkin.json()
            except json.JSONDecodeError:
                print("签到API返回非JSON格式")
                send_content += "签到API返回非JSON格式\n"
                continue
                
            if 'message' in checkin_data:
                mess = checkin_data['message']
                log = f"{email}----结果--{mess}----剩余({time})天"
                print(log)
                send_content += log + '\n'
            else:
                print(f"{email}----签到失败，cookie可能失效")
                send_content += f"{email}----签到失败，cookie可能失效\n"
                if sckey:
                    requests.get(
                        f"https://www.pushplus.plus/send?token={sckey}&content={email}+cookie已失效",
                        timeout=10
                    )
                    
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            send_content += f"请求失败: {e}\n"
    
    # 发送汇总通知
    if sckey and send_content:
        try:
            requests.get(
                f"https://www.pushplus.plus/send?token={sckey}&title=Glados签到报告&content={send_content}",
                timeout=10
            )
            print("推送通知发送成功")
        except requests.RequestException as e:
            print(f"推送通知失败: {e}")
