---
title: "Gobi 홈페이지 101: 초보자를 위한 디지털 브레인 구축 가이드"
tags: [Gobi, SDK, Tutorial, PKM, Debugging, Korean]
description: "Gobi 볼트를 프리미엄 인터랙티브 대시보드로 변환하는 방법."
thumbnail: ./Attachments/thumb.jpg
---

# 🎓 Gobi 홈페이지 101: 나만의 디지털 브레인 구축하기

**Gobi Space**의 세계에 오신 것을 환영합니다! [Mickey's Kitchen](https://gobispace.com/@mickeyfromsd)이나 [@jyk](https://gobispace.com/@jyk)와 같이 아름답고 인터랙티브한 볼트를 보고 어떻게 시작해야 할지 궁금하셨다면, 이 가이드가 정답을 제시해 드릴 것입니다.

이 문서는 수많은 디버깅과 개발 과정을 거쳐 정리한, 초보자를 위한 5단계 로드맵입니다.

---

## 🛠️ 1단계: 볼트 초기화

홈페이지를 만들기 전에 먼저 볼트가 필요합니다.

1.  **로컬 폴더 생성**: 맥(Mac)에 폴더를 만듭니다 (예: `Documents/My_Gobi_Vault`).
2.  **Gobi CLI 실행**: 터미널을 열고 다음 명령어를 입력합니다:
    ```bash
    cd [폴더-경로]
    gobi init
    ```
3.  **동기화(Sync)**: 파일들을 클라우드로 동기화하기 시작합니다:
    ```bash
    gobi sync
    ```

---

## 🖼️ 2단계: "홈페이지 스킬" 활성화

Gobi는 기본 파일 리스트 대신 사용자가 직접 만든 HTML 페이지를 홈 화면으로 사용할 수 있게 해줍니다.

1.  **App 폴더 생성**: 볼트 루트(최상위)에 `app/` 폴더를 만듭니다.
2.  **index.html 생성**: `app/index.html` 파일을 만들고 HTML/JS 코드를 넣습니다.
3.  **BRAIN.md 연결**: 볼트 루트의 `BRAIN.md` 파일을 열고(없으면 생성) 다음 설정을 추가합니다:
    ```yaml
    ---
    homepage: ./app/index.html?nav=false
    ---
    ```
    *   `?nav=false`: Gobi의 기본 사이드바를 숨겨 깔끔한 전체 화면을 만듭니다.

---

## 🧩 3단계: Gobi SDK 이해하기

`index.html`은 **Gobi SDK**를 사용하여 볼트와 통신합니다. 가장 핵심적인 함수들은 다음과 같습니다:

- `gobi.listBrainUpdates()`: 최근 게시물과 업데이트 내역을 가져옵니다.
- `gobi.listFiles(path)`: 폴더 구조를 스캔하여 파일 목록을 가져옵니다.
- `gobi.renderMarkdown(content)`: 마크다운(`.md`) 파일을 아름다운 HTML로 변환합니다.
- `gobi.sendMessage(prompt)`: Gobi의 AI 에이전트와 연결하여 채팅 기능을 구현합니다.

---

## 🔍 4단계: 디버깅 마스터클래스 (전문가 팁)

가장 많은 초보자가 막히는 부분입니다. 저희가 개발 과정에서 깨달은 핵심 비법들입니다:

### 1. 샌드박스 감옥 🧱
`index.html`은 `app/` 폴더 안에서 실행됩니다. 보안상 Gobi는 루트 디렉토리(`/`)를 직접 리스트업하는 것을 차단합니다.
*   **해결책**: 부모 폴더는 볼 수 없지만, "옆집"은 부를 수 있습니다! `../Stock`이나 `../Music`과 같은 **상대 경로(Sibling Path)**를 사용하여 콘텐츠에 접근하세요.

### 2. `?nav=false` 파라미터의 역설 🔄
`nav=false`를 적용하면 Gobi 서버가 인식하는 "루트 경로"의 기준이 달라질 수 있습니다.
*   **해결책**: **다중 경로 탐색(Multi-Path Probe)** 전략을 사용하세요. 코드가 여러 경로를 순서대로 시도하게 만드세요:
    1. `../FolderName`
    2. `./FolderName`
    3. `/FolderName`
    *   *하나가 실패하면 데이터가 나올 때까지 다음 경로를 찌르세요!*

### 3. "자가 치유" 볼트 ID 🩹
가끔 SDK가 자신이 어떤 볼트 소속인지 잊어버릴 때가 있습니다 (`undefined` 반환).
*   **해결책**: 브라우저 주소창의 URL(예: `@mickeyfromsd` 부분)에서 직접 ID를 추출하여 요청에 수동으로 주입하세요.

---

## 🎨 5단계: 미학적 완성도 높이기

"@jyk 스타일"이나 "Mickey's Kitchen"과 같은 프리미엄 룩을 위해:

1.  **타이포그래피**: 제목에는 `Playfair Display`, 본문에는 `Montserrat`와 같은 Google Fonts를 사용하여 현대적인 느낌을 줍니다.
2.  **카드 레이아웃**: CSS Flexbox나 Grid를 사용하세요. `transition`과 `box-shadow`를 추가하여 마우스 오버 시 카드가 "튀어나오는" 효과를 줍니다.
3.  **단일 페이지 흐름(One-Page Flow)**: 여러 개의 버튼 대신, 사용자가 한 페이지에서 쭉 내려보며 탐색할 수 있게 구성하세요 (Stock -> Music -> Thoughts).

---

## ✅ 최종 성공 체크리스트

- [ ] `index.html`이 SDK를 기다리나요? (6초 재시도 루프 권장).
- [ ] 파일 경로에 `../` 접두사를 붙여 `app/` 폴더를 탈출했나요?
- [ ] `gobi sync`와 `gobi brain publish`를 실행하여 온라인 반영을 확인했나요?
- [ ] 전문적인 조언이 포함된 경우 **면책 조항(Disclaimer)**을 넣었나요?

> "샌드박스 제약은 벽이 아니라 퍼즐입니다." — *Mickey's Kitchen 개발팀*

---
## 📚 참고 문헌
더 자세한 내용은 내부 기술 로그를 확인하세요:
- `![[Study/Homepage_cli_skill/홈페이지 구축 - 101 gobispace cli v2.md]]`
- `![[Study/Homepage_cli_skill/gobi-homepage-history-en-v2.md]]`

🚀 **즐거운 구축(요리) 되세요!**
