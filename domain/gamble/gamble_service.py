# Importing Libraries
import random as rnd
import math

# Import Custom Modules
from domain.gamble.gamble_repository import UserGambleRepository
from domain.gamble.gamble_model import UserGamble

class UserGambleService:
    """유저 확률도박 정보 Service 클래스"""

    def __init__(self):
        self.userGambleRepository = UserGambleRepository()

    def gambleDataExists(self, userNum: int) -> bool:
        """유저 확률도박 정보 존재 여부 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 유저 확률도박 정보 존재 여부
        
        """
        return self.userGambleRepository.userExists(userNum)
    
    async def addUserGambleData(self, userNum: int) -> UserGamble:
        """유저 확률도박 정보 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserGamble: 만들어진 유저 확률도박 정보, 실패할 경우 None 반환
        
        """
        return await self.userGambleRepository.addUserGambleData(userNum)
    
    def getUserGambleData(self, userNum: int) -> UserGamble:
        """유저 확률도박 정보 가져오기 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserGamble: 유저 확률도박 정보
        
        """
        return self.userGambleRepository.getUserGambleData(userNum)
    
    def updateUserGambleData(self, userNum: int, gambleTime: int, gambleStack: int) -> bool:
        """유저 확률도박 정보 업데이트 함수
        
        Args:
            userNum: 유저 번호
            gambleTime: 유저 확률도박 시간
            gambleStack: 유저 확률도박 스택
        
        Returns:
            bool: 성공 여부

        """
        return self.userGambleRepository.updateUserGambleData(userNum, gambleTime, gambleStack)
    
    def getGambleResult(self, gambleTier: int) -> bool:
        """도박 결과 반환 함수
        
        Args:
            gambleTier: 위험도(저: 0, 중: 1, 고: 2)
            
        Returns:
            bool: 도박 결과
        
        """
        # 도박 확률
        # 저위험: 50%, 중위험: 30%, 고위험: 20%
        gambleRate = [0.5, 0.3, 0.2]
        result = rnd.random()

        return result < gambleRate[gambleTier]
    
    def receiveGambleReward(self, point: int, gambleTier: int) -> tuple:
        """도박 보상 반환 함수
        
        Args:
            point: 도박 판돈
            gambleTier: 위험도(저: 0, 중: 1, 고: 2)
            
        Returns:
            tuple: 성공 여부, 도박 보상 경험치, 포인트
        
        """
        if self.getGambleResult(gambleTier):
            # 도박 배율
            # 저위험: 2배, 중위험: 4배, 고위험: 6배
            gambleRate = [1, 3, 5]
            rewardPoint = point * gambleRate[gambleTier]
            rewardExp = math.log2(rewardPoint + 1) * gambleRate[gambleTier]

            return True, rewardExp, rewardPoint
        
        else: 
            # 도박 실패 시 판돈의 30% 반환, 경험치 1~2 반환
            rewardPoint = point * 0.7
            rewardExp = rnd.randint(1, 2)

            return False, rewardExp, rewardPoint

    def getSlotResult(self) -> tuple:
        """슬롯머신 결과 반환 함수
        
        Returns:
            tuple: 슬롯머신 결과, 결과 배열
        
        """
        symbolNum = [0, 1, 2, 3, 4, 5, 6, 7] # 0~7까지의 숫자로 설정
        chance = [29, 24, 19, 14, 12, 10, 7, 5] # 확률을 100 기준으로 설정

        slotResult = []
        for i in range(3):
            slotResult.append(rnd.choices(symbolNum, chance)[0]) # 3개의 결과를 뽑아내어 리스트에 저장

        # slotResult = [1, 5, 1]

        result = -1

        # 첫 번째가 조커일 경우  
        if slotResult[0] == 5:  
            
            # 두 번째가 조커일 경우
            if slotResult[1] == 5:    

                # 세 번째가 조커일 경우
                if slotResult[2] == 5:
                    result = 5

                # 앞에 2개가 조커일 경우
                else:
                    result = slotResult[2]

            # 세 번째가 조커일 경우
            elif slotResult[2] == 5:
                result = slotResult[1]

            # 둘 다 조커가 아닐 경우
            else:
                result = slotResult[1] if slotResult[1] == slotResult[2] else -1

        # 두 번째가 조커일 경우
        elif slotResult[1] == 5:

            # 세 번째가 조커일 경우
            if slotResult[2] == 5:
                result = slotResult[0]

            # 둘 다 조커가 아닐 경우
            else:
                result = slotResult[0] if slotResult[0] == slotResult[2] else -1

        # 세 번째가 조커일 경우
        elif slotResult[2] == 5:
            
            result = slotResult[0] if slotResult[0] == slotResult[1] else -1

        # 조커가 없을 경우
        else:
            result = slotResult[0] if slotResult[0] == slotResult[1] == slotResult[2] else -1

        return result, slotResult

        
    def receiveSlotReward(self, point: int) -> tuple:
        """슬롯머신 보상 반환 함수
        
        Args:
            result: 슬롯머신 결과
            point: 슬롯머신 판돈
        
        Returns:
            tuple: 슬롯 결과, 슬롯머신 결과 배열, 보상 경험치, 포인트
        
        """
        weights = [4, 8, 16, 39, 54, 79, 776, 999] # 보상 가중치

        slotResult = self.getSlotResult()
        rewardPoint = 0
        rewardExp = 0

        if slotResult[0] == -1:
            rewardPoint = point
            rewardExp = rnd.randint(2, 5)

        else:
            rewardPoint = point * weights[slotResult[0]]
            rewardExp = math.log2(rewardPoint + 1) * (1 + slotResult[0])

        return slotResult[0], slotResult[1], rewardExp, rewardPoint

    def showSlotResult(self, resultArray) -> str:
        """슬롯머신 결과 출력 함수
        
        Args:
            resultArray: 슬롯머신 결과 배열
        
        Returns:
            str: 슬롯머신 결과 출력
        
        """
        symbols = [":cherries:", ":lemon:", ":tangerine:", ":watermelon:", ":grapes:", ":black_joker:", ":seven:", ":gem:"]

        return f"『ㅤ{symbols[resultArray[0]]}ㅤ{symbols[resultArray[1]]}ㅤ{symbols[resultArray[2]]}ㅤ』"