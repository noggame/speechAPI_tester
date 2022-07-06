# 환경 설정
- Docker/Docker-compose engine
- Python 3.9.7
- Postgresql



# 실행 절차
1. 소스코드 다운로드

    git clone https://github.com/noggame/speechAPI_tester.git

2. 이미지 생성
Python 테스트 클라이언트 이미지 생성을 위해 "environments/dockerfiles" 경로의 Dockerfile_TestTool 실행

    docker build -t apitest:1.0 -f ./environments/dockerfiles/Dockerfile_TestTool .

- 이미지 생성 후 동작 확인을 위한 TestTool 이미지 개별 실행은 아래 코드 참고

    docker run -it -d --name test_tool -v ${src_path}:/usr/src -v ${data_path}:/usr/src/dataset --network host apitest:1.0 /bin/sh

3. 실행환경 설정
- 클라이언트 환경설정
    - 경로확인 : "config/cfgParser.py" 파일에서 config/prod.config 파일을 환경설정 파일로 사용도록 설정

    ``` Python
    config.read(f'{os.getcwd()}/config/prod.config')
    ```

    - 환경설정
        - postgresql : DB 접속정보 설정
        - system : 생성파일 저장경로 설정
        - vision : Vision API Test 옵션 설정

4. 컨테이너 환경 구축
테스트 클라이언트 구동에 사용되는 환경 구축
- docker-compose 환경설정 : "environments/dockerfiles/config/.env" 편잡/사용
    - POSTGRES_* : postgresql 컨테이너 실행 옵션
    - SERVER_* : 호스트 정보
- docker-compose 실행

    docker-compose --env-file ./environments/dockerfiles/config/.env -f ./environments/dockerfiles/docker-compose.yml up -d

- (DB 정보가 정의되지 않은 경우 초기설정)
    - 'apidata' 데이터베이스 생성
    - "./environments/DB/DB_SCHEME.sql"에 정의된 쿼리 실행
    - datainfo, api, key 테이블에 사용될 정보 미리 등록



# 개발환경 구축
## Python(3.9.7) 테스트 도구 실행환경 구축
- Conda
```
conda config --add conda-forge
conda create -n py397 python=3.9.7 --file requirements_conda.txt
conda install flask
```
- Container
'''
pip install -r ./environments/python/requirements.txt
'''


# Error Handling
## 로그파일에 urllib3 exception 발생하는 경우 (lib 호환 이슈)

'''
apt remove python3-urllib3
pip install urllib3
pip install requests
'''
