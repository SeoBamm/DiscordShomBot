# Importing Libraries
import random as rnd
import math

# Import Custom Modules
from domain.russian.russian_repository import UserRussianRepository
from domain.russian.russian_model import UserRussian

class UserRussianService:
    """유저 러시안 룰렛 정보 Service 클래스"""

    def __init__(self):
        self.userRussianRepository = UserRussianRepository()

    def russianDataExists(self, userNum: int) -> bool:
        """유저 러시안 룰렛 정보 존재 여부 반환 함수

        Args:
            userNum: 유저 번호

        Returns:
            bool: 유저 러시안 룰렛 정보 존재 여부

        """
        return self.userRussianRepository.userExists(userNum)
    
    async def addUserRussianData(self, userNum: int) -> UserRussian:
        """유저 러시안 룰렛 정보 추가 함수

        Args:
            userNum: 유저 번호  

        Returns:
            UserRussian: 만들어진 유저 러시안 룰렛 정보, 실패할 경우 None 반환

        """
        return await self.userRussianRepository.addUserRussianData(userNum)
    
    def getUserRussianData(self, userNum: int) -> UserRussian:
        """유저 러시안 룰렛 정보 가져오기 함수

        Args:
            userNum: 유저 번호

        Returns:
            UserRussian: 유저 러시안 룰렛 정보

        """
        return self.userRussianRepository.getUserRussianData(userNum)
    
    def updateUserRussianData(self, userNum: int, russianTime: int, russianStack: int) -> bool:
        """유저 러시안 룰렛 정보 업데이트 함수

        Args:
            userNum: 유저 번호
            russianTime: 유저 러시안 룰렛 시간
            russianStack: 유저 러시안 룰렛 스택

        Returns:
            bool: 성공 여부
        """
        return self.userRussianRepository.updateUserRussianData(userNum, russianTime, russianStack)
    
    def updateUserRussianDead(self, userNum: int, russianDead: int) -> bool:
        """유저 러시안 룰렛 사망 정보 업데이트 함수

        Args:
            userNum: 유저 번호
            russianDead: 유저 러시안 룰렛 사망

        Returns:
            bool: 성공 여부
        """
        return self.userRussianRepository.updateUserRussianDead(userNum, russianDead)
    
    def russianResult(self) -> bool:
        """러시안 룰렛 결과 반환 함수

        Returns:
            bool: 러시안 룰렛 결과(True: 사망, False: 생존)
        """
        # 러시안 룰렛 확률
        # 1/6 확률로 사망
        russianRate = 1/6
        russianResult = rnd.random() < russianRate

        return russianResult
    
    def receiveRussianReward(self, point: int, exp: int) -> tuple:
        """러시안 룰렛 보상 반환 함수
        
        Args:
            point: 현재 포인트
            exp: 현재 경험치
            
        Returns:
            tuple: 생존 여부, 보상 경험치,  포인트
            
        """
        # 사망 시
        if self.russianResult():

            return False, 0, 0
        
        # 생존 시
        else:
            rewarpPoint = point
            rewardExp = 29 + int(math.log((point + 1)) / math.log(1.05) * 2.5)

            return True, rewardExp, rewarpPoint
