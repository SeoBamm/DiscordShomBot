# Import Custom Modules
from domain.user.user_repository import UserRepository
from domain.user.user_model import User

class UserService:
    """UserService 클래스"""

    def __init__(self):
        self.userRepository = UserRepository()

    def getUserCount(self) -> int:
        """전체 유저 수 반환
        
        Returns:
            int: 전체 유저 수
        
        """
        return self.userRepository.getUserLength()

    def isUserExist(self, userId: int, guildId: int) -> bool:
        """유저 존재 여부 확인
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            
        Returns:
            bool: 유저 존재 여부
        
        """
        return self.userRepository.userExists(userId, guildId)

    async def addUser(self, userId: int, guildId: int, userName: str) -> int:
        """유저 추가
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            userName: 유저 이름
            
        Returns:
            int: 성공 코드(1: 성공, 2: 실패, 3: 이미 존재)
        
        """
        return await self.userRepository.addUser(userId, guildId, userName)

    def getUserInfo(self, userId: int, guildId: int) -> User:
        """유저 정보 가져오기
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            
        Returns:
            User: 유저 정보
            
        """
        return self.userRepository.getUser(userId, guildId)

    def updateUserName(self, userId: int, guildId: int, newName: str) -> bool:
        """유저 이름 수정
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            newName: 새로운 이름
            
        Returns:
            bool: 성공 여부
        
        """
        return self.userRepository.setUserName(userId, guildId, newName)

    def addUserPoint(self, userId: int, guildId: int, points: int) -> bool:
        """유저 포인트 추가
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            points: 추가할 포인트
            
        Returns:
            bool: 성공 여부
        
        """
        return self.userRepository.addUserPoint(userId, guildId, points)

    def subtractUserPoint(self, userId: int, guildId: int, points: int) -> bool:
        """유저 포인트 차감
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            points: 차감할 포인트
            
        Returns:
            bool: 성공 여부
        
        """
        return self.userRepository.subUserPoint(userId, guildId, points)

    def setUserPoint(self, userId: int, guildId: int, points: int) -> bool:
        """유저 포인트 설정
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            points: 설정할 포인트
            
        Returns:
            bool: 성공 여부
        
        """
        return self.userRepository.setUserPoint(userId, guildId, points)

    def addUserExperience(self, userId: int, guildId: int, experience: int) -> bool:
        """유저 경험치 추가
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            experience: 추가할 경험치
            
        Returns:
            bool: 성공 여부
        
        """
        return self.userRepository.addUserExp(userId, guildId, experience)
    
    def setUserExperience(self, userId: int, guildId: int, experience: int) -> bool:
        """유저 경험치 설정
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            experience: 설정할 경험치
            
        Returns:
            bool: 성공 여부
        
        """
        return self.userRepository.setUserExp(userId, guildId, experience)