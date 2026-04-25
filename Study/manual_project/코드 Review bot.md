## 목차 

1. Project Overview  
2. Directory structure  
3. Tech stack  
4. Architecture Diagram  
5. Call Flow  
6. Module Description  
7. Data Struct  
8. Infra and Deployment  
9. Environment  
10. Git ignore  
11. Go reference and Example  

---
## 1. Project overview
매일 정해진 시간에 k8s cronjob 으로 실행되어, snowflake 에 로딩된 git merge request snapshot data 를 조회하고, 열려있는 목록을 Teams/Kakao/Slack/Facebook message 등으로 채널에 전송하는 봇.

---
## 2. Directory Structure
### 디렉토리 구조 
```
root /
 |--- .giignore     
 |--- .gitlab-ci.yml # pipeline 설정
 |--- Dockerfile     # container image 빌드 정의
 |--- README.md
 |--- go.mod         # 의존성 dependency 선언
 |--- go.sum         # checksum 검증
 |--- cmd/
 |    |--- main.go   # app entry point 
 |
 |---internal/reviewbot/
 |    |--- mr.go    # sf DB query and MR data model
 |    |--- teams.go  # webhook message 
 |    |--- teams_test.go
 |    |--- user.go   # loading user and json file
 |
 |--- helm/
      |--- .helmignore # k8s 배포용 Helm chart 
      |--- Chart.yaml  # Helm pkg exception pattern
      |--- values.yaml # static 배포값 (dev 환경) 
      |--- values.yaml.js # CI/CD 용 jinja2 teamplte 값
      |--- templates/
           |----cronjob.yaml # k8s cronjob resource teamplate
```

### Directory 설계원칙 

```
# Go project Standard Layout
# ref: https://github.com/golang-standards/project-layout
# 
# cmd/      - 실행가능한 바이너리 진입점. 각 서브디렉토리가 하나의 바이너리에 대응
# internal/ - 외부 패키지에서 import 할 수 없는 비공개 패키지. 고 컴파일러가 경로 강제 제한
# helm/     - k8s 배포를 위한 Helm 차트 디렉토리
```

---
## 3. Tech Stack

카테고리: 기술/버전/용도  
언어: Go / 1.23.0 / 메인 앱 개발  
DB: Snowflake /- / git snapshot data storage  
메시징: Teams Webhook / Adaptive Card v1.2 / Teams 알림전송   
컨테이너: Docker / - / app 컨테이너화  
오케스트: K8s / - / CronJob 스케줄링  
패키지관리: Helm / V2 (API) / K8s 클러스터 호스팅  
CI/CD: Gitlab / - / 빌드/패키지/배포 자동화  
클라우드: AWS / - / K8s 클러스터 호스팅   
빌드이미지: Alpine Linux / 3.21 / Go 빌드환경
런타임이미지: Wolfi (Chainguard) / - / 프러덕션 컨테이너 베이스 

### 주요 Go 의존성

```go
// go.mod 에서 선언된 직접 의존성
require (
	github.com/joho/godotenv v1.5.1 // .env file env var 
	github.com/cnowflakedb/gosnowflake v1.13.1 // snowflake DB driver
)
// 간접 의존성 중 핵임
// github.com/youmark/pkcs8 - PKCS#8 암호화 키 파싱 (JWT 인증용)
// github.com/golang-jwt/jt/v4 - JWT토큰생성 (snowflake 인증용)
// github.com/aws/aws-sdk-go-v2 - aws s3 접근 (snowflake 내부사용)
```

---

## 4. Architecture Diagram

1. K8s Cluster (AWS)
	1. cronjob: daily
	2. Pod
		1. Container (Go binary)
			1. evnFrom: K8s Secrets
			2. volumeMount: secret_config.json
		2. Snowflake DB (SnapShot)
		3. K8s Secrets (env vars, config)
		4. MS Teams WebHook (Adaptive card message)

---
## 5. Call Flow 
### 전체 실행 흐름
```
K8s CronJob Trigger : Daily UTC14:55 (KST 23:55)

cmd/main.go :: main()

1. dodotenv.Load() 
   : .env file 로드 (로컬 개발용, K8s 에서는 없어도 경고만)
2. os.Getenv() x10
   : 필수 환경변수 10개 검증 (없으면 log.panic)
3. pem.Decode() 
   : pkcs8.ParsePKCS8PrivateKeyRSA() PEM 형식 비공개 키 디코딩
4. codereviewbot.LoadSecretConfigFromFile() -> user.go
   : secret_config.json 파일에서 채널/사용자 정보 로드
5. gosnowflake.Config 생성 -> cfg.Validate() -> DSN 생성
   : JWT 인증방식으로 Snowflake 접속 설정 구성
6. sql.Open ("snowflake" ,dsn) -> db.Ping()
   : Snowflake 데이터베이스 연결 수립 및 연결 확인
7. for_, channel :=range secretConfig.Channels{
    7.a. for _, group:= range channel.GitLabGroups{
		   codereviewbot.GetMergeRequests() --> mr.go
		   : Snowflake 에서 해당 그룹의 코드 조회
		   mps.Copy(allCodes, codes)
		   : 여러 그룹의 결과를 하나의 맵으로 병합
		   } //end group loop
	7.b. codereviewbot.SendMessage() -> teams.go
	: Teams 웹훅으로 Adaptive Card 메시지 전송  
   } // end channel loop
8. 프로세스 종료 (exit 0)
```

### 상세 함수 콜 플로우

```
main() // cmd/main.go
- godotenv.Load() // 외부패키지 .env 파일의 KEY=VALUE 쌍을 OS 환경변수로 로딩.
- os.Getenv("GITLAB_GROUP_FULL_PATH") // 표준 라이브러리 총 10개 변수검증
- pem.Decode([]byte(snowflakePrivateKey)) // encoding/pem 코딩, 디코딩 BEGIN 형식 파싱
- pkcs8.ParsePKCS8PrivateKeyRSA(block, passphrase) // youmark/pkcs8 키추출
- codereviewbot.LoadSecretConfigFromFile(path) //internal/codereviewbot/user.go
  - os.ReadFile(path) // go 표준 os . 파일 전체를 []byte로 읽기, 
  - json.Unmarshal(b,&sc) 
  // go 표준 encoding/json , JSON 바이트를 SecretConfig구조체로 역직렬화
- gosnowflake.Config{...} // 외부 gosnowflake
  - cfg.Validate() // 설정 유효성 검증
  - gosnowflake.DSN(cfg) // Data source Name 문자열 생성
- sql.Open("snowflake", dsn) // go표준,database/sql ,드라이버 초기화
  - db.Ping() // 실제 네트워크 연결 수립 및 확인
- for _, channel:= range secretConfig.Channels // cmd/main.go
	  for _, group := range channel.GitLabGroups // cmd/main.go
		  - codereviewbot.GetMergeRequests (db, query, group)
		    //internal/codeviewbot/mr.go 
		    - db.Query(query, projectFullPath) // database/sql
		      : 파라미터화된 SQL 쿼리
		      : ? 플레이스홀더에 projectFullPath 바인딩
		    - for rows.next() // mr.go
		      - rows.Scan(&project, &mr, Assignee, ...)
		        // 각 행의 컬럼 값을 변수에 매핑
		        // mrs[project]=append(mrs[project], mr)
- maps.Copy(allMrs, mrs) // go 표준 maps (go 11.21+)
- codereviewbot.SendMessage(allMrs ,users, webhookUrl) 
	// internal/codreviewbot/teams.go		    
	- buildTextBlocks(u, mrs) // teams.go
	  - for projectKey, mrsList :=range mrsList
	    - getNameFromGitLabUser(u,assignee) // teams.go 
	    - getUPNFromGitLabUser(u, assignee) // teams.go
	    - getDataFromTimestamp (createdAt) // teams.go RFC3339 date only
	    - getDauysAgo(createdAt) // time.Parse -> time.Since -> hours/24
	    - getReviewers(u, reviewersJSON)
	      - json.Unmarshal(reviewersJSON)
	      - for each reviewer: // [{\"username\":"jdoe\"}] parsing
	        getNameFromGitLabUser()
	        getUPNFromGitLabUser()
- buildEntities(authors) // teams.go, @멘션을 위한 entity json 생성, 중복 UPN 제거
- fmt.Sprintf(msg, textBlocks, entities) // Adaptive Card JSON 템플릿 동적 삽입
- http.Client.Do(req) // go 표준 net/http
  // POST 요청으로 Teams 에 웹훅 전송. Content-Type: application/json
```

### 데이터 흐름도

[snowflake DB] SQL Query (gitlab_mergerequests_snapshot table) --> buildTextBlocks
[secret_config.json] JSON Parse --> buildTextBlocks
[BuildTextBlocks] + [buildEntities] --> Adaptive JSON Message  --> HTTP POST
[MS Teams Webhook]

---
## 6.  Module Description

**역할** : 전체 흐름을 오케스트레이션하는 메인함수
```go
// Go 언어 참고: 패키지와 진입점
// 반드시 package main 의 func main() 에서 시작됨
// cmd/ 디렉토리 아래에 main.go 를 두는것은 Go 프로젝트의 관례임
// 예)
// packge main
// func main(){
//     fmt.Println("Hello World!")
// }

// Go 언어 참고: 환경변수 처리
// os.Getenv("KEY") 는 환경변수를 읽어 string 으로 반환함.
// 변수가 없으면 빈 문자열 "" 을 반환함. 에러가 아님.
// godotenv.Load() 는 .env파일의 내용을 환경 변수로 주입함.
// 로컬 개발시 유용.
// 예)
// val :=os.Getenv("MY_KEY")
// if val=="" {
//     log.Fatal("MY_KEY is required") 
// }
// 
// Go 에러처리 패턴
// log.Fatal(err) // 에러 출력 후 os.Exit(1)
// log.Panic(err) // 에러 출력 후 panic (defer 실행됨)
// 예)
// result, err := someFunction()
// if err !=nil {
//    log.Fatal(err) // 즉시종료 
// }
```

** 주요 처리 단계 **
1. 환경변수 로딩: '.env' 파일 로드 후 10개 필수 환경 변수 검증
2. 비공개키 파싱: PEM -> PKCS#8 -> RSA Private Key
3. 설정 파일 로딩: 'secret_config.json' 에서 채널 사용자 데이터 로드
4. DB 연결:  snowflake JWT 인증으로 데이터 베이스 연결
5.  채널별 처리 루프: 각 채널의 Gitlab그룹별 MR 코드 조회 -> Teams 전송

### 'internal/codereviewbot/mr.go' 데이터 조회 모음

**역할**: snowflake 에서 gitlab 코드 머지 리퀘스트 스냅샷 데이터 조회

```go
// Go 언어 참고: database/sql 패키지
// db.Query(query, args...) // 여러 행 반환
// db.QueryRow(query, args...) // 단일 행 반환 
// db.Exec(query, args...) // sql.Result (INSERT/UPDATE/DELETE)
// 플레이스 홀더로 SQL injection 방지.
// 예)
// rows, err:= db.Query("SELECT name FROM users WHERE id=?",userID)
// defer rows.Close()
// for rows.Next(){
//    var name sgtring
//    rows.Scan(&name)
// }

// Go 언어 참고 : Type Alias
// type MergeRequests map[String][]MergeRequest
// map[sgring][]Megerequst  에 이름을 부여, 가독성 높임.
// 키는 프로젝트 경로 (string) , 값은 해당 프로젝트 목록 (슬라이스)
// 예)
// type UserMap map[string]User
//   users :=make(UserMap)
//   users ["john"] = User{Name:"John"}
```

**SQL 쿼리분석('QueryMergeRequests')

```sql
-- CTE 1: last snapshot only (de-dup)
-- QUALIFY + ROW_NUMBER() 
WITH mrs_distinct_per_day as(
	SELECT *
	FROM gitlab_mergerequests_snapshot
	qualify row_number() over (
		PARTITION BY substr (inserted_timestamp, 0, 10), mergerequest_iid
		ORDER BY inserted_timestamp DESC 
	)=1
)

-- CTE 2: target group MR filtered
, mrs_for_target_groups as (
	SELECT project_fullpath, author_username, mergereqest_title, ...
	FROM mrs_distinct_per_day
	WHERE startswith(lower(project_fullpath), lower(?)) -- param bind
	and inserted_timestamp >= current_date() -- today only
) SELECT * FROM mrs_for_target_gropus
```

---
### 'internal/coderevidewbot/teams.go' - msg module

** 역할: 데이터를 팀즈 카드 형식으로 변환하여 웹훅 전송

```go
// Go 언어 참고: 문자열 템플릿과 fmt.Sprintf
// Go 문자열 포맷팅은 fmt.Sprintf 를 사용함.
// %s ,%d, %f, %v (기본포맷), $+v (필드명 포함)
// 이 코드에서 JSON 문자열 상수 (msg) 에 %s 플레이스 폴더를 두고, 
// fmt.Sprintf(msg, textBlocks, entities) 로 동적 데이터를 삽입.
// 예)
// name :="World"
// greeting :=fmt.Sprintf("Hello , %s! You are #%d.", name,1)
// // 결과: "Hello, World! You are #1."

// Go 언어 참고: HTTP 클라이언트
// net/http 패키지로 HTTP 요청을 생성하고 전송함.
// http.NewRequest(method, url, body) -> *http.Request
// client.Do(req) -> *http.Response, error
//
// 예)
// client :=&http.Client()
// body := strings.NewReader('{"key":"value"}')
// req, _ := http.NewRequest("POST",url,body)
// req.Header.Add("Content-Type","application/json")
// resp, _ := client.Do(req)
// defer resp.Body.Close()

// Go 언어 참고: 시간처리
// time.Parse(layout, value)로 문자열을 시간으로 변환
// 고유한 레이아웃 문자열을 사용함. "2016-01-02T15:04:05Z07:00" (RFC3339)
// 이 레이아웃은 Go 의 탄생 시간(2006 1월 2일 15:04:05) 기반
// time.Since(t) 는 현재까지의 duration 반환
// t, _:= time.Parse(time.RFC3339, "2026-01-14:T10:30:00Z")
// elapsed :=time.Since(t)
// days :=int(elapsed.Hours()/24)
```

**핵심함수들:
함수
'SendMessage()'
'bildTextBlocks()'
'buildEntities()'
'getNameFromGitLabUser()'
'getUPNFromGitLabUser()'
'getDateFromTimestamp()'
'getDaysAgo()'
'getReviewers()'

---
## 7. Data Struct

```go
// internal/codreviewbot/user.go 
type SecretConfig struct{
	Channels []ChannelData `json:"channels"`
	Users []UserData `json:"users"`
}
type ChannelData struct{
	GitLabGroups []String `json:"gitlabGroups"`
	MSTreamsWebhook string `json:"mstreamsWebhook"`
}
type UserData struct{
	Name string `json:"name"`
	GitlabUser string `json:"gitlabUser"`
	UPN string `json:"upn"`
}


// internal/codereviewbot/mr.go
type MergeRequest struct{
	Assignee string // coder id
	Title string // code ref subject
	Iid string // code internal ID 
	CreatedAt string 
	UpdatedAt string
	State string
	Reviewers string 
}

type MrgeRequest map[string][]MergeRequest
```

### 'secret_config.json' example

```json
{
	"channels":[
	{
	 "gitlabGrups":["corp/dev", "corp/crm"], 
	 "msteamsWebhook":"https://outlook.webhook.office.com/webhook2/..."
``	},
	{
	 "gitlabGrups":["corp/pm", "corp/qa"], 
	 "msteamsWebhook":"https://outlook.webhook.office.com/webhook2/..."
	}
	],
	"users:"[
	{
	 "name":"John Doe",
	 "gitlabUser":"jdoe",
	 "upn":"john.doe@corp.com"
	}
	]
}
```

## 8. Infra and Deployment

CI/CD pipeline (.gitlab-ci.yml)

common check -> build (go) -> package (docker)-> test -> deoploy (K8s)
-> dev branch or prd branch 

### docker build
```dockerfile
# Wolfi base image (Chainguard 사의 보안 강화 이미지)
FROM  registry.gitlab.comm/.../wolfi-base/crop-main:latest
WORKDIR /app
COPY --chown=65532:65532 bin/app app # UID 65532 non SU
ENTRYPOINT ["app/app"]
```

**Ref: CI 의 빌드 스테이지에서 'go build' 로 미리 컴파일한 bin/app 을 DockerFile 에서 COPY
> 멀티 스테이지 빌드가 아닌 CI artifact 를 사용하는 방식

### K8s CronJob

```yaml
# helm/templates/cronjob.yaml 핵심 설정 
apiVersion:batch/v1
kind: CronJob
sepc:
	Schedule "55 14 * * *" # daily UTC 14:55 (KST 23:55)
	concurrencyPoicy: Replace
	failedJobsHistoryLimit: 5
	successfulJobsHistoryLimit: 5
	jobTemplate:
		spc:
			containers:
				-envFrom: # k8s secret env 
					- secretRef: corp.default.credentials
					- secretRef: code-review-bot
				volumeoounts: # secret_config.json file mount
					- mountPath: /etc/code_reveiw_bot
			volumes:
				-secret: #k8s secret into file mount
					secretName: code-reveiw-bot
					items:
						- key: secret_config.json
						  path: secret_config.json
```

## 9. Environment

GITLAB_GROUP_FULL_PATH
MS_TEAMS_WEBHOOK_URL
SNOWFLAKE_WAREHOUSE
SNOWFLAKE_DATABASE
SNOWFLAKE_SCHEMA
SNOWFLAKE_ROLE
SNOWFLAKE_USER
SNOWFLAKE_PRIAVTE_KEY
SNOWFLAKE_PRIVATE_KEY_PASSPHRASE
SECRET_CONFIG_PATH

## 10.gitignore

.env
.cache_ggshield
user_map.txt  # this is python remants, currently it is secret_config.json's users
test.sh # dev test script
examples
users.json
secret_config.json

## 11. Go reference  and Example 

```go
// pattern 1. maps 패키지 (Go 1.21+)
// maps.Copy(dst, src) 는 src 의 모든 키/값 쌍을 dst 에 복사함.
// 기존에 dst 에 동일한 키가 있으면 덮어씌움.
// 예)
// import "maps"
// allMrs := make(map[string][]MergeRequest)
// maps.Copy(allMrs, newMrs)

// pattern 2. slice append
// append(slice, elements...) 는 슬라이스 끝에 요소를 추가한 새로운 슬라이스를 반환함.
// 용량이 부족하면 자동으로 재할당함.
// 예)
// mrs[project] = append(mrs[project], mr)

// pattern 3. make() 로 맵/슬라이스 초기화
// 초기 용량을 지정하거나 바로 사용할 수 있도록 초기화함.
// 예)
// m := make(map[string]int)
// s := make([]string, 0, 10) // 길이 0, 용량 10

// pattern 4. range loop
// for-range 는 슬라이스(index, value), 맵(key, value), 채널(value) 등을 순회함.
// 예)
// for project, mrList := range mrs { ... }

// pattern 5. 포인터와 구조체
// 구조체를 함수에 전달할 때 복사를 피하거나 상태를 변경하기 위해 포인터를 사용함.
// 예)
// func updateMR(mr *MergeRequest) { mr.State = "merged" }

// pattern 6. internal 패키지 접근 제어
// internal/ 디렉토리 내의 패키지는 해당 부모 디렉토리의 하위 패키지에서만 import 가능.
// 외부 프로젝트에서는 이 코드를 사용할 수 없음 (캡슐화).

// pattern 7. strings.Join 과 문자열
// 슬라이스의 문자열들을 구분자로 합칠 때 효율적임.
// 예)
// res := strings.Join([]string{"a", "b", "c"}, ", ") // "a, b, c"

// pattern 8. raw string literal
// 백틱(`)을 사용하여 여러 줄 문자열이나 이스케이프가 필요 없는 문자열을 정의함.
// JSON 이나 SQL 쿼리에 매우 유용함.
// 예)
// query := `SELECT * FROM table WHERE id = ?`

// test example (teams_test.go)
// go test ./internal/reviewbot/... 로 실행
// func TestSendMessage(t *testing.T) {
//     // mock data 생성 후 SendMessage 호출 및 에러 검증
// }

```