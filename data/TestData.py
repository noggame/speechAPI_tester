

class TestData:
    def __init__(self) -> None:
        self.id = None
        self.expected = None
        self.stt_kt = None
        self.stt_kakao = None
        self.acc_kt = 0
        self.acc_kakao = 0
        self.winner = None
    
    def __str__(self) -> str:
        expected = f'Expected : {self.expected} (id : {self.id})'
        stt_kt = f'KT : {self.stt_kt} ({self.acc_kt} %)'
        stt_kakao = f'KAKAO : {self.stt_kakao} ({self.acc_kakao} %)'
        winner = f'WIN : {self.winner}'
        return f'{expected}\n{stt_kt}\n{stt_kakao}\n{winner}\n'