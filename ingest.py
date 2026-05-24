import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


def main():
    # 1. 임베딩 모델 로드 (화두: 왜 이 모델을 쓸까?)
    # 'jhgan/ko-sroberta-multitask'는 한국어 문장 의미 추출에 압도적인 성능을 내는 실무 표준 모델입니다.
    print("🤖 임베딩 모델 로딩 중...")
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')

    # 2. Vector DB 초기화 (Qdrant)
    # 초기 테스트를 위해 무거운 Docker 대신 로컬 폴더('./qdrant_db')에 데이터를 저장하는 모드를 씁니다.
    client = QdrantClient(path="./qdrant_db")
    collection_name = "semiconductor_regulations"

    # 컬렉션(테이블)이 없으면 생성 (벡터 차원수 768은 위 모델의 출력 크기와 동일해야 함)
    if not client.collection_exists(collection_name):
        print(f"🗄️ '{collection_name}' 컬렉션 생성 중...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

    # 3. CSV 데이터 읽기
    df = pd.read_csv('data/regulations.csv')

    # 4. 텍스트를 벡터로 변환하고 DB에 적재 (Upsert)
    points = []
    for index, row in df.iterrows():
        # 어떤 텍스트를 벡터로 만들지 결정 (제목과 내용을 합쳐서 의미를 풍부하게 함)
        text_to_embed = f"제목: {row['title']} | 내용: {row['content']}"

        # 모델을 통과하면 768개의 숫자(Float)로 이루어진 리스트가 나옵니다.
        vector = model.encode(text_to_embed).tolist()

        # Vector DB에 넣을 데이터 구조체 생성 (메타데이터 포함)
        points.append(PointStruct(
            id=int(row['id']),
            vector=vector,
            payload={"title": row['title'], "content": row['content'], "category": row['category']}
        ))

    # DB에 밀어넣기
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    print("✅ 3개의 규제 데이터가 Vector DB에 성공적으로 적재되었습니다!")


if __name__ == "__main__":
    main()