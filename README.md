# 🔍 AI 기반 반도체 수출 규제 리스크 분석 에이전트

> 반도체 부품 수출에 대해 질문하면, RAG 파이프라인으로 관련 규제 조항을 찾고
> LLM이 리스크 여부를 판단해 **실시간 스트리밍**으로 답변하는 AI 시스템

---

## 📌 프로젝트 소개

반도체 수출 규제는 조항이 복잡하고 방대해 단순 키워드 검색으로는 한계가 있습니다.
이 프로젝트는 유저가 자연어로 질문하면 벡터 DB에서 관련 규제 조항을 찾아
LLM이 리스크를 분석하고 실시간으로 답변하는 **RAG(Retrieval-Augmented Generation) 시스템**입니다.

```
예시 질문: "HBM3 칩을 중국에 수출해도 되나요?"
예시 답변: "미국 EAR 규정 및 칩스법 조건에 따르면, HBM3 칩은 14나노 이하
            첨단 반도체에 해당하여 중국 수출이 원칙적으로 제한됩니다..."
```

---

## 🏗️ 시스템 아키텍처

```
유저 질문
    ↓
FastAPI /query
    ↓
SentenceBERT → 벡터(768차원) 변환
    ↓
Qdrant 코사인 유사도 검색 → 관련 규제 조항 Top 3
    ↓
프롬프트에 규제 조항 주입 (RAG 핵심)
    ↓
OpenAI API 호출 (gpt-4o-mini, stream=True)
    ↓
SSE 실시간 스트리밍 → 브라우저
```

---

## 🛠️ 기술 스택

| 분류 | 기술 | 설명 |
|------|------|------|
| **Language** | Python 3.10 | |
| **Backend** | FastAPI, Uvicorn | 비동기 API 서버 |
| **Vector DB** | Qdrant | 로컬 파일 모드, 벡터 유사도 검색 |
| **Embedding** | SentenceBERT | `jhgan/ko-sroberta-multitask` (768차원) |
| **LLM** | OpenAI API | `gpt-4o-mini` 스트리밍 모드 |
| **Streaming** | SSE | Server-Sent Events 실시간 전송 |
| **Frontend** | HTML + JavaScript | 단일 파일 채팅 UI |

---

## 📁 프로젝트 구조

```
mini/
├── data/
│   └── regulations.csv      # 반도체 규제 원본 데이터
├── docs/
│   ├── plan.md              # 프로젝트 기획 및 역할 분담
│   ├── ARCHITECTURE.md      # 시스템 구성도 및 플로우차트
│   ├── DATA_SCHEMA.md       # 데이터 구조 정의
│   ├── API_SPEC.md          # API 엔드포인트 명세
│   └── CODE_FLOW.md         # 코드 실행 흐름 설명
├── templates/
│   └── index.html           # 프론트엔드 채팅 UI
├── qdrant_db/               # Qdrant 로컬 벡터 DB (gitignore)
├── ingest.py                # 데이터 임베딩 → Qdrant 적재 (1회 실행)
├── search.py                # 벡터 검색 테스트 CLI
├── api.py                   # FastAPI 메인 서버
├── CLAUDE.md                # Claude Code 협업 설정
├── requirements.txt         # Python 패키지 목록
└── .env                     # 환경변수 (gitignore)
```

---

## ⚙️ 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/dpaqjtld-oz/mini.git
cd mini
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

루트에 `.env` 파일 생성:

```
OPENAI_API_KEY=sk-...
```

### 4. 데이터 적재 (최초 1회)

```bash
python ingest.py
```

### 5. 서버 실행

```bash
uvicorn api:app --reload
```

### 6. 접속

브라우저에서 `http://localhost:8000` 접속

---

## 🚀 주요 기능

- **자연어 질문** — 복잡한 규제 조항을 자연어로 질문
- **RAG 검색** — 벡터 유사도 기반으로 관련 규제 조항 Top 3 자동 추출
- **실시간 스트리밍** — SSE 방식으로 LLM 답변을 타이핑 효과로 표시
- **한국어 최적화** — 한국어 특화 임베딩 모델 사용

---

## 👥 팀원 & 역할

| 이름 | 역할 | 담당 |
|------|------|------|
| **동훈** | RAG Retrieval | 데이터 적재, Qdrant 검색 모듈, 프롬프트 설계, FastAPI 서버 구조 |
| **팀원** | RAG Generation | OpenAI API 연결, SSE 스트리밍 구현, 프론트엔드 |

---

## 📌 참고 문서

- [API 명세서](docs/API_SPEC.md)
- [시스템 아키텍처](docs/ARCHITECTURE.md)
- [데이터 스키마](docs/DATA_SCHEMA.md)
- [코드 흐름 설명](docs/CODE_FLOW.md)
