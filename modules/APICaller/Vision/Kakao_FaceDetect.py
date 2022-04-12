import requests
import json
from data.Vision.FaceInfo import Face
from modules.APICaller.APICaller import APICaller

class Kakao_FaceAPI(APICaller):

    def __init__(self, url=None, key=None, targetFile=None, options=None):
        super().__init__(url, key, targetFile, options)


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
                    # coordinate (x, y)
                    x = face_data['x']
                    y = face_data['y']
                    # width, height
                    width = face_data['w']
                    height = face_data['h']
                    # gender
                    male_property = face_data['facial_attributes']['gender']['male']
                    female_property = face_data['facial_attributes']['gender']['female']
                    gender = 'man' if male_property > female_property else 'female'

                    # add Face object to list
                    face = Face(x=x, y=y, width=width, height=height, gender=gender)
                    faceList.append(face)

                # sorting with coordinate.x
                faceList.sort(key=lambda m: m.x)

                return faceList
        except:
            print("[Error] fail to request.")
            return None

        return faceList
