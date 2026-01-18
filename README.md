# 삼쩜삼(3o3) 웹 자동화 테스트 과제

**Playwright(Python)**를 사용하여 로그인 하기 전 3가지 시나리오를 자동화하였으며, **GitHub Actions**를 통해 CI/CD 파이프라인 및 리포팅/알림 자동화를 구현했습니다.

---

## 기술 스택 (Tech Stack)

| 구분 | 기술 | 설명 |
|---|---|---|
| **Language** | Python 3.10+ | 주요 개발 언어 |
| **Framework** | Playwright | E2E 테스팅 프레임워크 |
| **Test Runner** | Pytest | 테스트 실행 및 관리 |
| **Reporting** | Allure | 상세한 테스트 결과 리포트 (Screenshot 포함) |
| **Infrastructure** | Docker | 일관된 독립 테스트 환경 제공 |
| **CI/CD** | GitHub Actions | 테스트 실행 - 리포트 배포 - 알림 자동화 파이프라인 |
| **Notification** | Slack | 테스트 결과 실시간 알림 연동 |

---

## 📂 디렉토리 구조 (Directory Structure)

```bash
3o3/
├── .github/workflows/   # CI/CD 설정 (GitHub Actions)
│   └── ci.yml
├── src/
│   ├── page/            # Page Object Model (POM) 구현
│   │   ├── basepage.py  # 공통 페이지 로직
│   │   └── loginpage.py # 로그인 관련 페이지 로직
│   └── util/
│       └── locator.py   # UI 요소 로케이터 관리
├── tests/
│   ├── conftest.py      # Pytest 설정 (브라우저, Hook, 리포트 첨부 등)
│   └── test_3o3.py      # 실제 테스트 시나리오 파일
├── dockerfile           # Docker 환경 구성 파일
├── pytest.ini           # Pytest 실행 옵션 설정
├── requirements.txt     # 의존성 패키지 목록
└── README.md            # 프로젝트 설명서
```

---

## 💻 실행 방법 (How to Run)

**Docker**를 이용한 실행 방법.

### 방법 : Docker로 실행하기

1.  **필수 조건**: Docker Desktop 설치, .env 파일 생성 -> zip 파일 안 env.text 파일에 있는 내용 복붙
2.  **실행 명령어**:
    ```bash
    # 1. Docker 이미지 빌드
    docker build -t 3o3 .

    # 2. 테스트 실행 (결과는 allure-results 폴더에 저장됨)
    docker run --rm -v $(pwd)/allure-results:/app/allure-results 3o3 --> mac
    docker run --rm -v ${pwd}/allure-results:/app/allure-results 3o3 --> windows
    ```


---

##  테스트 시나리오 (Test Scenarios)

### 1. `test_landing`
*   **목적**: 메인 랜딩 페이지가 정상적으로 로드되는지 확인
*   **검증**: '카카오 계정으로 계속하기' 버튼 등의 핵심 요소 노출 여부

### 2. `test_login_scenario` (Positive)
*   **목적**: 정상적인 로그인 페이지 진입 및 UI 요소 확인
*   **과정**: 메인 진입 -> 로그인 진입 -> ID/Pass 입력 폼 확인
*   **검증**: ID, Password, 로그인 버튼, QR 로그인 버튼이 모두 정상 노출되는지 확인

### 3. `test_login_negative` (Negative)
*   **목적**: 잘못된 정보 입력 시 로그인 실패 처리가 올바른지 확인
*   **과정**: 임의의 잘못된 ID/PW 입력 -> 로그인 시도
*   **검증**: "비밀번호가 일치하지 않습니다" 경고 문구(Toast/Msg) 노출 여부

---

## 🔄 CI/CD 파이프라인 (GitHub Actions)

코드가 `main` 브랜치에 푸시되면 자동으로 아래 파이프라인이 실행됩니다.

1.  **Build**: Docker 이미지를 빌드하여 테스트 환경 준비
2.  **Test**: Docker 컨테이너 내부에서 pytest 실행 (Chromium, Firefox, Webkit)
3.  **Reporting**: Allure Report 생성 및 **GitHub Pages**에 배포
4.  **Notification**: 테스트 성공/실패 여부를 **Slack Webhook**으로 전송 --> https://join.slack.com/t/3o3hq/shared_invite/zt-3nlwnam6r-dt6yjOhb61BH0QbXAW2NAQ **slack link**

### 📊 테스트 결과 리포트 확인
*   **URL**: `https://junseoseki.github.io/3o3/`
*   리포트에는 각 테스트 케이스의 성공/실패 여부, 소요 시간, 그리고 **실패 시 스크린샷이 자동 첨부**됩니다.

## 📝 과제 수행 후기 및 개선 포인트
*   **안정성 확보**: `conftest.py`에 `autouse` 픽스처를 사용하여 테스트 간의 독립성을 보장하고, 실패 시 자동 스크린샷 첨부 Hook을 구현하여 디버깅 용이성을 높였습니다.
*   **보안**: 민감한 계정 정보는 `.env` 및 GitHub Secrets로 관리하여 코드에 노출되지 않도록 했습니다.
*   **확장성**: Page Object Model(POM) 패턴을 적용하여, 추후 페이지나 로직이 변경되더라도 유지보수가 쉽도록 설계했습니다.
*   **속도**: 병렬 실행을 통해 test 수행 시간을 단축하였습니다.

## 💡 추가로 고민한 포인트나 개선 아이디어
*   **카카오 로그인**: CI 환경에서의 카카오 로그인은 보안 정책(캡챠봇 등)으로 인해 자동화가 불안정했습니다. 토큰 주입 방식도 고려했으나, 과제용 테스트 계정의 제한적인 환경을 고려하여 로그인 전 단계의 검증에 집중하는 것이 과제의 취지에 더 부합한다고 판단했습니다. 