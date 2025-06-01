class User:
    def __init__(self, user_num: int, user_id: int, user_guild: int, user_name: str, user_exp: int, user_point: int):
        self.user_num = user_num
        self.user_id = user_id
        self.user_guild = user_guild
        self.user_name = user_name
        self.user_exp = user_exp
        self.user_point = user_point

    def to_dict(self) -> dict:
        """User 객체를 딕셔너리로 변환
        
        Returns:
            dict: User 객체의 딕셔너리

        """
        return {
            "user_num": self.user_num,
            "user_id": self.user_id,
            "user_guild": self.user_guild,
            "user_name": self.user_name,
            "user_exp": self.user_exp,
            "user_point": self.user_point
        }
    
    @staticmethod
    def from_dict(data: dict) -> "User":
        """딕셔너리를 User 객체로 변환
        
        Args:
            data: User 객체의 딕셔너리
        
        Returns:
            User: User 객체

        """
        return User(
            user_num=data["user_num"],
            user_id=data["user_id"],
            user_guild=data["user_guild"],
            user_name=data["user_name"],
            user_exp=data["user_exp"],
            user_point=data["user_point"]
        )