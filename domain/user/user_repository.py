# Import required libraries
import mysql.connector

# Import Custom Modules
from database.DBConnector import DBConnector
from utils import ServerLog as log
from domain.user.user_model import User

class UserRepository:
    """유저 정보 Repository 클래스"""

    def __init__(self):
        self.db_connector = DBConnector()
        self.conn = self.db_connector.getConnection()

    @staticmethod
    def info(msg) -> None:
        """정보 로그 출력 함수"""
        log.printInfoLog("domain.user.UserRepository: " + msg)

    @staticmethod
    def err(msg) -> None:
        """에러 로그 출력 함수"""
        log.printErrorLog("domain.user.UserRepository: " + str(msg))

    # =====[User Repository]=================================================

    def getUserLength(self) -> int:
        """전체 유저 수 반환 함수
        
        Returns:
            int: 전체 유저 수
        
        """
        return self.db_connector.getLength("user_data")
    
    def userExists(self, userId: int, guildId: int) -> bool:
        """유저 존재 여부 반환 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버버 ID
        
        Returns:
            bool: 유저 존재 여부
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_data WHERE user_id = %s AND user_guild = %s"
        cursor.execute(query, (userId, guildId))

        result = cursor.fetchone()
        return result is not None
    
    async def addUser(self, userId: int, guildId: int, userName: str) -> int:
        """유저 추가 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            userName: 유저 이름
        
        Returns:
            int: 성공 코드(1: 성공, 2: 실패, 3: 이미 존재)
        
        """
        try:
            if self.userExists(userId, guildId):
                UserRepository.info(f"User {userId} in guild {guildId} already exists")
                return 3

            cursor = self.conn.cursor()
            query = "INSERT INTO user_data (user_id, user_guild, user_name) VALUES (%s, %s, %s)"
            cursor.execute(query, (userId, guildId, userName))

            self.db_connector.forceCommitDB()
            return 1
        
        except mysql.connector.Error as e:
            UserRepository.err(e)
            return 2
        
    def getUser(self, userId, guildId) -> "User":
        """유저 정보 반환 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
        
        Returns:
            User: 유저 정보
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_data WHERE user_id = %s AND user_guild = %s"
        cursor.execute(query, (userId, guildId))

        result = cursor.fetchone()

        if result is None:
            return None
        
        return User(
            user_num=result[0],
            user_id=result[1],
            user_guild=result[2],
            user_name=result[3],
            user_exp=result[4],
            user_point=result[5]
        )

    def setUserAttributeWithCommit(self, userId: int, guildId: int, attr: str, value) -> bool:
        """유저 정보 수정 함수(커밋 포함)
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            attr: 수정할 속성
            value: 수정 값
        
        Returns:
            bool: 수정 성공 여부
        
        """
        try:
            cursor = self.conn.cursor()
            query = f"UPDATE user_data SET {attr} = %s WHERE user_id = %s AND user_guild = %s"
            cursor.execute(query, (value, userId, guildId))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserRepository.err(e)
            return False
        
    def setUserAttributeWithNoCommit(self, userId: int, guildId: int, attr: str, value) -> bool:
        """유저 정보 수정 함수(커밋 미포함)
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            attr: 수정할 속성
            value: 수정 값
        
        Returns:
            bool: 수정 성공 여부
        
        """
        try:
            cursor = self.conn.cursor()
            query = f"UPDATE user_data SET {attr} = %s WHERE user_id = %s AND user_guild = %s"
            cursor.execute(query, (value, userId, guildId))

            return True
        
        except mysql.connector.Error as e:
            UserRepository.err(e)
            return False
        
    def setUserName(self, userId: int, guildId: int, newName: str) -> bool:
        """유저 이름 수정 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            newName: 새로운 유저 이름
        
        Returns:
            bool: 수정 성공 여부
        
        """
        return self.setUserAttributeWithCommit(userId, guildId, "user_name", newName)
    
    def addUserPoint(self, userId: int, guildId: int, point: int) -> bool:
        """유저 포인트 추가 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            point: 추가할 포인트
        
        Returns:
            bool: 추가 성공 여부
        
        """
        return self.setUserAttributeWithCommit(userId, guildId, "user_point", self.getUser(userId, guildId).user_point + point)
    
    def subUserPoint(self, userId: int, guildId: int, point: int) -> bool:
        """유저 포인트 차감 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            point: 차감할 포인트
        
        Returns:
            bool: 차감 성공 여부
        
        """
        return self.setUserAttributeWithCommit(userId, guildId, "user_point", self.getUser(userId, guildId).user_point - point)
    
    
    def setUserPoint(self, userId: int, guildId: int, point: int) -> bool:
        """유저 포인트 설정 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            point: 설정할 포인트
        
        Returns:
            bool: 설정 성공 여부
        
        """
        res = self.setUserAttributeWithNoCommit(userId, guildId, "user_point", point)
        # if res:
        #     self.db_connector.forceCommitDB()

        return res
    
    def addUserExp(self, userId: int, guildId: int, exp: int) -> bool:
        """유저 경험치 추가 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            exp: 추가할 경험치
        
        Returns:
            bool: 추가 성공 여부
        
        """
        return self.setUserAttributeWithCommit(userId, guildId, "user_exp", self.getUser(userId, guildId).user_exp + exp)
    
    def setUserExp(self, userId: int, guildId: int, exp: int) -> bool:
        """유저 경험치 설정 함수
        
        Args:
            userId: 유저 ID
            guildId: 서버 ID
            exp: 설정할 경험치
        
        Returns:
            bool: 설정 성공 여부
        
        """
        return self.setUserAttributeWithCommit(userId, guildId, "user_exp", exp)