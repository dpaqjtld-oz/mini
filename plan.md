# 🚀 프로젝트명: [AI 기반 반도체 수출 규제 리스크 분석 에이전트]

## 1. 프로젝트 목적 (Objective)
단순한 텍스트 검색을 넘어, 유저가 특정 반도체 부품 수출에 대해 질문하면 RAG 파이프라인을 통해 최신 규제 조항을 찾고 LLM이 리스크 여부를 판단하여 실시간으로 알려주는 시스템을 구축한다. (전체 AI 서빙 파이프라인의 병목 해결 및 흐름 이해에 집중)

## 2. 핵심 목표 및 MVP (Minimum Viable Product)
- [ ] **Data:** KOTRA 뉴스 및 수출 통제 리스트 텍스트 데이터를 SentenceBERT로 임베딩하여 Vector DB에 적재한다.
- [ ] **Backend:** FastAPI를 이용하여 빠르고 안정적인 API 서버를 구축한다.
- [ ] **LLM & RAG:** 유저의 질문과 가장 유사한 규제 데이터를 Vector DB에서 찾아 프롬프트에 주입하고 LLM의 답변을 받아온다.
- [ ] **UX (스트리밍):** 응답 지연(Latency)을 줄이기 위해 LLM의 답변 과정을 SSE(Server-Sent Events)로 프론트엔드에 실시간 스트리밍한다.

## 3. 기술 스택 (Tech Stack)
- **Language:** Python 3.10
- **Backend:** FastAPI, Uvicorn
- **Vector DB:** [Milvus 또는 Qdrant 중 선택]
- **AI Models:** SentenceBERT (임베딩용), [OpenAI API 또는 로컬 vLLM 중 선택]
- **Infrastructure:** Docker Compose (로컬 환경 격리용)

## 4. 제외할 기능 (Out of Scope)
*본 프로젝트의 핵심 아키텍처 학습에 방해되는 요소는 과감히 제외한다.*
- 복잡한 프론트엔드 UI/UX (간단한 HTML/JS 화면으로 대체)
- 유저 회원가입 / 로그인 시스템
- 관리자(Admin) 대시보드 페이지

## 5. 1차 마일스톤 역할 분담
- **동훈:** [담당할 역할 작성 - 예: Data 파이프라인 및 Vector DB 구축]
- **팀원:** [담당할 역할 작성 - 예: FastAPI 세팅 및 스트리밍 로직 구현]