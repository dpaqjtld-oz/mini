from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient


def main():
    print("🤖 임베딩 모델 로딩 중... (약간의 시간이 걸립니다)")
    # 1. 텍스트를 벡터로 변환하는 모델 (데이터를 넣을 때 썼던 모델과 '반드시' 똑같은 모델을 써야 합니다!)
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')

    # 2. 우리가 만든 로컬 Vector DB(qdrant_db 폴더)에 연결
    client = QdrantClient(path="./qdrant_db")
    collection_name = "semiconductor_regulations"

    print("\n=============================================")
    print("🔍 AI 반도체 규제 검색 에이전트에 오신 것을 환영합니다!")
    print("=============================================\n")

    # 3. 유저에게 질문을 입력받는 무한 루프 시작
    while True:
        # input() 함수로 터미널에서 직접 질문을 입력받습니다.
        query = input("❓ 궁금한 수출 규제를 물어보세요 (종료하려면 'q' 입력): ")

        if query.lower() == 'q':
            print("👋 검색을 종료합니다.")
            break

        if not query.strip():
            continue

        # 4. 유저의 질문을 768개의 숫자(벡터)로 변환
        # (이때 LLM API 비용이 전혀 들지 않고 내 PC의 자원만 씁니다.)
        query_vector = model.encode(query).tolist()

        # 5. Vector DB 검색: 질문 벡터와 가장 유사한(각도가 좁은) 데이터 2개 찾기
        search_response = client.query_points(
            collection_name=collection_name,
            query=query_vector,  # query_vector 대신 query 매개변수에 바로 넣습니다.
            limit=2
        )

        print("\n💡 [검색 결과 Top 2]")
        print("-" * 40)

        # query_points의 결과물은 .points 안에 리스트로 담겨서 나옵니다.
        for i, hit in enumerate(search_response.points):
            # 최신 버전에서는 score 대신 이 문맥과 얼마나 일치하는지 숫자로 보여줍니다.
            print(f"[{i + 1}순위]")
            print(f" 🔹 조항: {hit.payload.get('title')}")
            print(f" 🔹 내용: {hit.payload.get('content')}")
            print("-" * 40)
        print("\n")


if __name__ == "__main__":
    main()