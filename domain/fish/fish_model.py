# Import Libraries

from datetime import datetime

class UserFish:
    def __init__(self, user_num: int, user_fish_time: int = 0, user_fish_cnt: int = 0, user_fish_success: int = 0, user_fish_great: int = 0, user_fish_boots: int = 0, user_fish_blow: int = 0, user_fish_now: int = 0):
        self.user_num = user_num
        self.user_fish_time = user_fish_time
        self.user_fish_cnt = user_fish_cnt
        self.user_fish_success = user_fish_success
        self.user_fish_great = user_fish_great
        self.user_fish_boots = user_fish_boots
        self.user_fish_blow = user_fish_blow
        self.user_fish_now = user_fish_now

    def to_dict(self) -> dict:
        """UserFish 객체를 딕셔너리로 변환
        
        Returns:
            dict: UserFish 객체의 딕셔너리
        """
        return {
            "user_num": self.user_num,
            "user_fish_time": self.user_fish_time,
            "user_fish_cnt": self.user_fish_cnt,
            "user_fish_success": self.user_fish_success,
            "user_fish_great": self.user_fish_great,
            "user_fish_boots": self.user_fish_boots,
            "user_fish_blow": self.user_fish_blow,
            "user_fish_now": self.user_fish_now
        }
    
    @staticmethod
    def from_dict(data: dict) -> "UserFish":
        """딕셔너리를 UserFish 객체로 변환
        
        Args:
            data: UserFish 객체의 딕셔너리
        
        Returns:
            UserFish: UserFish 객체
        """
        return UserFish(
            user_num=data["user_num"],
            user_fish_time=data["user_fish_time"],
            user_fish_cnt=data["user_fish_cnt"],
            user_fish_success=data["user_fish_success"],
            user_fish_great=data["user_fish_great"],
            user_fish_boots=data["user_fish_boots"],
            user_fish_blow=data["user_fish_blow"],
            user_fish_now=data["user_fish_now"]
        )