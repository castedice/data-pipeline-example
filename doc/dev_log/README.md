# Development Log

## 12/26

### 사전 준비

각 컴포넌트는 추 후 활용이 용이하도록 마이크로서비스로 구현

따라서 poetry로 컴포넌트 별 depandancy 관리가 필요

로컬에서 개발 및 테스트 후 도커라이즈

code analyzer를 적극적으로 활용

1. Code Formatter: [black](https://github.com/python/black)
2. Code Linter: [wemake-python-style](https://github.com/wemake-services/wemake-python-styleguide)
3. Static Type Checker: [mypy](https://github.com/python/mypy) + [monkeytype](https://github.com/Instagram/MonkeyType)

Github action에 적용되기 전까지 수동으로 진행

```bash
black .
monkeytype run main.py
mypy .
flake8 .
```

### mongodb

docker-compose.yml 작성

[참고 1 - mongodb](https://hub.docker.com/_/mongo)

[참고 2 - dockerhub](https://woolbro.tistory.com/90)

[참고 3 - mongo express 포함](https://gist.github.com/adamelliotfields/cd49f056deab05250876286d7657dc4b)

[참고 4 - .env 파일 경로 설정](https://docs.docker.com/compose/environment-variables/): 개발, 배포, 테스트용 env 파일이 다를 때 사용 가능

### api

[참고 1 - logging](https://velog.io/@otzslayer/파이썬-로깅-멋지게-하기)

api에 로깅까지 추가하여 구현 완료

### 느낀점

별 생각 없이 맨 앞 부분의 모듈인 `data_source_mock` branch를 만들었는데, API가 없으면 테스트가 어려움을 깨달음

결국 `data_source_mock` branch에서 data lake insert api와 data lake db까지 구현

개발 전에 계획을 잘 세우는 것이 중요하다는 것을 다시 한 번 깨달음

## 12/27

### 모듈화 진행

logging 모듈과 router를 모듈화

## 01/02

### branch 이름 변경

`data_source_mock` branch의 개발 내용이 매칭이 안되므로
`data_lake_insert` branch로 이름을 변경

### 속도 향상 관련

[참고 1 - gunicorn with uvicorn!?](https://facerain.club/fastapi-nginx/)

`gunicorn` 설치 후 정상 작동 확인

`nginx`는 필요한 경우에 추 후 추가

### 도커라이즈

[참고 1 - poetry로 배포하기](https://medium.com/@harpalsahota/dockerizing-python-poetry-applications-1aa3acb76287)

[참고 2 - fastapi 도커라이즈](https://malwareanalysis.tistory.com/139)

### locust

구현 완료

현재는 `MongoDb`, `DATA_LAKE_INSERT`, `DATA_SOURCE_MOCK`이 모두 하나의 머신에서 작동하여 제대로 테스트할 수 없었지만, RPS가 6개 정도까지는 충분했음

### makefile

makefile 작성

setting: 테스트 환경 설정
clean: 테스트 시 발생하는 용량이 큰 데이터 삭제
build: 새롭게 빌드 후 컴포즈 업
analysis: black, mypy, flake8 자동 검사

### etl

ETL은 어떻게 만드는 것이 좋을지 고민이 됨

cli로 사용자에게 자율성과 적응에 대한 시간을 요구하는 것이 좋을지

누구나 쉽게 사용할 수 있도록 하는 것이 좋을지 고민이 필요함

### smb file server

payload를 저장할 파일 서버를 독립적으로 구성하는 것이 좋을 것 같다는 생각이 들어 smb file server 컨테이너를 띄울 docker-compose 파일을 작성

다시 생각해본 결과 데이터 스토리지를 할 머신에서 data lake insert가 돌면 해결될 것이라 생각되어 해당 부분은 주석 처리

## 01/07

### plotly dash

etl은 일단 사용자의 편의성을 증대하는 방향으로 구현하기로 함

프론트엔드 구현을 진행해본 적이 없어서 python으로 구현할 수 있는 방법을 선택하였음

pyqt는 이전에 잠시 스터디를 진행하였다가 다시 사용할 일이 없을 것이라 생각하여 스터디를 중단하였고, 이번에도 사용하지 않음

그 외에 pysimplegui나 dearpygui 등도 pyqt와 같은 이유로 활용성이 떨어질 것으로 생각하여 사용하지 않음

그래서 data visualization 도구로도 사용되고 있는 plotly dash를 이용하여 구현하기로 함

확실히 data와 관련되어서는 개발이 편리한 점은 있지만 아직 커뮤니티 파워가 약해서 문제상황 해결이 쉽지 않음

datatable에서 selected_row 부분은 초기화를 해주어야지만 에러가 나지 않는데, 이 부분 원인을 찾는 것이 어려웠음

## 01/08

### plotly dash

어느정도 구현은 완료하였지만, 데이터 테이블을 필터링 한 뒤에 전체를 선택하는 버튼이 원하는대로 작동하지 않음

이슈 사항을 기록해두고 추 후 개선하거나 plotly dash를 포기하는 것이 나을 수도 있을 것 같음

kibana에 대해서 검색이 더 필요함

일단은 진행은 가능하니 여기까지 구현하고 뒷 부분 구현을 진행

데이터를 어떻게 가져올지 고민이 됐는데, 데이터를 불러오는 api를 구현해두고 etl 앱에서 해당 코드를 끌어가는 방법으로 구현하는 것이 좋을 것 같음

## To do

1. [ ] (12/26) git hook이나 github action으로 code analyzer 자동화
2. [ ] (12/26) commit message, pull request message template 작성
3. [ ] (12/27) nfs에 데이터 저장하는 방법 고민
4. [ ] (12/27) authorization 어떻게 할지 고민
5. [ ] (1/2) ngix 추가
6. [ ] (1/6) kafka 추가
7. [ ] (1/6) 분산처리를 위한 zookeeper, log 수집을 위한 logbeat, logstash, elasticsearch, kibana 추가
8. [ ] (1/8) plotly dash 데이터 선택 기능 개선 필요, kibana가 대안이 될 수도?