#test 코드
import requests

url = "https://2930-34-125-151-143.ngrok-free.app/ask"
headers = {"Content-Type": "application/json"}

# 테스트할 질문 예시
data = {
    "text": "니 이름은 뭐니?"
}

try:
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        res_json = response.json()
        print("✅ 응답 성공!")
        print("📌 답변:", res_json.get("answer"))
        print("📎 참조 문서:")
        for doc in res_json.get("source_docs", []):
            print(f" - {doc['id']}: {doc['title']}")
    else:
        print("❌ 상태 코드:", response.status_code)
        print("⚠️ 응답 내용:", response.text)

except Exception as e:
    print("❌ 요청 실패:", e)
