# Importing Libraries

import random as rnd
import math

# Import Custom Modules

from domain.subsidy.subsidy_repository import UserSubsidyRepository
from domain.subsidy.subsidy_model import UserSubsidy

class UserSubsidyService:
    """유저 지원금 정보 Service 클래스"""

    def __init__(self):
        self.userSubsidyRepository = UserSubsidyRepository()

    def subsidyDataExists(self, userNum: int) -> bool:
        """유저 지원금 정보 존재 여부 반환 함수

        Args:
            userNum: 유저 번호

        Returns:
            bool: 유저 지원금 정보 존재 여부

        """
        return self.userSubsidyRepository.userExists(userNum)
    
    async def addUserSubsidyData(self, userNum: int) -> UserSubsidy:
        """유저 지원금 정보 추가 함수

        Args:
            userNum: 유저 번호

        Returns:
            UserSubsidy: 만들어진 유저 지원금 정보, 실패할 경우 None 반환

        """
        result = await self.userSubsidyRepository.addUserSubsidyData(userNum)

    def getUserSubsidyData(self, userNum: int) -> UserSubsidy:
        """유저 지원금 정보 가져오기 함수

        Args:
            userNum: 유저 번호

        Returns:
            UserSubsidy: 유저 지원금 정보

        """
        return self.userSubsidyRepository.getUserSubsidyData(userNum)
    
    def updateUserSubsidyData(self, userNum: int, subsidyTime: int, subsidyStack: int) -> bool:
        """유저 지원금 정보 업데이트 함수

        Args:
            userNum: 유저 번호
            subsidyTime: 유저 지원금 시간
            subsidyStack: 유저 지원금 스택

        Returns:
            bool: 성공 여부

        """
        return self.userSubsidyRepository.updateUserSubsidyData(userNum, subsidyTime, subsidyStack)
    
    def receiveSubsidyReward(self, entirePoint: int) -> int:
        """지원금 반환 함수

        Args:
            entirePoint: 유저 보유 포인트

        Returns:
            int: 지원금 수량

        """
        # 기본금 30,000p 기준 전체 포인트가 낮을 수록 많이, 늪을 수록 적게 줌

        base = 30000  # 기준 포인트
        k = -0.5  # 로그 기울기 조정 (음수여야 감소 효과가 생김)

        # 포인트가 0 이하일 경우 지원 없음
        if entirePoint <= 0:
            return 0 
    
        # 로그 함수 적용
        correction_factor = 1 + k * math.log(entirePoint / base)
        
        # 최소 보정치 설정 (너무 작아지는 것 방지)
        correction_factor = max(2/30, correction_factor)  # 최소 2000 p 보정 유지

        # 0.8 ~ 1.2 사이의 랜덤 가중치
        randomPointWeight = rnd.uniform(0.9, 1.1)

        # 최종 지원금 계산
        subsidy = int(base * correction_factor * randomPointWeight)

        return subsidy
        



