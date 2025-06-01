# Import required libraries

from datetime import datetime
import mysql.connector
import math

# Import Custom Modules

from database.DBConnector import DBConnector
from utils import ServerLog as log
from domain.subsidy.subsidy_model import UserSubsidy

class UserSubsidyRepository:
    """유저 지원금 정보 Respository 클래스"""

    def __init__(self):
        self.db_connector = DBConnector()
        self.conn = self.db_connector.getConnection()

    @staticmethod
    def info(msg) -> None:
        """정보 로그 출력 함수"""
        log.printInfoLog("domain.subsidy.UserSubsidyRepository: " + msg)

    @staticmethod
    def err(msg) -> None:
        """에러 로그 출력 함수"""
        log.printErrorLog("domain.subsidy.UserSubsidyRepository: " + str(msg))

    # =====[UserSubsidy Repository]=========================================

    def userExists(self, userNum: int) -> bool:
        """유저 지원금 정보 존재 여부 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 유저 지원금 정보 존재 여부
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_subsidy WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()
        return result is not None
    
    def getUserSubsidyData(self, userNum: int) -> UserSubsidy:
        """유저 지원금 정보 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserSubsidy: 유저 지원금 정보, 실패할 경우 None 반환
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_subsidy WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()
        if result is None:
            return None

        return UserSubsidy(
            user_num=result[0],
            user_subsidy_time=result[1],
            user_subsidy_cnt=result[2]
        )
    
    async def addUserSubsidyData(self, userNum: int) -> UserSubsidy:
        """유저 지원금 정보 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserSubsidy: 만들어진 유저 지원금 정보, 실패할 경우 None 반환
        
        """
        try:
            if self.userExists(userNum):
                UserSubsidyRepository.info(f"User {userNum}'s Subsidy Data Already Exists")
                return self.getUserSubsidyData(userNum)
            
            cursor = self.conn.cursor()
            query = "INSERT INTO user_subsidy (user_num, user_subsidy_time, user_subsidy_cnt) VALUES (%s, %s, %s)"
            cursor.execute(query, (userNum, 0, 0))

            self.db_connector.forceCommitDB()
            return self.getUserSubsidyData(userNum)
        except mysql.connector.Error as e:
            UserSubsidyRepository.err(e)
            return None
        
    def updateUserSubsidyData(self, userNum: int, subsidyTime: int, subsidyCnt: int) -> bool:
        """유저 지원금 정보 갱신 함수
        
        Args:
            userNum: 유저 번호
            subsidyTime: 지원금 시간
            subsidyCnt: 지원금 횟수
        
        Returns:
            bool: 갱신 성공 여부
        
        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_subsidy SET user_subsidy_time = %s, user_subsidy_cnt = %s WHERE user_num = %s"
            cursor.execute(query, (subsidyTime, subsidyCnt, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserSubsidyRepository.err(e)
            return False
        
    def updateUserSubsidyTime(self, userNum: int, subsidyTime: int) -> bool:
        """유저 지원금 시간 갱신 함수
        
        Args:
            userNum: 유저 번호
            subsidyTime: 지원금 시간
        
        Returns:
            bool: 갱신 성공 여부
        
        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_subsidy SET user_subsidy_time = %s WHERE user_num = %s"
            cursor.execute(query, (subsidyTime, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserSubsidyRepository.err(e)
            return False
        
    def updateUserSubsidyCnt(self, userNum: int, subsidyCnt: int) -> bool:
        """유저 지원금 횟수 갱신 함수
        
        Args:
            userNum: 유저 번호
            subsidyCnt: 지원금 횟수
        
        Returns:
            bool: 갱신 성공 여부
        
        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_subsidy SET user_subsidy_cnt = %s WHERE user_num = %s"
            cursor.execute(query, (subsidyCnt, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserSubsidyRepository.err(e)
            return False