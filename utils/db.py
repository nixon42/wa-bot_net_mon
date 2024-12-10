import sqlite3
from typing import Optional, List
from .model import LocalTable


class Database:
    def __init__(self, db_file: str, table: str):
        self.db_file = db_file
        self.db = None
        self.table = table

    def connect(self):
        try:
            self.db = sqlite3.connect(self.db_file)
            self.create_table()
            return self.db
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def close(self):
        if self.db:
            self.db.close()

    def create_table(self):
        try:
            cursor = self.db.cursor()
            query = f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
                network_name TEXT,
                client_name TEXT,
                ip_address TEXT,
                status TEXT,
                last_down_time TEXT,
                last_up_time TEXT
            )
            """
            cursor.execute(query)
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert(self, data: LocalTable) -> Optional[int]:
        try:
            cursor = self.db.cursor()
            data_dict = data.to_dict()
            columns = ', '.join(data_dict.keys())
            values = ', '.join(['?' for _ in data_dict])
            query = f"INSERT INTO {self.table} ({columns}) VALUES ({values})"
            cursor.execute(query, list(data_dict.values()))
            self.db.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            return None

    def update_field_by_ip(self, ip_address: str, field: str, value: Optional[str]) -> bool:
        try:
            cursor = self.db.cursor()
            query = f"UPDATE {self.table} SET {field} = ? WHERE ip_address = ?"
            cursor.execute(query, (value, ip_address))
            self.db.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating {field}: {e}")
            return False

    def fetch_by_ip(self, ip_address: str) -> Optional[LocalTable]:
        try:
            cursor = self.db.cursor()
            query = f"SELECT * FROM {self.table} WHERE ip_address = ?"
            cursor.execute(query, (ip_address,))
            row = cursor.fetchone()
            if row:
                return LocalTable(*row)
            return None
        except sqlite3.Error as e:
            print(f"Error fetching data by IP: {e}")
            return None

    def fetch_all(self, limit: int = None, offset: int = 0) -> List[LocalTable]:
        try:
            cursor = self.db.cursor()
            query = f"SELECT * FROM {self.table}"
            if limit:
                query += f" LIMIT {limit} OFFSET {offset}"
            cursor.execute(query)
            rows = cursor.fetchall()
            return [LocalTable(*row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching all data: {e}")
            return []

    def delete_by_ip(self, ip_address: str) -> bool:
        try:
            cursor = self.db.cursor()
            query = f"DELETE FROM {self.table} WHERE ip_address = ?"
            cursor.execute(query, (ip_address,))
            self.db.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting record by IP: {e}")
            return False

    def fetch_by_network_name(self, network_name: str) -> list[LocalTable]:
        """
        Fetch all records with the specified network name.

        Args:
            network_name (str): The name of the network to search for.

        Returns:
            list[LocalTable]: A list of LocalTable objects representing the records.
        """
        try:
            cursor = self.db.cursor()
            query = f"SELECT * FROM {self.table} WHERE network_name = ?"
            cursor.execute(query, (network_name,))
            rows = cursor.fetchall()
            return [LocalTable(*row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching records by network name: {e}")
            return []
