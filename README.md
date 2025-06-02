# Discord Bot - ShomBot

### 1. 프로젝트 개요
<br> 설명: <br>
- 디스코드 서버 내 사용자 간 상호작용 촉진

- 출석 체크, 도박 게임(슬롯머신/러시안 룰렛), 낚시 시스템 등 다양한 오락 기능 제공

- 사용자 프로필 관리 및 경제 시스템(보조금 지급)을 통한 지속적인 참여 유도

- Azure 클라우드 기반 시스템 통합

- Azure VM을 활용한 24/7 봇 운영 환경 구축

- Application Insights와 OpenCensus 연동으로 실시간 로그 모니터링 및 성능 분석

- MySQL 데이터베이스 연계 기능 최적화

- 사용자 데이터(프로필, 재화, 출석 정보)의 체계적 관리

- 클라우드 환경에 최적화된 쿼리 처리 및 트랜잭션 안정성 보장<br><br><br>


- 사용한 클라우드 기술: Microsoft Azure VM, Application Insights
<br><br><br>

### 2. 사전 요구 사항
<br>
- Python 3.10.11 <br><br>
- MySQL 8.0 <br><br>
- 사용 가능한 Microsoft Azure 계정 <br><br>

<br><br><br>
### 3. 설치 및 실행 방법
<br>
1. 프로젝트 클론 <br>>> git clone https://github.com/SeoBamm/DiscordShomBot <br><br>
2. 의존성 설치 <br>>> pip install py-cord opencensus-ext-azure python-dotenv mysql-connector-python <br><br>
3. initializeDB 디렉토리 내의 csv 파일을 MySQL seobot_db 스키마에 import <br><br>
4. ShomBotApplication.py 실행<br>>> python ShomBotApplication.py
