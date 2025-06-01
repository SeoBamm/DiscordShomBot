# Importing Libraries
import random as rnd
import math

# Import Custom Modules
from domain.fish.fish_repository import UserFishRepository
from domain.fish.fish_model import UserFish

from domain.user.user_service import UserService
from domain.user.user_model import User

class UserFishService:
    """유저 낚시 정보 Service 클래스"""

    def __init__(self):
        self.userFishRepository = UserFishRepository()

    def fishDataExists(self, userNum: int) -> bool:
        """유저 낚시 정보 존재 여부 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 유저 낚시 정보 존재 여부
        
        """
        return self.userFishRepository.userExists(userNum)
    
    async def addUserFishData(self, userNum: int) -> UserFish:
        """유저 낚시 정보 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserFish: 만들어진 유저 낚시 정보, 실패할 경우 None 반환
        
        """
        return await self.userFishRepository.addUserFishData(userNum)
        
    def getUserFishData(self, userNum: int) -> UserFish:
        """유저 낚시 정보 가져오기 함수

        Args:
            userNum: 유저 번호

        Returns:
            UserFish: 유저 낚시 정보

        """
        return self.userFishRepository.getUserFishData(userNum)
    
    def updateUserFishData(self, userNum: int, fishTime: int, fishCnt: int, fishSuccess: int, fishGreat: int,fishBoots: int, fishBlow: int, fishNow: int) -> bool:
        """유저 낚시 정보 업데이트 함수
        
        Args:
            userNum: 유저 번호
            fishTime: 유저 낚시 시간
            fishCnt: 유저 낚시 횟수
            fishSuccess: 유저 낚시 성공 횟수
            fishGreat: 유저 낚시 대성공 횟수
            fishBoots: 유저 낚시 부츠 횟수
            fishBlow: 유저 낚시 복어 횟수
            fishNow: 유저 낚시 현재 상태
        
        Returns:
            bool: 성공 여부

        """
        return self.userFishRepository.updateUserFishData(userNum, fishTime, fishCnt, fishSuccess, fishGreat, fishBoots, fishBlow, fishNow)
    
    def addFishCnt(self, userNum: int) -> bool:
        """유저 낚시 횟수 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 성공 여부

        """
        userFish = self.getUserFishData(userNum)
        userFish.user_fish_cnt += 1
        return self.userFishRepository.updateUserFishCnt(userNum, userFish.user_fish_cnt)
    
    def addSuccessFishCnt(self, userNum: int) -> bool:
        """유저 낚시 성공 횟수 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 성공 여부

        """
        userFish = self.getUserFishData(userNum)
        userFish.user_fish_success += 1
        return self.userFishRepository.updateUserFishSuccess(userNum, userFish.user_fish_success)

    def addGreatFishCnt(self, userNum: int) -> bool:
        """유저 낚시 대성공 횟수 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 성공 여부

        """
        userFish = self.getUserFishData(userNum)
        userFish.user_fish_great += 1
        return self.userFishRepository.updateUserFishGreat(userNum, userFish.user_fish_great)
    
    def addBootsFishCnt(self, userNum: int) -> bool:
        """유저 낚시 부츠 횟수 추가 함수

        Args:
            userNum: 유저 번호

        Returns:
            bool: 성공 여부

        """
        userFish = self.getUserFishData(userNum)
        userFish.user_fish_boots += 1
        return self.userFishRepository.updateUserFishBoots(userNum, userFish.user_fish_boots)
    
    def addBlowFishCnt(self, userNum: int) -> bool:
        """유저 낚시 복어 횟수 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 성공 여부

        """
        userFish = self.getUserFishData(userNum)
        userFish.user_fish_blow += 1
        return self.userFishRepository.updateUserFishBlow(userNum, userFish.user_fish_blow)

    def toggleFishNow(self, userNum: int) -> bool:
        """유저 낚시 현재 상태 변경 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 성공 여부

        """
        userFish = self.getUserFishData(userNum)
        userFish.user_fish_now = 1 - userFish.user_fish_now
        return self.userFishRepository.updateUserFishNow(userNum, userFish.user_fish_now)
    
    def getFishResult(self) -> int:
        """낚시 결과 반환 함수
        
        Returns:
            int: 낚시 결과(0: 실패, 1: 성공, 2: 부츠, 3: 월척)
        
        """
        # 낚시 확률
        # 실패: 10%, 성공: 75%, 부츠: 8%, 복어: 5%, 월척: 2%
        fishRate = [0.1, 0.75, 0.08, 0.05, 0.02]
        fishResult = rnd.choices([0, 1, 2, 3, 4], fishRate)[0]

        return fishResult
    
    def receiveFishReward(self, userLevel: int, bootsCnt: int, fishCnt: int) -> tuple:
        """낚시 보상 반환 함수
        
        Args:
            userLevel: 유저 레벨
            bootsCnt: 부츠 낚은 횟수
            fishCnt: 낚시 횟수
        
        Returns:
            tuple: 낚시 결과, 보상 경험치, 보상 포인트, 이벤트 코드
        
        """
        fishResult = self.getFishResult()
        primaryExp = 20

        # 낚시 이벤트 코드 정리
        # 0: 특별한 이벤트 없음
        # 1: 부츠를 77번 낚음         -> 경험치 0, 포인트 7,777,777
        # 2: 첫 낚시에 월척을 낚음     -> 보상 5배

        rewardPoint = 0
        rewardExp = 0
        rewardCode = 0

        reward = math.floor(
            (3000 + 97000 * (1 - math.exp(-0.0691 * userLevel))) * rnd.uniform(0.9, 1.1))
            
        # 낚시 실패 시 경험치 5, 포인트 0 반환
        if fishResult == 0:
            
            rewardPoint = 5
            rewardExp = 0
            rewardCode = 0
            
        # 낚시 성공 시 경험치 20, 레벨에 비례한 포인트 반환
        elif fishResult == 1:

            rewardExp = primaryExp
            rewardPoint = reward
        
        # 부츠 낚을 시 경험치 0, 부츠를 77번 낚았을 때 7,777,777 포인트 반환, 나머지는 1 포인트 반환
        elif fishResult == 2:

            rewardExp = 0

            if bootsCnt == 76:

                rewardPoint = 7777777
                rewardCode = 1
            
            else:
                
                rewardPoint = 1

        # 복어 낚을 시 경험치 20, 레벨에 비례한 음수 포인트 반환
        elif fishResult == 3:

            rewardExp = primaryExp
            rewardPoint = reward

        # 월척 낚을 시 일반 낚시의 2배 보상 경험치, 레벨 반환, 첫트만에 월척을 낚았을 경우 5배 보상
        elif fishResult == 4:

            if fishCnt == 0:
                
                rewardExp = primaryExp * 5
                rewardPoint = reward * 5
                rewardCode = 2
            
            else:
                
                rewardExp = primaryExp * 2
                rewardPoint = reward * 2

        return fishResult, rewardExp, rewardPoint, rewardCode
            
        


        
        

