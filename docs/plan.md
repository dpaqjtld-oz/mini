# 프로젝트명: AI 기반 반도체 수출 규제 리스크 분석 에이전트

## 1. 프로젝트 목적
유저가 특정 반도체 부품 수출에 대해 질문하면 RAG 파이프라인을 통해 최신 규제 조항을 찾고,
LLM이 리스크 여부를 판단하여 실시간으로 알려주는 시스템 구축.

**핵심 학습 목표:** LLM/RAG 파이프라인 전체 흐름을 직접 구현하며 AI 서빙 아키텍처 이해

---

## 2. 기술 스택 (확정)
| 구분 | 기술 | 비고 |
|------|------|------|
| Language | Python 3.10 | |
| Backend | FastAPI, Uvicorn | |
| Vector DB | Qdrant | 로컬 파일 모드 |
| 임베딩 모델 | SentenceBERT (`jhgan/ko-sroberta-multitask`) | 768차원 |
| LLM | OpenAI API (gpt-4o-mini) | |
| 스트리밍 | SSE (Server-Sent Events) | |
| Frontend | HTML + JavaScript | 단일 파일, 심플 UI |

---

## 3. MVP 체크리스트

- [x] **Data:** 반도체 규제 데이터를 SentenceBERT로 임베딩하여 Qdrant에 적재 (`ingest.py`)
- [x] **Search:** 질문 벡터와 DB 유사도 검색 테스트 (`search.py`)
- [ ] **Backend:** FastAPI 서버 구축 및 `/query` 엔드포인트 구현 (`api.py`)
- [ ] **LLM & RAG:** 검색 결과를 프롬프트에 주입하여 OpenAI API 호출
- [ ] **Streaming:** SSE로 LLM 응답을 프론트엔드에 실시간 전송
- [ ] **Frontend:** HTML/JS로 채팅 UI 구현

---

## 4. 역할 분담

> 핵심 목표: 둘 다 LLM/RAG 파이프라인을 직접 구현하여 취업 포트폴리오에 활용

### RAG 파이프라인 기준 분리

```
[유저 질문]
     ↓
← 동훈 담당 ──────────────────────────────┐
Qdrant 검색 → 관련 조항 추출 → 프롬프트 완성
                                          ↓
← 팀원 담당 ──────────────────────────────┘
OpenAI API 호출 → SSE 스트리밍 → 프론트엔드
```

| 담당 | 역할 | 상세 작업 |
|------|------|-----------|
| **동훈** | RAG - Retrieval 담당 | ~~데이터 적재~~ (완료), Qdrant 검색 모듈, 프롬프트 템플릿 설계, FastAPI 서버 기본 구조 |
| **팀원** | RAG - Generation 담당 | OpenAI API 연결, SSE 스트리밍 구현, 프론트엔드 HTML/JS |

---

## 5. 마일스톤

| 단계 | 목표 | 담당 | 상태 |
|------|------|------|------|
| 1단계 | 데이터 적재 & 벡터 검색 | 동훈 | ✅ 완료 |
| 2단계 | FastAPI 서버 + 검색 엔드포인트 | 동훈 | 🔲 진행 전 |
| 3단계 | OpenAI API 연결 + RAG 완성 | 팀원 | 🔲 진행 전 |
| 4단계 | SSE 스트리밍 구현 | 팀원 | 🔲 진행 전 |
| 5단계 | 프론트엔드 + 전체 연동 테스트 | 팀원 | 🔲 진행 전 |

---

## 6. 제외 기능 (Out of Scope)
- 복잡한 프론트엔드 UI/UX (간단한 HTML/JS로 대체)
- 유저 회원가입 / 로그인
- 관리자 대시보드
- Docker Compose 배포 (로컬 실행으로 대체)
