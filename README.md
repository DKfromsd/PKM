
# 1. My PKM  via Obsidian 준비 
	https://obsidian.md

# 2. Gemini CLI

brew install gemini-cli , 0.17.1

## 3. Claude CLI 설치 

curl -fsSL https://claude.ai/install.sh | bash. , 2.0.55

- curl: 서버에서 데이터를 다운로드하거나 업로드할 때 사용하는 도구입니다. 여기서는 설치 스크립트 파일을 가져오는 역할을 합니다.
- -f (fail): 서버 오류가 발생하면 아무것도 출력하지 않고 조용히 실패하게 합니다.
- -s (silent): 진행 바나 에러 메시지를 숨깁니다 (조용히 실행).
- -S (show-error): -s와 함께 쓰이며, 정말 심각한 에러가 났을 때만 메시지를 보여줍니다.
- -L (location): 웹 주소가 바뀌어 있으면(리다이렉트) 새 주소로 자동으로 따라가서 데이터를 가져옵니다.
- https://claude.ai/install.sh: Claude 설치 코드가 담긴 파일의 인터넷 주소입니다.    
- | (Pipe): 앞의 결과를 뒤로 넘겨준다는 뜻입니다. 즉, curl로 다운로드한 텍스트 내용을 바로 다음 명령어로 전달합니다.

## 4. Open AI Codex 

npm i -g @openai/codex , 0.63.0

## 5. PATH 업데이트 명령어 

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

이 명령어는 "컴퓨터에게 claude라는 프로그램이 어디 있는지 알려주는 작업"입니다. 

- echo '...': 따옴표 안의 문장을 그대로 출력하라는 뜻입니다.
- export PATH=...: 시스템의 '경로(PATH) 목록'에 특정 폴더를 추가하겠다는 설정 문구입니다.
- $HOME/.local/bin: Claude가 설치된 실제 폴더 위치입니다. ($HOME은 내 사용자 계정 폴더를 의미합니다.)
- :$PATH: 기존에 이미 설정되어 있던 다른 경로들도 유지하라는 뜻입니다. (이걸 안 쓰면 다른 명령어들이 안 돌아갈 수 있습니다.)
- >>: 출력된 문장을 파일의 맨 마지막 줄에 덧붙이라는 기호입니다.
- ~/.zshrc: 맥 터미널(zsh)이 켜질 때마다 읽어들이는 설정 파일입니다. 여기에 저장해둬야 터미널을 껐다 켜도 claude 명령어를 기억합니다
## 6. Automation

### 1단계: 기존 구글 드라이브 데이터를 Markdown(.md)으로 변환

Obsidian은 Markdown 기반이므로 기존 Docs와 Slides를 변환해야 합니다.

1. Google Docs/Slides 내보내기:   
- Google Takeout을 사용하여 전체 데이터를 다운로드하거나, 'Google Drive to Obsidian' 같은 서드파티 툴(예: rclone 또는 오픈소스 변환 스크립트)을 사용하여 .md 파일로 변환합니다.
- Slides의 경우: 이미지와 텍스트가 섞여 있으므로, PDF로 변환 후 AI(Claude/Gemini)에게 "이 PDF를 Obsidian용 Markdown 구조로 요약해줘"라고 요청하는 것이 구조화에 유리합니다.
### 2단계: 로컬 Obsidian Vault 및 GitHub 연동 설정

로컬 PC(Mac/Win)에서 파일이 생성되면 자동으로 GitHub에 올라가는 구조를 만듭니다.

1. Obsidian 설치 및 Vault 생성: 로컬 폴더를 하나 지정합니다.
2. Git 연동:
- 해당 폴더에서 git init을 실행하고 GitHub의 Public/Private 저장소와 연결합니다.
- 자동화: Obsidian 플러그인 중 **"Obsidian Git"**을 설치합니다. 이 플러그인은 일정 시간마다 또는 앱 종료 시 자동으로 add, commit, push를 수행해 줍니다.

	Obsidian Git 플러그인 설치 순서

1. **Obsidian 설정 열기:** 왼쪽 하단 톱니바퀴 아이콘(`Settings`)을 클릭.
2. **커뮤니티 플러그인 이동:** 왼쪽 메뉴에서 `Community plugins`를 선택.
3. **제한 모드 해제:** 만약 `Restricted mode`가 켜져 있다면 `Turn on community plugins`
4. **검색 및 설치:** `Browse` 버튼 **"Git"**을 입력 (공식 명칭: **Obsidian Git**, 개발자:) 
5. **활성화:** `Install`을 누른 후, 바로 나타나는 `Enable` 버튼까지 눌러야 작동

### 3단계: AI 및 음성 입력을 통한 자동 문서 생성 (STT & File Processing)

현재 보유하신 Claude, Gemini, Codex를 활용하여 자동화 파이프라인을 구축합니다.

1. STT 및 요약 자동화 (Voice Mode)
- OpenAI Whisper (로컬 설치 권장): Mac/Windows에서 녹음된 파일을 Whisper를 통해 텍스트로 변환하는 간단한 Python 스크립트를 작성합니다.
- AI 정제: 변환된 텍스트를 Claude나 Gemini API에 보내 "이 내용을 Obsidian 양식(헤더, 태그 포함)으로 정리해줘"라고 요청한 뒤, 결과를 Vault 폴더에 .md로 저장하게 합니다.

2. docx, txt 첨부 자동화:
- 특정 'Inbox' 폴더에 파일을 넣으면, Python 스크립트(또는 Zapier/Make 같은 툴)가 이를 감지하여 내용을 읽고 AI를 통해 Markdown으로 변환하여 Obsidian 본진으로 옮기도록 구성합니다.

### 4단계: 디바이스 간 동기화 및 자동 Push 전략

Mac과 Windows 양쪽에서 작업하므로 충돌을 방지해야 합니다.

1. 작업 순서:
- 입력: 음성 녹음 또는 문서 투고 → 처리기: 로컬 스크립트(Gemini/Codex 활용)가 .md 파일 생성 → 저장: Obsidian Vault 폴더.
- 동기화: Obsidian Git 플러그인이 5~10분 간격으로 GitHub에 자동으로 Push.
- 다른 PC에서: 작업 시작 전 git pull을 통해 최신 상태 유지 (이 역시 플러그인이 자동으로 수행 가능).    

### 추천 도구 및 기술 스택 요약

- 언어: Python (파일 감시 및 AI API 호출용)
- AI 도구:
- Claude/Gemini: 문서 요약 및 구조화.
- Codex: 자동화 스크립트 작성 및 수정 시 활용
- STT: Whisper (로컬 실행 시 개인정보 보호에 유리).
- Obsidian 플러그인: Obsidian Git, Templater(문서 양식 자동화).

### 실행을 위한 첫걸음 제언

먼저 Obsidian Git 플러그인을 설정하여 "로컬 파일 수정 → GitHub 반영"
Python으로 "특정 폴더에 txt를 넣으면 제목과 내용을 추출해 md로 바꾸는" 간단한 스크립트  
### 1. 가장 추천하는 방식: Obsidian Digital Garden (난이도: 하)
Obsidian 내에서 특정 노드만 선택해서 내 도메인으로 바로 쏘아 올릴 수 있는 가장 쉬운 방법입니다.
- 비용: 0원 (Vercel 호스팅 사용)
- 특징: 노트를 작성 상단에 dg-publish: true라는 문구만 넣으면 실시간으로 내 도메인 사이트에 업데이트.
- 설정 순서:
1. Obsidian 커뮤니티 플러그인에서 "Digital Garden" 설치.
2. GitHub 계정 연결 및 Vercel(무료 호스팅 서비스) 계정 생성.
3. Vercel 설정에서 본인의 **개인 도메인(DNS)**을 추가 (CNAME 레코드 설정).
4. 플러그인 설정 창에서 'Publish' 버튼을 누르면 끝.

### 2. 더 예쁘고 강력한 방식: Quartz 4.0 (난이도: 중)

현재 Obsidian 커뮤니티에서 가장 인기 있는 오픈소스 퍼블리싱 도구입니다. 백그라운드에서 GitHub Actions가 돌아가며 자동으로 사이트를 빌드합니다.

- 비용: 0원 (GitHub Pages 사용)
- 특징: Obsidian의 거의 모든 기능(그래프 뷰, 백링크, 다크모드 등)을 웹에서 완벽하게 지원합니다.
- 설정 순서:

1. [Quartz 저장소](https://github.com/jackyzha0/quartz)를 Fork 합니다. 
2. 본인의 Obsidian Vault 내용물을 Quartz 폴더로 복사합니다.
3. GitHub Repository 설정(Settings > Pages)에서 본인의 개인 도메인을 입력합니다.
4. 도메인 관리소(DNS)에서 GitHub Pages의 IP 주소(A 레코드)나 도메인 주소(CNAME)를 연결합니다.

---

### 3. DNS 설정 시 주의사항 (공통)

도메인 관리 페이지(예: 가비아, 후이즈, Cloudflare 등)에서 다음과 같이 레코드를 추가해야 합니다.

|   |   |   |   |
|---|---|---|---|
|타입|이름(Host)|값(Value)|설명|
|CNAME|www 또는 notes|사용자명.github.io|GitHub Pages 연결 시|
|CNAME|@ 또는 www|cname.vercel-dns.com|Vercel(Digital Garden) 사용 시|
