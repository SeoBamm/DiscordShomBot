# Import required libraries
from datetime import datetime
import mysql.connector
import math

# Import Custom Modules
from database.DBConnector import DBConnector
from utils import ServerLog as log
from domain.gamble.gamble_model import UserGamble

class UserGambleRepository:
    """유저 확률도박 정보 Respository 클래스"""

    def __init__(self):
        self.db_connector = DBConnector()
        self.conn = self.db_connector.getConnection()

    @staticmethod
    def info(msg) -> None:
        """정보 로그 출력 함수"""
        log.printInfoLog("domain.gamble.UserGambleRepository: " + msg)

    @staticmethod
    def err(msg) -> None:
        """에러 로그 출력 함수"""
        log.printErrorLog("domain.gamble.UserGambleRepository: " + str(msg))

    # =====[UserGamble Repository]=========================================

    def userExists(self, userNum: int) -> bool:
        """유저 확률도박 정보 존재 여부 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 유저 확률도박 정보 존재 여부
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_gamble WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()
        return result is not None
    
    async def addUserGambleData(self, userNum: int) -> UserGamble:
        """유저 확률도박 정보 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserGamble: 만들어진 유저 확률도박 정보, 실패할 경우 None 반환
        
        """
        try:
            if self.userExists(userNum):
                UserGambleRepository.info(f"User {userNum}'s Gamble Data Already Exists")
                return self.getUserGambleData(userNum)
            
            cursor = self.conn.cursor()
            query = "INSERT INTO user_gamble (user_num, user_gamble_time, user_gamble_cnt) VALUES (%s, %s, %s)"
            cursor.execute(query, (userNum, 0, 0))

            self.db_connector.forceCommitDB()
            return self.getUserGambleData(userNum)
    
        except mysql.connector.Error as e:
            UserGambleRepository.err(e)
            return None
            

    def getUserGambleData(self, userNum: int) -> UserGamble:
        """유저 확률도박 정보 반환 함수
        
        Args:
            userNum: 유저 번호
            
        Returns:
            UserGamble: 유저 확률도박 정보
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_gamble WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()

        if result is None:
            return None

        return UserGamble(
            user_num=result[0],
            user_gamble_time=result[1],
            user_gamble_cnt=result[2]
        )
    
    def updateUserGambleData(self, userNum: int, gambleTime: int, gambleStack: int) -> bool:
        """유저 확률도박 정보 업데이트 함수
        
        Args:
            userNum: 유저 번호
            gambleTime: 확률도박 시간
            gambleStack: 확률도박 스택
        
        Returns:
            bool: 업데이트 성공 여부
        
        """
        cursor = self.conn.cursor()
        query = "UPDATE user_gamble SET user_gamble_time = %s, user_gamble_cnt = %s WHERE user_num = %s"
        cursor.execute(query, (gambleTime, gambleStack, userNum))

        self.db_connector.commitDB()
        return True

    def updateUserGambleTime(self, userNum: int, gambleTime: int) -> bool:
        """유저 확률도박 정보 시간 업데이트 함수
        
        Args:
            userNum: 유저 번호
            gambleTime: 확률도박 시간
        
        Returns:
            bool: 업데이트 성공 여부
        
        """
        cursor = self.conn.cursor()
        query = "UPDATE user_gamble SET user_gamble_time = %s WHERE user_num = %s"
        cursor.execute(query, (gambleTime, userNum))

        self.db_connector.commitDB()
        return True
    
    def updateUserGambleStack(self, userNum: int, gambleStack: int) -> bool:
        """유저 확률도박 정보 스택 업데이트 함수
        
        Args:
            userNum: 유저 번호
            gambleStack: 확률도박 스택
        
        Returns:
            bool: 업데이트 성공 여부
        
        """
        cursor = self.conn.cursor()
        query = "UPDATE user_gamble SET user_gamble_cnt = %s WHERE user_num = %s"
        cursor.execute(query, (gambleStack, userNum))

        self.db_connector.commitDB()
        return True