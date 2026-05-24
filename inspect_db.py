from qdrant_client import QdrantClient


def main():
    # 1. 데이터가 저장된 로컬 폴더에 연결
    client = QdrantClient(path="./qdrant_db")
    collection_name = "semiconductor_regulations"

    print(f"🗄️ '{collection_name}' 컬렉션 상태 확인 중...")

    # 2. 컬렉션 정보 조회 (데이터가 몇 개나 들어있는지 확인)
    collection_info = client.get_collection(collection_name=collection_name)
    print(f"📊 총 저장된 데이터 개수(Points): {collection_info.points_count}개")

    # 3. 저장된 데이터 전체 스캔 (RDBMS의 SELECT * 와 같은 역할)
    # Vector DB에서는 이를 'scroll(스크롤)'이라고 부릅니다.
    records, next_page_offset = client.scroll(
        collection_name=collection_name,
        limit=10,  # 가져올 데이터 개수 제한
        with_payload=True,  # 등록한 텍스트 데이터(제목, 내용 등) 포함 여부
        with_vectors=False  # 768개의 실수 배열이 콘솔에 쏟아지면 보기 힘드므로 꺼둡니다.
    )

    print("\n📝 Vector DB에 저장된 규제 데이터 실물:")
    for record in records:
        print(f"\n[데이터 고유 ID: {record.id}]")
        print(f" 🔹 제목: {record.payload.get('title')}")
        print(f" 🔹 내용: {record.payload.get('content')}")
        print(f" 🔹 카테고리: {record.payload.get('category')}")


if __name__ == "__main__":
    main()