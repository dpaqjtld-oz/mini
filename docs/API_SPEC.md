# API_SPEC.md - API 엔드포인트 명세

## 기본 정보
- **Base URL:** `http://localhost:8000`
- **Framework:** FastAPI
- **응답 방식:** SSE (Server-Sent Events)

---

## 엔드포인트 목록

### 1. `GET /`
메인 페이지 (HTML 반환)

| 항목 | 내용 |
|------|------|
| Method | GET |
| URL | `/` |
| 응답 | `index.html` (채팅 UI) |

---

### 2. `POST /query`
유저 질문을 받아 RAG 파이프라인 실행 후 SSE 스트리밍 응답

| 항목 | 내용 |
|------|------|
| Method | POST |
| URL | `/query` |
| Content-Type | `application/json` |
| 응답 타입 | `text/event-stream` (SSE) |

**요청 Body:**
```json
{
  "question": "HBM3 칩을 중국에 수출해도 되나요?"
}
```

**요청 필드:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `question` | string | ✅ | 유저가 입력한 수출 규제 관련 질문 |

**응답 (SSE 스트림):**
```
data: HBM3 칩의 경우

data: , 미국 EAR 규정에 따라

data:  수출이 제한됩니다.

data: [DONE]
```

**응답 필드:**
| 이벤트 | 설명 |
|--------|------|
| `data: {text}` | LLM이 생성한 토큰 (실시간 스트리밍) |
| `data: [DONE]` | 스트리밍 종료 신호 |

**에러 응답:**
```json
{
  "detail": "질문을 입력해주세요."
}
```

---

### 3. `GET /health`
서버 상태 확인

| 항목 | 내용 |
|------|------|
| Method | GET |
| URL | `/health` |

**응답:**
```json
{
  "status": "ok"
}
```

---

## 내부 처리 흐름 (`POST /query`)

```
1. 요청 수신
   └── question 유효성 검사 (빈 문자열 체크)

2. 벡터 변환
   └── SentenceBERT로 question → vector (float[768])

3. Qdrant 검색
   └── 코사인 유사도 Top 3 조항 추출
   └── 각 조항의 title, content 추출

4. 프롬프트 조립
   └── 시스템 프롬프트 + 규제 조항 3개 + 유저 질문 결합

5. OpenAI API 호출
   └── model: gpt-4o-mini
   └── stream: True

6. SSE 스트리밍
   └── 토큰 단위로 data: {token} 전송
   └── 완료 시 data: [DONE] 전송
```

---

## 프론트엔드 연동 방법 (JavaScript)

```javascript
const response = await fetch('/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: userInput })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const text = decoder.decode(value);
  const lines = text.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const token = line.replace('data: ', '');
      if (token === '[DONE]') break;
      // 화면에 토큰 추가
      answerDiv.innerText += token;
    }
  }
}
```
