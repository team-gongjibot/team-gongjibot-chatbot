import requests

url = "https://fd19-34-125-151-143.ngrok-free.app/ping"

try:
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("status") == "pong":
        print("✅ FastAPI 서버가 정상 작동 중입니다.")
    else:
        print("⚠️ 서버는 켜져 있지만 예상과 다른 응답입니다:", response.text)
except Exception as e:
    print("❌ FastAPI 서버에 연결할 수 없습니다:", e)
