# speechAPI_tester  폴더 생성
# COPY /mnt/d/Workspace/python/speechAPI_tester 
# logs 폴더 생성
EXPOSE 5700

##### package
apt update
apt install libsndfile1
apt install ffmpeg


##### module
python3 -m pip install --upgrade pip
pip install google
pip install google-cloud
pip install google-cloud-vision
pip install requests_toolbelt
pip install pydub
pip install numpy
pip install librosa

