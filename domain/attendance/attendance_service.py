# Importing Libraries
import random as rnd
import math

# Import Custom Modules
from domain.attendance.attendance_repository import UserAttendanceRepository
from domain.attendance.attendance_model import UserAttendance

class UserAttendanceService:
    """유저 출석 정보 Service 클래스"""

    def __init__(self):
        self.userAttendanceRepository = UserAttendanceRepository()

    def attendanceDataExists(self, userNum: int) -> bool:
        """유저 출석 정보 존재 여부 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 유저 출석 정보 존재 여부
        
        """
        return self.userAttendanceRepository.userExists(userNum)
    
    async def addUserAttendanceData(self, userNum: int) -> UserAttendance:
        """유저 출석 정보 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserAttendance: 만들어진 유저 출석 정보, 실패할 경우 None 반환
        
        """
        return await self.userAttendanceRepository.addUserAttendanceData(userNum)
    
    def getUserAttendanceData(self, userNum: int) -> UserAttendance:
        """유저 출석 정보 가져오기 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserAttendance: 유저 출석 정보
        
        """
        return self.userAttendanceRepository.getUserAttendanceData(userNum)
    
    def updateUserAttendanceData(self, userNum: int, userAtt: str, userAttTotal: int, userAttStack: int) -> bool:
        """유저 출석 정보 업데이트 함수
        
        Args:
            userNum: 유저 번호
            userAtt: 유저 출석 일시
            userAttTotal: 유저 출석 누적 일수
            userAttStack: 유저 출석 스택
        
        Returns:
            bool: 성공 여부
        
        """
        return self.userAttendanceRepository.updateUserAttendanceData(userNum, userAtt, userAttTotal, userAttStack)    

    def getUserAttendanceWeight(self, attTotal: int, attStack: int) -> float:
        """유저 출석 가중치 계산 함수

        Args:
            attTotal: 유저 출석 총 횟수
            attStack: 유저 출석 스택

        Returns:
            float: 유저 출석 가중치

        """
        return math.log2(attTotal + 1) * min(attStack, 5)
    
    def receiveAttendanceReward(self, attTotal: int, attStack: int) -> tuple:
        """출석 보상 경험치, 포인트 반환 함수
        
        Args:
            attTotal: 유저 출석 총 횟수
            attStack: 유저 출석 스택
        
        Returns:
            tuple: 출석 보상 경험치, 포인트
        
        """
        rewardWeight = self.getUserAttendanceWeight(attTotal, attStack)

        # 0.8 ~ 1.2 사이의 랜덤 가중치
        # 포인트를 많이 받으면 경험치는 적게 받음
        randomPointWeight = rnd.uniform(0.8, 1.2)
        randomExpWeight = 2 - randomPointWeight

        rewardPoint, rewardExp = int(rewardWeight * randomPointWeight * 10000), int(rewardWeight * randomExpWeight * 128)

        return rewardExp, rewardPoint




