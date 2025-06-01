# Import required libraries
from datetime import datetime
import mysql.connector
import math

# Import Custom Modules
from database.DBConnector import DBConnector
from utils import ServerLog as log
from domain.russian.russian_model import UserRussian

class UserRussianRepository:
    """유저 러시안 룰렛 정보 Respository 클래스"""

    def __init__(self):
        self.db_connector = DBConnector()
        self.conn = self.db_connector.getConnection()

    @staticmethod
    def info(msg) -> None:
        """정보 로그 출력 함수"""
        log.printInfoLog("domain.russian.UserRussianRepository: " + msg)

    @staticmethod
    def err(msg) -> None:
        """에러 로그 출력 함수"""
        log.printErrorLog("domain.russian.UserRussianRepository: " + str(msg))

    # =====[UserRussian Repository]=========================================

    def userExists(self, userNum: int) -> bool:
        """유저 러시안 룰렛 정보 존재 여부 반환 함수

        Args:
            userNum: 유저 번호

        Returns:
            bool: 유저 러시안 룰렛 정보 존재 여부

        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_russian WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()
        return result is not None
    
    async def addUserRussianData(self, userNum: int) -> UserRussian:
        """유저 러시안 룰렛 정보 추가 함수

        Args:
            userNum: 유저 번호

        Returns:
            UserRussian: 만들어진 유저 러시안 룰렛 정보, 실패할 경우 None 반환

        """
        try:
            if self.userExists(userNum):
                UserRussianRepository.info(f"User {userNum}'s Russian Data Already Exists")
                return self.getUserRussianData(userNum)
            
            cursor = self.conn.cursor()
            query = "INSERT INTO user_russian (user_num, user_russian_time, user_russian_cnt) VALUES (%s, %s, %s)"
            cursor.execute(query, (userNum, 0, 0))
            
            self.db_connector.forceCommitDB()
            return self.getUserRussianData(userNum)
        
        except mysql.connector.Error as e:
            UserRussianRepository.err(f"User {userNum}'s Russian Data Add Failed: {e}")
            return None
        
    def getUserRussianData(self, userNum: int) -> UserRussian:
        """유저 러시안 룰렛 정보 반환환 함수

        Args:
            userNum: 유저 번호

        Returns:
            UserRussian: 유저 러시안 룰렛 정보

        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_russian WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()
        if result is None:
            return None

        return UserRussian(
            user_num=result[0],
            user_russian_time=result[1],
            user_russian_cnt=result[2],
            user_russian_dead=result[3]
        )
    
    def updateUserRussianData(self, userNum: int, russianTime: int, russianStack: int) -> bool:
        """유저 러시안 룰렛 정보 업데이트 함수

        Args:
            userNum: 유저 번호
            russianTime: 유저 러시안 룰렛 시간
            russianStack: 유저 러시안 룰렛 스택

        Returns:
            bool: 성공 여부

        """
        cursor = self.conn.cursor()
        query = "UPDATE user_russian SET user_russian_time = %s, user_russian_cnt = %s WHERE user_num = %s"
        cursor.execute(query, (russianTime, russianStack, userNum))

        self.db_connector.commitDB()
        return True
    
    def updateUserRussianTime(self, userNum: int, russianTime: int) -> bool:
        """유저 러시안 룰렛 시간 업데이트 함수

        Args:
            userNum: 유저 번호
            russianTime: 유저 러시안 룰렛 시간

        Returns:
            bool: 성공 여부

        """
        cursor = self.conn.cursor()
        query = "UPDATE user_russian SET user_russian_time = %s WHERE user_num = %s"
        cursor.execute(query, (russianTime, userNum))

        self.db_connector.commitDB()
        return True
    
    def updateUserRussianStack(self, userNum: int, russianStack: int) -> bool:
        """유저 러시안 룰렛 스택 업데이트 함수

        Args:
            userNum: 유저 번호
            russianStack: 유저 러시안 룰렛 스택

        Returns:
            bool: 성공 여부

        """
        cursor = self.conn.cursor()
        query = "UPDATE user_russian SET user_russian_cnt = %s WHERE user_num = %s"
        cursor.execute(query, (russianStack, userNum))

        self.db_connector.commitDB()
        return True
    
    def updateUserRussianDead(self, userNum: int, russianDead: int) -> bool:
        """유저 러시안 룰렛 데드 업데이트 함수

        Args:
            userNum: 유저 번호
            russianDead: 유저 러시안 룰렛 데드

        Returns:
            bool: 성공 여부

        """
        cursor = self.conn.cursor()
        query = "UPDATE user_russian SET user_russian_dead = %s WHERE user_num = %s"
        cursor.execute(query, (russianDead, userNum))

        self.db_connector.commitDB()
        return True