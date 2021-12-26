from config import *
import pyodbc
import datetime
import uuid

db_connection = pyodbc.connect("Driver={SQL Server};"
                               f"Server={CONFIG_DB_SERVER};"
                               "Database=master;"
                               "Trusted_Connection=yes;")
db_connection.autocommit = True
db_cursor = db_connection.cursor()

def create_db(db_cursor):
    sql_query = """
    IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'TicTacToe')
    BEGIN
        CREATE DATABASE TicTacToe
    END
    """
    db_cursor.execute(sql_query)

def create_tables(db_cursor):
    sql_query = """
    USE TicTacToe;
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='GameSession' and xtype='U')
    BEGIN
        CREATE TABLE GameSession (
            SessionID nvarchar(36),
            GameMode int,
            GameStarted datetime,
            GameEnded datetime,
            Status nvarchar(16),
            CONSTRAINT PK_GameSession_SessionID PRIMARY KEY CLUSTERED (SessionID ASC)
        )
    END;
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='GameDetails' and xtype='U')
    BEGIN
        CREATE TABLE GameDetails (
            SessionID nvarchar(36),
            TurnTime datetime,
            Turn nvarchar(1),
            Position nvarchar(3),
	        CONSTRAINT FK_GameDetails_SessionID FOREIGN KEY (SessionID) REFERENCES [dbo].[GameSession](SessionID)
        )
    END
    """
    db_cursor.execute(sql_query)

class GameSession:
    def __init__(self, game_mode, db_cursor):
        self.DB_CURSOR = db_cursor
        self.SESSION_ID = str(uuid.uuid4())
        self.GAME_MODE = game_mode
        self.GAME_STARTED = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.GAME_ENDED = "NULL"
        self.STATUS = "In Progress"

    def write_session(self):
        sql_query = f"""
        USE TicTacToe;
        INSERT INTO GameSession (SessionID, GameMode, GameStarted, GameEnded, Status)
        VALUES ('{self.SESSION_ID}', {self.GAME_MODE}, '{self.GAME_STARTED}', {self.GAME_ENDED}, '{self.STATUS}');
        """
        self.DB_CURSOR.execute(sql_query)

    def write_turn(self, turn, position):
        turn_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        sql_query = f"""
        USE TicTacToe;
        INSERT INTO GameDetails (SessionID, TurnTime, Turn, Position)
        VALUES ('{self.SESSION_ID}', '{turn_time}', '{turn}', '{position}');
        """
        self.DB_CURSOR.execute(sql_query)

    def update_session(self, winner):
        game_ended = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        winner_status = f"{winner} is winner." if winner != "DRAW" else winner
        sql_query = f"""
        USE TicTacToe;
        UPDATE GameSession
        SET Status = '{winner_status}', GameEnded = '{game_ended}'
        WHERE SessionID = '{self.SESSION_ID}'
        """
        self.DB_CURSOR.execute(sql_query)

create_db(db_connection)
create_tables(db_connection)