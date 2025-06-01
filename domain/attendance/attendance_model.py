# Import libraries  
from datetime import datetime

class UserAttendance:
    def __init__(self, user_num: int, user_att: datetime = None, user_att_total: int = 0, user_att_stack: int = 0):
        self.user_num = user_num
        self.user_att = user_att if user_att else datetime(2025, 2, 4, 0, 0, 0)
        self.user_att_total = user_att_total
        self.user_att_stack = user_att_stack

    def to_dict(self) -> dict:
        """UserAttendance 객체를 딕셔너리로 변환
        
        Returns:
            dict: UserAttendance 객체의 딕셔너리
        """
        return {
            "user_num": self.user_num,
            "user_att": self.user_att.strftime("%Y-%m-%d %H:%M:%S"),
            "user_att_total": self.user_att_total,
            "user_att_stack": self.user_att_stack
        }
    
    @staticmethod
    def from_dict(data: dict) -> "UserAttendance":
        """딕셔너리를 UserAttendance 객체로 변환
        
        Args:
            data: UserAttendance 객체의 딕셔너리
        
        Returns:
            UserAttendance: UserAttendance 객체
        """
        return UserAttendance(
            user_num=data["user_num"],
            user_att=datetime.strptime(data["user_att"], "%Y-%m-%d %H:%M:%S"),
            user_att_total=data["user_att_total"],
            user_att_stack=data["user_att_stack"]
        )
