# Data Pipeline Example

## Introduction

![Pipeline Structure](./doc/images/readme_pipeline.jpg)

다음과 같은 구조를 가진 Data Pipeline에 대한 예제입니다.

각 컴포넌트는 도커라이즈 되어 있으므로 필요한 부분만 수정하여 사용할 수 있습니다.

## Usage

```bash
make setting
```

## Components

### Data Source Mock

데이터 소스를 모의 환경으로 만들어서 사용합니다.

해당 모듈은 실제 환경에서는 필요하지 않으므로 도커라이즈하지 않습니다.

`Data Lake insert API`의 성능 평가를 위해 사용합니다.

user load testing tool인 [locust](https://locust.io/)를 이용하여 구현하였습니다.

### Data Lake

Data Lake는 다양한 소스에서 들어오는 데이터를 저장합니다.

http 요청을 통해 데이터가 전송된다고 가정합니다.

원본 데이터를 그대로 DB에 올리게 되면 성능 문제가 발생할 수 있습니다.

따라서 데이터는 파일의 형식으로 저장하고, 데이터의 경로와 메타 정보만을 NoSQL DB에 저장합니다.

DB에 저장되는 내용은 다음과 같습니다.

1. 데이터 분류
2. 데이터 수집 시점
3. 데이터가 포함하는 키 값
4. 저장된 데이터 경로
5. 데이터 설명

이번 예시에서는 NoSQL은 MongoDB를 파일 형식은 JSON을 사용합니다.

MongoDB는 웹 기반 인터페이스인 Mongo Express와 함께 사용합니다.

퍼포먼스를 위해 비동기로 처리합니다.

- Web Framework: [FastAPI](https://github.com/tiangolo/fastapi)
- Database Driver: [motor](https://github.com/mongodb/motor)
- File I/O: [aiofiles](https://github.com/Tinche/aiofiles/)