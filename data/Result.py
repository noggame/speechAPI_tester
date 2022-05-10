from typing import List


class TestResult:
    def __init__(self, id, service, source, expected:list, actual:list) -> None:
        self._id = id
        self._source = source
        self._service = service
        self._expected = expected
        self._actual = actual

        # self._accuracy = accuracy
        # self._categories = categories

    def __str__(self) -> str:
        #####   Format   #####
        # {
        #    "id":"41_0610_819_0_10019_05",
        #    "source":"/mnt/d/Workspace/python/speechAPI_tester/sample/clova_dataset/wavs_train/41_0610_819_0_10019_05.wav",
        #    "service":"KT_STT",
        #    "expected":[
        #       "20명 들어갈 자리 있나요?"
        #    ],
        #    "actual":[
        #       "피곤할 짜리 있나요"
        #    ]
        # }


        result_json = '{'                                   # open json
        result_json += f'"id": "{self.id}"'
        result_json += f', "source": "{self.source}"'
        result_json += f', "service": "{self.service}"'   # publisher
        
        result_json += f', "expected": ['
        expectedList = []
        for exp in self._expected:
            expectedList.append(f'{exp}')
        expectedList = ', '.join(expectedList)
        result_json += f'{expectedList}]'

        result_json += f', "actual": ['
        if self._actual:
            actualList = []
            for act in self._actual:
                actualList.append(f'{act}')
            actualList = ', '.join(actualList)
            result_json += f'{actualList}'
        result_json += ']'


        # result_str += f'[Expected] : {self.expected}'
        # result_str += f'[Actual] : {self.actual}\n'
        # result_str += f'[Accuracy] : {self.accuracy}\n'
        # result_str += f'[Categories] : {self.categories}'

        result_json += '}'                                  # close json
        return result_json
        
    @property
    def id(self):
        return self._id

    @property
    def source(self):
        return self._source

    @property
    def service(self):
        return self._service

    @property
    def expected(self) -> list:
        return self._expected

    @property
    def actual(self) -> list:
        return self._actual

    @id.setter
    def id(self, id):
        self._id = id

    @service.setter
    def service(self, service):
        self._service = service

    @source.setter
    def source(self, source):
        self._source = source

    @expected.setter
    def expected(self, expected:list):
        self._expected = expected

    @actual.setter
    def actual(self, actual:list):
        self._actual = actual


class ResultFlag:

    SKIP = False
    KT = False
    KAKAO = False

    def __init__(self) -> None:
        pass

    def init(self):
        self.SKIP = False
        self.KT = False
        self.KAKAO = False