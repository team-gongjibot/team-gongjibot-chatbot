import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 현재 상위 디렉토리를 sys.path에 추가
import json
from services.indexing import build_faiss_index

def test_build_faiss_index():
    # 현재 디렉토리 기준 상위 폴더에 파일들이 있다고 가정
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "announcements.json")
    index_path = os.path.join(base_dir, "announcements.index")

    # 테스트 전에 기존 인덱스 삭제 (있을 경우)
    if os.path.exists(index_path):
        os.remove(index_path)

    print(f"🔍 JSON 경로: {json_path}")
    print(f"📦 FAISS 인덱스 경로: {index_path}")

    # 인덱스 생성 테스트
    result = build_faiss_index(json_path=json_path, index_path=index_path)

    # 결과 출력
    print("\n=== 테스트 결과 ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 간단한 검증
    assert result["status"] == "success", "FAISS 인덱스 생성 실패"
    assert os.path.exists(index_path), "FAISS 인덱스 파일이 생성되지 않았음"
    assert result["count"] > 0, "임베딩된 문서 수가 0임"

    print("\n✅ 테스트 통과!")

if __name__ == "__main__":
    test_build_faiss_index()

from services.indexing import build_faiss_index

if __name__ == "__main__":
    result = build_faiss_index("announcements.json", "announcements.index")
    print(result)
    

