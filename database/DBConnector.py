# Importing libraries
import mysql.connector
import threading
import time

# Importing Custom Modules
from utils.initialize import getDBconfig
from utils import ServerLog as log

# =======[ 기본 설정 ]===================================================

db_dict = getDBconfig()

db_config = {
    'host': db_dict['HOST'],
    'user': db_dict['USER'],
    'password': db_dict['PASSWORD'],
    'database': db_dict['DATABASE'],
    'raise_on_warnings': db_dict['RAISE_ON_WARNINGS']
}
db_commit_threshold = db_dict['DB_COMMIT_THRESHOLD']
db_ping_interval = db_dict['DB_PING_INTERVAL']

# =======[ DB 연결 클래스 ]==============================================

class DBConnector:
    """MySQL 데이터베이스 싱글톤 클래스"""
    _instance = None  # 클래스 인스턴스 변수

    def __new__(cls):
        """싱글톤 패턴을 통해 하나의 DB 연결 인스턴스만 생성"""
        if cls._instance is None:
            cls._instance = super(DBConnector, cls).__new__(cls)

        return cls._instance
    
    def __init__(self):
        """생성자"""
        if not hasattr(self, 'conn'):
            try:
                self.conn = mysql.connector.connect(**db_config)
                self.count = 0
                self.commit_threshold = db_commit_threshold

                if self.conn.is_connected():
                    DBConnector.info("DB Connected to MySQL Server version " + self.conn.get_server_info())

                self.keep_alive_thread = threading.Thread(target=self.keep_alive, daemon=True)
                self.keep_alive_thread.start()

            except Exception as e:
                DBConnector.err("DB Connection Error: " + str(e))


    @staticmethod
    def info(msg) -> None:
        """정보 로그 출력 함수"""
        log.printInfoLog("database.DBConnector: " + msg)

    @staticmethod
    def err(msg) -> None:
        """에러 로그 출력 함수"""
        log.printErrorLog("database.DBConnector: " + str(msg))

    def keep_alive(self) -> None:
        """DB 연결 유지 함수"""
        while True:
            try:
                if self.conn.is_connected():
                    self.conn.ping(reconnect=True)
                    DBConnector.info("Ping sent to keep the DB Connection is alive")

                else:
                    self.conn.reconnect(attempts=3, delay=5)
                    DBConnector.info("DB Connection Reconnected")

            except mysql.connector.Error as e:
                DBConnector.err("DB Connection Error Occurred: " + str(e))
            
            time.sleep(db_ping_interval)

    # =====[Initialize]=================================================

    def forceCommitDB(self) -> None:
        """DB 강제 커밋 함수"""
        try:
            self.conn.commit()
            self.count = 0
            DBConnector.info("DB Committed by Force")

        except Exception as e:
            self.conn.rollback()
            DBConnector.err("DB Commit Error: " + str(e))

    def commitDB(self) -> None:
        """DB 커밋 함수"""
        try:
            self.count += 1

            if self.count >= self.commit_threshold:
                self.conn.commit()
                self.count = 0
                DBConnector.info("DB Committed")

        except Exception as e:
            self.conn.rollback()
            DBConnector.err("DB Commit Error: " + str(e))


    #=====[Helper]==============================================================
    
    def getConnection(self):
        """DB 연결 객체 반환 함수"""
        return self.conn
    
    def getLength(self, table_name: str) -> int:
        """테이블의 길이 반환 함수
        
        Args:
            table_name: 테이블 이름
        
        Returns:
            int: 테이블의 길이, 존재하지 않을 경우 -1 반환
        
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            length = cursor.fetchone()[0]
            return length
        
        except mysql.connector.Error as err:
            DBConnector.err(err)
            return -1
        
        
db_connection = DBConnector()
