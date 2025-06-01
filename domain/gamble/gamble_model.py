# Import Libraries

from datetime import datetime

class UserGamble:
    def __init__(self, user_num: int, user_gamble_time: int = 0, user_gamble_cnt: int = 0):
        self.user_num = user_num
        self.user_gamble_time = user_gamble_time
        self.user_gamble_cnt = user_gamble_cnt
        
    def to_dict(self) -> dict:
        """UserGamble 객체를 딕셔너리로 변환
        
        Returns:
            dict: UserGamble 객체의 딕셔너리
        """
        return {
            "user_num": self.user_num,
            "user_gamble_time": self.user_gamble_time,
            "user_gamble_cnt": self.user_gamble_cnt
        }
    
    @staticmethod
    def from_dict(data: dict) -> "UserGamble":
        """딕셔너리를 UserGamble 객체로 변환
        
        Args:
            data: UserGamble 객체의 딕셔너리
        
        Returns:
            UserGamble: UserGamble 객체
        """
        return UserGamble(
            user_num=data["user_num"],
            user_gamble_time=data["user_gamble_time"],
            user_gamble_cnt=data["user_gamble_cnt"]
        )
    
    