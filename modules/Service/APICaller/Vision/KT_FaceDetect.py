import json
import requests
import logging
from PIL import Image
from Struct.Vision.FaceInfo import Face
from modules.Service.APICaller.BaseAPICaller import BaseAPICaller

class KT_FaceDatect(BaseAPICaller):
    def __init__(self, url=None, key=None, targetFile=None, options=None) -> None:
        super().__init__(url, key, targetFile, options)
    
    def request(self, url=None, key=None, targetFile=None, options=None):
        _url = url if url else self.url
        _key = key if key else self.key
        _targetFile = targetFile if targetFile else self.targetFile

        headers = options if options else self.options
        files = {'imgFile':open(_targetFile, 'rb')}

        faceList = []

        try:
            response = requests.post(url=_url, headers=headers, files=files)
            im = Image.open(targetFile)

            if response.status_code == 200:
                # parsing faces
                data = response.text
                data = json.loads(data) if data else None
                faces = data['resultList']
                
                img_width, img_height = im.size
                im.close()

                for face_data in faces:
                    
                    # coordinate (x, y)
                    v1, v2, v3, v4 = [(v['x'], v['y']) for v in face_data['rect']['vertices']]
                    # v1-----v2 #
                    # |       | #
                    # |       | #
                    # v4-----v3 #
                    x, y = v1

                    # width, height
                    width = v2[0] - v1[0]
                    height = v4[1] - v1[1]

                    # add Face object to list
                    face:Face = Face(x=x, y=y, width=width, height=height, gender=None)
                    faceList.append(face)

                # sorting with coordinate.x
                faceList.sort(key=lambda f: f.x)
            else:
                logging.warn("[ERROR] bad response. >> {}".format(response))
                
                return faceList

        except Exception as e:
            # logging.warn("[ERROR] bad response. >> {}".format(response))
            print("[Error] fail to request. >> {}".format(e))
            return None
        
        return faceList
