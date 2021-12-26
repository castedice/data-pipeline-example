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

### 느낀점

별 생각 없이 맨 앞 부분의 모듈인 `data_source_mock` branch를 만들었는데, API가 없으면 테스트가 어려움을 깨달음

결국 `data_source_mock` branch에서 data lake insert api와 data lake db까지 구현

개발 전에 계획을 잘 세우는 것이 중요하다는 것을 다시 한 번 깨달음



## To do

1. [ ] git hook이나 github action으로 code analyzer 자동화
2. [ ] commit message, pull request message template 작성