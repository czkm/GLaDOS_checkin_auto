import requests
import json

def send_glados_checkin():
    url = "https://glados.network/api/user/checkin"
    headers = {
        'cookie': 'koa:sess=eyJ1c2VySWQiOjI5MDA3LCJfZXhwaXJlIjoxNzc1MzUxNzMyNjM5LCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=HJ27gHpPm7nCBPLo0gIGffCIujw',
        'referer': 'https://glados.network/console/checkin',
        'origin': 'https://glados.network',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8'
    }
    payload = {"token": "glados.one"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        print(f"请求状态码: {response.status_code}")
        print(f"请求响应: {response.text}")

        try:
            response_data = response.json()
            message = response_data.get('message', '未知签到结果')
            points = response_data.get('points', 0)
            print(f"签到结果: {message}, 获得点数: {points}")
            return response_data
        except json.JSONDecodeError:
            print("API返回非JSON格式")
            return None

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None

if __name__ == "__main__":
    send_glados_checkin()
