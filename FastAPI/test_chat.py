import requests

url = "http://127.0.0.1:8000/ask"
headers = {"Content-Type": "application/json"}

# 테스트할 질문 예시
data = {
    "text": "부처님오신날로 인한 보강 날짜가 언제야?"
}

try:
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        res_json = response.json()
        print("✅ 응답 성공!")
        print("답변:", res_json.get("answer"))
        print("참조 문서:")
        for doc in res_json.get("source_docs", []):
            print(f" - {doc['id']}: {doc['title']}")
    else:
        print("❌ 상태 코드:", response.status_code)
        print("⚠️ 응답 내용:", response.text)
except Exception as e:
    print("❌ 요청 실패:", e)
