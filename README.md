# Data Pipeline Example

## Introduction

![Pipeline Structure](./doc/images/readme_pipeline.jpg)

다음과 같은 구조를 가진 Data Pipeline에 대한 예제입니다.

각 컴포넌트는 추 후 활용이 용이하도록 마이크로서비스로 구현합니다.

따라서 poetry로 컴포넌트 별 depandancy 관리가 필요합니다.

개발 순서는 로컬에서 개발 및 테스트 후 도커라이즈합니다.

code analyzer를 적극적으로 활용합니다.

1. Code Formatter: [black](https://github.com/python/black)
2. Code Linter: [wemake-python-style](https://github.com/wemake-services/wemake-python-styleguide)
3. Static Type Checker: [mypy](https://github.com/python/mypy) + [monkeytype](https://github.com/Instagram/MonkeyType)

Github action에 적용되기 전까지 수동으로 진행합니다.

사용법

```bash
black .
monkeytype run main.py
mypy .
flake8 .
```
