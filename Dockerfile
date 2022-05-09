# speechAPI_tester  폴더 생성
# COPY /mnt/d/Workspace/python/speechAPI_tester 
# logs 폴더 생성
FROM python:3.8.13
EXPOSE 9090

##### Install
# package
RUN apt update
RUN apt install -y libsndfile1
RUN apt install -y ffmpeg
# python modules
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install flask
RUN python3 -m pip install pillow waitress
RUN python3 -m pip install google google-cloud google-cloud-vision
RUN python3 -m pip install requests_toolbelt pydub numpy librosa

#WORKDIR /usr/src
#CMD ["python3", "main_restapi.py"]


# docker run -it --name test_python -v /mnt/d/workspace/python/speechAPI_tester:/usr/src -p 9090:9090 stt_api:1.0 /bin/bash