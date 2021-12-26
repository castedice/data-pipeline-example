# Development Log

## 12/26

### Data Lake

Data Lake는 다양한 소스에서 들어오는 데이터를 저장합니다.

http 요청을 통해 데이터가 전송된다고 가정합니다.

원본 데이터를 그대로 DB에 올리게 되면 성능 문제가 발생할 수 있습니다.

따라서 데이터는 파일의 형식으로 저장하고, 데이터의 경로와 메타 정보만을 NoSQL DB에 저장합니다.

DB에 저장되는 내용은 다음과 같습니다.

1. 데이터 경로
2. 데이터 수집 시점
3. 데이터 저장 시점
4. 데이터가 포함하는 키 값

이번 예시에서는 NoSQL은 MongoDB를 파일 형식은 JSON을 사용합니다.

### Data Source Mock

데이터 소스를 모의 환경으로 만들어서 사용합니다.

해당 모듈은 실제 환경에서는 필요하지 않으므로 도커라이즈하지 않습니다.

Data Lake의 성능 평가를 겸합니다.

성능 평가를 위해 [locust](https://locust.io/)를 사용합니다.

## To do

1. [ ] git hook이나 github action으로 code analyzer 자동화
2. [ ] commit message, pull request message template 작성