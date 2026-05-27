# CODE_FLOW.md - 코드 실행 흐름 이해

---

## ingest.py 실행 흐름

> **한 줄 요약:** CSV 파일을 읽어서 텍스트를 숫자(벡터)로 변환한 뒤 Qdrant DB에 저장하는 스크립트

```
python ingest.py 실행
        │
        ▼
① 임베딩 모델 로드
   SentenceTransformer('jhgan/ko-sroberta-multitask')
   → 한국어 문장을 숫자 배열로 바꿔주는 AI 모델을 메모리에 올림
        │
        ▼
② Qdrant DB 연결
   QdrantClient(path="./qdrant_db")
   → 로컬 폴더(qdrant_db/)를 DB로 사용
        │
        ▼
③ 컬렉션(테이블) 존재 여부 확인
   client.collection_exists("semiconductor_regulations")
        │
        ├── 없으면 → create_collection() 으로 새로 생성
        │           size=768 (모델 출력 크기), distance=COSINE
        │
        └── 있으면 → 그냥 넘어감
        │
        ▼
④ CSV 파일 읽기
   pd.read_csv('data/regulations.csv')
   → id, title, content, category 컬럼 3행 로드
        │
        ▼
⑤ 반복문 (행마다 반복)
   for index, row in df.iterrows():
        │
        ▼
   ⑤-1. 임베딩할 텍스트 조합
         text = "제목: {title} | 내용: {content}"
         → 제목+내용을 합쳐야 의미가 풍부해져서 검색 품질 향상
        │
        ▼
   ⑤-2. 텍스트 → 벡터 변환
         model.encode(text).tolist()
         → "제목: 미국 EAR..." → [0.23, -0.11, 0.87, ...] 768개 숫자
        │
        ▼
   ⑤-3. PointStruct 생성
         PointStruct(
           id=1,
           vector=[0.23, -0.11, ...],   ← 검색에 사용
           payload={title, content, category}  ← 검색 후 꺼낼 원본 텍스트
         )
        │
        ▼
⑥ DB에 저장
   client.upsert(points=[...])
   → 3개 포인트 한꺼번에 DB에 밀어넣기
   → upsert = 없으면 insert, 있으면 update
        │
        ▼
⑦ 완료 메시지 출력 후 종료
```

---

## search.py 실행 흐름

> **한 줄 요약:** 유저 질문을 벡터로 변환해서 DB 안의 벡터들과 비교, 가장 비슷한 규제 조항 2개를 꺼내 출력

```
python search.py 실행
        │
        ▼
① 임베딩 모델 로드
   SentenceTransformer('jhgan/ko-sroberta-multitask')
   → ⚠️ ingest.py와 반드시 같은 모델 사용
     (다른 모델 쓰면 벡터 공간이 달라져 검색 결과 엉망)
        │
        ▼
② Qdrant DB 연결
   QdrantClient(path="./qdrant_db")
   → ingest.py가 저장해둔 DB에 연결
        │
        ▼
③ 무한 루프 시작 (while True)
        │
        ▼
   ③-1. 유저 질문 입력 대기
         query = input("❓ 궁금한 수출 규제를 물어보세요")
        │
        ├── 'q' 입력 → break → 프로그램 종료
        ├── 공백 입력 → continue → 다시 입력 대기
        │
        └── 질문 입력됨 → 다음 단계로
        │
        ▼
   ③-2. 질문 → 벡터 변환
         model.encode(query).tolist()
         "HBM3 중국 수출 가능?" → [0.15, 0.32, -0.44, ...] 768개 숫자
        │
        ▼
   ③-3. Qdrant 검색
         client.query_points(
           collection_name="semiconductor_regulations",
           query=query_vector,
           limit=2
         )
         → DB 안의 모든 벡터와 코사인 유사도 계산
         → 유사도 높은 순으로 2개 반환
        │
        ▼
   ③-4. 결과 출력
         for hit in search_response.points:
           hit.payload['title']    → 규제 조항 제목
           hit.payload['content']  → 규제 조항 내용
        │
        ▼
   ③-5. 다시 ③-1로 돌아가 다음 질문 대기
```

---

## 두 파일의 관계

```
[ingest.py]                      [search.py]
    │                                │
    │  같은 모델 사용                 │
    │  jhgan/ko-sroberta-multitask   │
    │                                │
    ▼                                ▼
텍스트 → 벡터로 변환         질문 → 벡터로 변환
    │                                │
    ▼                                ▼
qdrant_db/ 에 저장    →      qdrant_db/ 에서 검색
```

> ingest.py 를 먼저 실행해야 qdrant_db/ 폴더가 생김
> search.py 는 그 DB가 있어야 동작함

---

## 코사인 유사도란?

```
"미국 EAR 반도체 수출 통제" 벡터  →  [0.23, -0.11, 0.87, ...]
"HBM3 중국 수출 가능?" 벡터       →  [0.21, -0.09, 0.91, ...]
                                         ↑ 숫자들이 비슷함 = 의미가 비슷함

"오늘 점심 뭐 먹지?" 벡터          →  [-0.55, 0.73, -0.12, ...]
                                         ↑ 숫자들이 다름 = 의미가 다름
```

두 벡터가 같은 방향을 가리킬수록 유사도 1에 가까움
다른 방향을 가리킬수록 유사도 0(또는 -1)에 가까움

---

## search.py 의 한계 (다음 단계 RAG로 해결)

```
현재 search.py
유저 질문 → 벡터 검색 → 조항 텍스트 출력 (여기서 끝)

다음 단계 api.py (RAG)
유저 질문 → 벡터 검색 → 조항 텍스트 → LLM 프롬프트에 주입 → LLM 답변 생성
                                              ↑
                                       이 부분이 RAG 핵심
```
