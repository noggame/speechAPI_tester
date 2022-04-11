import requests
import json
from data.Vision.FaceInfo import Face
from modules.APICaller.APICaller import APICaller

class Kakao_FaceAPI(APICaller):
    def __init__(self, url=None, key=None, targetFile=None, options=None):
        super().__init__(url, key, targetFile, options)


# kakaoapi = Kakao_STT(url='https://kakaoi-newtone-openapi.kakao.com/v1/recognize', key=key.kakao['KJH'])
    # def requestVisionAPIFromKakao(target_file=None):
    #     url = "https://dapi.kakao.com/v2/vision/face/detect"
    #     _target_file = target_file
    #     files = {'image':open(_target_file, 'rb')}
    #     header = {
    #         # 'Content-Type': 'multipart/form-data',
    #         # 'Content-Type': 'application/x-www-form-urlencoded',
    #         # 'Content-Type': 'application/octet-stream',
    #         'Authorization': cfg.get('kakao', 'key_sdh') # 'KakaoAK 697f04dd01214c2a532634d6df4d1126'
    #     }

    #     try:
    #         response = requests.post(url=url, headers=header, files=files)

    #         if response.status_code == 200:
    #             return response.text
    #     except:
    #         print(response)

    #     return None

    def request(self, url=None, key=None, targetFile=None, options=None):
        _url = url if url else self.url
        _key = key if key else self.key
        _targetFile = targetFile if targetFile else self.targetFile
        # _options = options if options else self._options


        header = {'Authorization': _key}
        files = {'image':open(_targetFile, 'rb')}

        faceList = []

        try:
            response = requests.post(url=_url, headers=header, files=files)
            if response.status_code == 200:

                # parsing faces
                data = response.text
                data = json.loads(data) if data else None
                faces = data['result']['faces']

                for face_data in faces:
                    # gender
                    male_property = face_data['facial_attributes']['gender']['male']
                    female_property = face_data['facial_attributes']['gender']['female']
                    gender = 'man' if male_property > female_property else 'female'
                    # coordinate (x, y)
                    x = face_data['x']
                    y = face_data['y']

                    # add Face object to list
                    face = Face(x=x, y=y, gender=gender)
                    faceList.append(face)

                # sorting with coordinate.x
                faceList.sort(key=lambda m: m.x)

                return faceList
        except:
            print("[Error] fail to request.")
            return None

        return faceList
