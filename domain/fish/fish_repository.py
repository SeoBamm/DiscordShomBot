# Import required libraries
from datetime import datetime
import mysql.connector
import math

# Import Custom Modules
from database.DBConnector import DBConnector
from utils import ServerLog as log
from domain.fish.fish_model import UserFish

class UserFishRepository:
    """유저 낚시 정보 Respository 클래스"""

    def __init__(self):
        self.db_connector = DBConnector()
        self.conn = self.db_connector.getConnection()

    @staticmethod
    def info(msg) -> None:
        """정보 로그 출력 함수"""
        log.printInfoLog("domain.fish.UserFishRepository: " + msg)

    @staticmethod
    def err(msg) -> None:
        """에러 로그 출력 함수"""
        log.printErrorLog("domain.fish.UserFishRepository: " + str(msg))

    # =====[UserFish Repository]=========================================

    def userExists(self, userNum: int) -> bool:
        """유저 낚시 정보 존재 여부 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 유저 낚시 정보 존재 여부
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_fish WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()
        return result is not None
    
    async def addUserFishData(self, userNum: int) -> UserFish:
        """유저 낚시 정보 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserFish: 만들어진 유저 낚시 정보, 실패할 경우 None 반환
        
        """
        try:
            if self.userExists(userNum):
                UserFishRepository.info(f"User {userNum}'s Fish Data Already Exists")
                return self.getUserFishData(userNum)
            
            cursor = self.conn.cursor()
            query = "INSERT INTO user_fish (user_num, user_fish_time, user_fish_cnt, user_fish_success, user_fish_great, user_fish_boots, user_fish_blow, user_fish_now) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (userNum, 0, 0, 0, 0, 0, 0, 0))
            self.db_connector.forceCommitDB()
            
            UserFishRepository.info(f"User {userNum}'s Fish Data Added")
            return self.getUserFishData(userNum)
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in addUserFishData: {e}")
            return None
        
    def getUserFishData(self, userNum: int) -> UserFish:
        """유저 낚시 정보 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserFish: 유저 낚시 정보
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_fish WHERE user_num = %s"
        cursor.execute(query, (userNum,))
        
        result = cursor.fetchone()
        return UserFish.from_dict({
            "user_num": result[0],
            "user_fish_time": result[1],
            "user_fish_cnt": result[2],
            "user_fish_success": result[3],
            "user_fish_great": result[4],
            "user_fish_boots": result[5],
            "user_fish_blow": result[6],
            "user_fish_now": result[7]
        })
    
    def updateUserFishData(self, userNum: int, fishTime: int, fishCnt: int, fishSuccess: int, fishGreat: int, fishBoots: int, fishBlow: int, fishNow: int) -> bool:
        """유저 낚시 정보 업데이트 함수

        Args:
            userNum: 유저 번호
            fishTime: 낚시 시간
            fishCnt: 낚시 수
            fishSuccess: 낚시 성공 수
            fishGreat: 월척 낚은 수
            fishBoots: 부츠 낚은 수
            fishBlow: 복어 낚은은 수
            fishNow: 현재 물고기 수

        Returns:
            bool: 업데이트 성공 여부

        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_fish SET user_fish_time = %s, user_fish_cnt = %s, user_fish_success = %s, user_fish_great = %s, user_fish_boots = %s, user_fish_blow = %s, user_fish_now = %s WHERE user_num = %s"
            cursor.execute(query, (fishTime, fishCnt, fishSuccess, fishGreat, fishBoots, fishBlow, fishNow, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in updateUserFishData: {e}")
            return False
        
    def updateUserFishTime(self, userNum: int, fishTime: int) -> bool:
        """유저 낚시 시간 업데이트 함수

        Args:
            userNum: 유저 번호
            fishTime: 낚시 시간

        Returns:
            bool: 업데이트 성공 여부

        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_fish SET user_fish_time = %s WHERE user_num = %s"
            cursor.execute(query, (fishTime, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in updateUserFishTime: {e}")
            return False
        
    def updateUserFishCnt(self, userNum: int, fishCnt: int) -> bool:
        """유저 낚시 수 업데이트 함수

        Args:
            userNum: 유저 번호
            fishCnt: 낚시시 수

        Returns:
            bool: 업데이트 성공 여부

        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_fish SET user_fish_cnt = %s WHERE user_num = %s"
            cursor.execute(query, (fishCnt, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in updateUserFishCnt: {e}")
            return False
        
    def updateUserFishSuccess(self, userNum: int, fishSuccess: int) -> bool:
        """유저 낚시 성공 수 업데이트 함수

        Args:
            userNum: 유저 번호
            fishSuccess: 낚시 성공 수

        Returns:
            bool: 업데이트 성공 여부

        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_fish SET user_fish_success = %s WHERE user_num = %s"
            cursor.execute(query, (fishSuccess, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in updateUserFishSuccess: {e}")
            return False
        
    def updateUserFishGreat(self, userNum: int, fishGreat: int) -> bool:
        """유저 월척 낚은 수 업데이트 함수

        Args:
            userNum: 유저 번호
            fishGreat: 월척 낚은 수

        Returns:
            bool: 업데이트 성공 여부

        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_fish SET user_fish_great = %s WHERE user_num = %s"
            cursor.execute(query, (fishGreat, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in updateUserFishGreat: {e}")
            return False
        
    def updateUserFishBoots(self, userNum: int, fishBoots: int) -> bool:
        """유저 부츠 낚은 수 업데이트 함수

        Args:
            userNum: 유저 번호
            fishBoots: 부츠 낚은 수

        Returns:
            bool: 업데이트 성공 여부

        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_fish SET user_fish_boots = %s WHERE user_num = %s"
            cursor.execute(query, (fishBoots, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in updateUserFishBoots: {e}")
            return False
        
    def updateUserFishBlow(self, userNum: int, fishBlow: int) -> bool:
        """유저 복어 낚은 수 업데이트 함수

        Args:
            userNum: 유저 번호
            fishBlow: 복어 낚은 수

        Returns:
            bool: 업데이트 성공 여부

        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_fish SET user_fish_blow = %s WHERE user_num = %s"
            cursor.execute(query, (fishBlow, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in updateUserFishBlow: {e}")
            return False
        
    def updateUserFishNow(self, userNum: int, fishNow: int) -> bool:
        """유저 현재 낚시 유무 업데이트 함수

        Args:
            userNum: 유저 번호
            fishNow: 현재 낚시 유무

        Returns:
            bool: 업데이트 성공 여부

        """
        try:
            cursor = self.conn.cursor()
            query = "UPDATE user_fish SET user_fish_now = %s WHERE user_num = %s"
            cursor.execute(query, (fishNow, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserFishRepository.err(f"Error in updateUserFishNow: {e}")
            return False

