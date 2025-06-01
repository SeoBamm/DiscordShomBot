# Import Libraries

from datetime import datetime

class UserSubsidy:
    def __init__(self, user_num: int, user_subsidy_time: int = 0, user_subsidy_cnt: int = 0):
        self.user_num = user_num
        self.user_subsidy_time = user_subsidy_time
        self.user_subsidy_cnt = user_subsidy_cnt

    def to_dict(self) -> dict:
        """UserSubsidy 객체를 딕셔너리로 변환
        
        Returns:
            dict: UserSubsidy 객체의 딕셔너리
        
        """
        return {
            "user_num": self.user_num,
            "user_subsidy_time": self.user_subsidy_time,
            "user_subsidy_cnt": self.user_subsidy_cnt
        }
    
    @staticmethod
    def from_dict(data: dict) -> "UserSubsidy":
        """딕셔너리를 UserSubsidy 객체로 변환
        
        Args:
            data: UserSubsidy 객체의 딕셔너리
        
        Returns:
            UserSubsidy: UserSubsidy 객체
        
        """
        return UserSubsidy(
            user_num=data["user_num"],
            user_subsidy_time=data["user_subsidy_time"],
            user_subsidy_cnt=data["user_subsidy_cnt"]
        )