# Import required libraries
import mysql.connector

# Import Custom Modules
from database.DBConnector import DBConnector
from utils import ServerLog as log
from domain.attendance.attendance_model import UserAttendance

class UserAttendanceRepository:
    """유저 출석 정보 Respository 클래스"""

    def __init__(self):
        self.db_connector = DBConnector()
        self.conn = self.db_connector.getConnection()

    @staticmethod
    def info(msg) -> None:
        """정보 로그 출력 함수"""
        log.printInfoLog("domain.attendance.UserAttendanceRepository: " + msg)

    @staticmethod
    def err(msg) -> None:
        """에러 로그 출력 함수"""
        log.printErrorLog("domain.attendance.UserAttendanceRepository: " + str(msg))

    # =====[UserAttendance Repository]=========================================

    def userExists(self, userNum: int) -> bool:
        """유저 출석 정보 존재 여부 반환 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            bool: 유저 출석 정보 존재 여부
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_attendance WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()
        return result is not None
    
    async def addUserAttendanceData(self, userNum: int) -> UserAttendance:
        """유저 출석 정보 추가 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserAttendance: 만들어진 유저 출석 정보, 실패할 경우 None 반환
        
        """
        try:
            if self.userExists(userNum):
                UserAttendanceRepository.info(f"User {userNum}'s Attendance Data Already Exists")
                return self.getUserAttendanceData(userNum)

            cursor = self.conn.cursor()
            query = "INSERT INTO user_attendance (user_num) VALUES (%s)"
            cursor.execute(query, (userNum,))

            self.db_connector.forceCommitDB()
            return self.getUserAttendanceData(userNum)
        
        except mysql.connector.Error as e:
            UserAttendanceRepository.err(e)
            return None
    
    def getUserAttendanceData(self, userNum: int) -> UserAttendance:
        """유저 출석 정보 가져오기 함수
        
        Args:
            userNum: 유저 번호
        
        Returns:
            UserAttendance: 유저 출석 정보
        
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM user_attendance WHERE user_num = %s"
        cursor.execute(query, (userNum,))

        result = cursor.fetchone()

        if result is None:
            return None
        
        return UserAttendance(
            user_num=result[0],
            user_att=result[1],
            user_att_total=result[2],
            user_att_stack=result[3]
        )
    

    def updateUserAttendanceData(self, userNum: int, userAtt: int, userAttTotal: int, userAttStack: int) -> tuple:
        """유저 출석 정보 업데이트 함수
        
        Args:
            userNum: 유저 번호
            userAtt: 유저 출석 횟수
            userAttTotal: 유저 출석 총 횟수
            userAttStack: 유저 출석 스택
        
        Returns:
            tuple: 성공 여부 및 출석 보상 경험치, 포인트트
        
        """
        try: 
            cursor = self.conn.cursor()
            query = "UPDATE user_attendance SET user_att = %s, user_att_total = %s, user_att_stack = %s WHERE user_num = %s"
            cursor.execute(query, (userAtt, userAttTotal, userAttStack, userNum))

            self.db_connector.commitDB()
            return True
        
        except mysql.connector.Error as e:
            UserAttendanceRepository.err(e)
            return False
        