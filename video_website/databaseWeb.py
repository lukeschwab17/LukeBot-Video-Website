import sqlite3
from sqlite3 import dbapi2
from cryptography.fernet import Fernet
import os

class Database:
    def __init__(self):
        # open encrypted database
        self.db_file_location = r"C:\Users\schwa\Desktop\discord_project\LukeBot\LukeBot\databases\database.db"

        with open(
            r"C:\Users\schwa\Desktop\discord_project\LukeBot\LukeBot\keys\filekey.key",
            "rb",
        ) as key_file:
            self.key = Fernet(key_file.read())

        with open(self.db_file_location, "rb") as db_file:
            original = db_file.read()

        decrypted = self.key.decrypt(original)

        with open(self.db_file_location, "wb") as dec_file:
            dec_file.write(decrypted)

        self.database = self.db_file_location
        self.conn = None
        self.curs = None

    def connect(self):
        self.conn = sqlite3.connect(self.database)
        self.curs = self.conn.cursor()

    def close(self):
        # opening the original file to encrypt
        with open(self.db_file_location, "rb") as file:
            original = file.read()

        # encrypting the file
        encrypted = self.key.encrypt(original)

        # opening the file in write mode and
        # writing the encrypted data
        with open(self.db_file_location, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        if self.conn:
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()
        self.close()

    # get video by video id ( also is video filename )
    @classmethod
    def get_video(cls, id: int):
        with cls() as db:
            db.curs.execute(
                "SELECT rowid, * FROM recording_session_compilations WHERE rowid = ?",
                (id,),
            )
            video_data = db.curs.fetchone()
            return video_data

    @classmethod
    def get_all_videos(cls, id: str):
        with cls() as db:
            visible_videos = set()

            db.curs.execute(f"SELECT rowid, * FROM recording_session_compilations")
            all_videodata = db.curs.fetchall()

            db.curs.execute(
                f"SELECT server_id FROM server_users WHERE member_id = ?", (id,)
            )
            user_data_tuples = db.curs.fetchall()

            user_data = set()
            for guild_tuple in user_data_tuples:
                user_data.add(guild_tuple[0])

            for video in all_videodata:
                if video[4] in user_data:
                    visible_videos.add(video)

            return visible_videos

    @classmethod
    def check_search(cls, user_input: str):
        with cls() as db:
            db.curs.execute("SELECT rowid, * FROM recording_session_compilations")
            all_videodata = db.curs.fetchall()

            filtered_videos = []
        for video_data in all_videodata:
            if (
                user_input.lower() in str(video_data[1]).lower()
            ):  # check if user id in discord id string
                filtered_videos.append(video_data)
            elif (
                user_input.lower() in str(video_data[3]).lower()
            ):  # check if search is in video name
                filtered_videos.append(video_data)
        return filtered_videos

    @classmethod
    def vote_update(cls, vote: str, video_id: int, discord_id: str):
        """Updates video votes as well as user's votes"""
        with cls() as db:
            db.curs.execute("""CREATE TABLE IF NOT EXISTS video_votes (
                                video_id int,
                                votes integer,
                                PRIMARY KEY (video_id)
                            )""")
            
            db.curs.execute("""CREATE TABLE IF NOT EXISTS user_votes (
                                discord_id text,
                                videos_ids text,
                                PRIMARY KEY (discord_id)
                            )""")
            
            db.curs.execute("SELECT * FROM video_votes WHERE video_id = ?", (video_id,))
            video_row = db.curs.fetchone()
            db.curs.execute("SELECT * FROM user_votes WHERE discord_id = ?", (discord_id,))
            user_row = db.curs.fetchone()
            
            # if rows don't exist for video voted on or user that voted, create them
            if not video_row:
                db.curs.execute("INSERT INTO video_votes (video_id, votes) VALUES (?, ?)", (video_id, 0))
                video_row = (video_id, 0)
            if not user_row:
                db.curs.execute("INSERT INTO user_votes (discord_id, videos_ids) VALUES (?, ?)", (discord_id, ""))
                user_row = (discord_id, "")

            # add or remove votes
            if vote == "add":
                new_votes = video_row[1] + 1 
                db.curs.execute("UPDATE video_votes SET votes = ? WHERE video_id = ?", (new_votes, video_id))
                video_row = (video_id, new_votes)
            elif vote == "remove":
                new_votes = max(0, video_row[1] - 1)
                db.curs.execute("UPDATE video_votes SET votes = ? WHERE video_id = ?", (new_votes, video_id))
                video_row = (video_id, new_votes)

            if cls.check_votes(video_id, new_votes):
                print("Video deleted.")

    @classmethod
    def check_votes(cls, video_id: int, votes: int) -> bool:
        """Carries out video deletion if necessary
        
        returns boolean value depending on video deleted or not
        """
        with cls() as db:
            db.curs.execute("SELECT guild_id, user_ids FROM recording_session_compilations WHERE rowid = ?", (video_id,))
            video_data = db.curs.fetchone()

            video_guild = video_data[0]
            guild_size = len(str(video_data[1]).split()) # video_data[1] is string of user id's in guild seperated by spaces

            if votes >= (guild_size / 2):
                cls.delete_video(video_id)
                return True
            
            return False
                
    @classmethod
    def delete_video(cls, video_int: int):
        """Deletes video file and database row"""
        with cls() as db:
            db.curs.execute("DELETE FROM recording_session_compilations WHERE rowid = ?", (video_int,))
            try:
                os.remove(f'static/videos/{video_int}.mp4') # make sure this is right filepath before running
                print("Video Deletion Success")
            except OSError:
                print("Video deletion failed, specified file not found")
