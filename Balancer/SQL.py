from pathlib import Path
import json
import logging
import os
import shutil
import sqlite3
import time
import uuid
import datetime

class SQL:
    c = None
    conn = None
    log = logging.getLogger('Balancer').getChild(__name__)


    def __init__(self):
        dbFile = Path('party.db')
        if not dbFile.is_file():
            self.initalize()
        if self.conn is None:
            self.log.info("Attempt to connect to SQL local db")
            self.conn = sqlite3.connect(str(dbFile))
            self.conn.row_factory = self.dict_factory
            self.c = self.conn.cursor()
            # self.c.arraysize = 300
            self.log.info("Connected")


    def commit(self):
        self.conn.commit()


    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def initalize(self):
        # Init the connection

        self.conn = sqlite3.connect('party.db')
        self.conn.row_factory = self.dict_factory
        self.c = self.conn.cursor()

        # Add tables as needed
        self.log.info("Create players table")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS players
            (
                player_id TEXT UNIQUE ON CONFLICT FAIL NOT NULL,
                name TEXT UNIQUE,
                character_name TEXT
            )
            """)
        self.c.execute("""
            INSERT INTO players 
            (player_id,name,character_name)
            VALUES
            (?,?,?)
            """,(str(uuid.uuid1()),"party","party"))

        self.log.info("Create transactions table")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS transactions
            (
                player_id TEXT NOT NULL,
                amount NUMERIC,
                datetime TEXT,
                name TEXT
            )
            """)

        self.conn.commit()


    def get_players(self):
        self.c.execute("SELECT * FROM players")
        return self.c.fetchall()


    def get_player(self, player_id):
        self.c.execute("SELECT * FROM players WHERE player_id=?",(player_id,))
        return self.c.fetchone()


    def get_player_id(self, name):
        self.c.execute("SELECT * FROM players WHERE name=?",(name,))
        return self.c.fetchone()['player_id']


    def add_player(self, name, character_name):
        sqlCmd = f"""
            INSERT OR FAIL INTO players 
            (player_id,name,character_name)
            VALUES 
            (?,?,?)
        """
        self.c.execute(sqlCmd,(str(uuid.uuid1()),name,character_name))
        self.conn.commit()


    def get_balances(self):
        self.c.execute("SELECT * FROM transactions")
        transactions = self.c.fetchall()
        players = self.get_players()
        ret_val = {}
        for player in players:
            ret_val[player['player_id']] = 0

        for transaction in transactions:
            ret_val[transaction['player_id']] += transaction['amount']
        return ret_val


    def add_transaction(self, player_id, name, amount):

        sqlCmd = f"""
            INSERT OR FAIL INTO transactions 
            (player_id,name,amount,datetime)
            VALUES 
            (?,?,?,?)
        """
        self.c.execute(sqlCmd,
            (player_id,
            name,
            amount,
            datetime.datetime.now(),)
            )
        self.conn.commit()


