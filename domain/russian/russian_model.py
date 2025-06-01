class UserRussian:
    def __init__(self, user_num: int, user_russian_time: int = 0, user_russian_cnt: int = 0, user_russian_dead: int = 0):
        self.user_num = user_num
        self.user_russian_time = user_russian_time
        self.user_russian_cnt = user_russian_cnt
        self.user_russian_dead = user_russian_dead

    def to_dict(self) -> dict:
        """UserRussian 객체를 딕셔너리로 변환
        
        Returns:
            dict: UserRussian 객체의 딕셔너리
        """
        return {
            "user_num": self.user_num,
            "user_russian_time": self.user_russian_time,
            "user_russian_cnt": self.user_russian_cnt,
            "user_russian_dead": self.user_russian_dead
        }
    
    @staticmethod
    def from_dict(data: dict) -> "UserRussian":
        """딕셔너리를 UserRussian 객체로 변환
        
        Args:
            data: UserRussian 객체의 딕셔너리
        
        Returns:
            UserRussian: UserRussian 객체
        """
        return UserRussian(
            user_num=data["user_num"],
            user_russian_time=data["user_russian_time"],
            user_russian_cnt=data["user_russian_cnt"],
            user_russian_dead=data["user_russian_dead"]
        )