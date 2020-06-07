import sqlite3


# Create table
# c.execute('drop table if exists User')
# c.execute('drop table if exists Password')
# c.execute("CREATE TABLE if not exists User (id INTEGER primary key AUTOINCREMENT, name text NOT NULL, password text NOT NUll, updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)")
# c.execute("CREATE TABLE if not exists Password (id INTEGER primary key AUTOINCREMENT, user int NOT NULL, password text NOT NULL, updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, FOREIGN KEY(user) REFERENCES User(id))")

class DB:
    def connect(self):
        self.conn = sqlite3.connect('passman.db')
        self.cursor = self.conn.cursor()
        # self.cursor.execute('drop table if exists Password')
        self.cursor.execute("CREATE TABLE if not exists User (id INTEGER primary key AUTOINCREMENT, name text NOT NULL unique, password text NOT NUll, updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)")
        self.cursor.execute("CREATE TABLE if not exists Password (id INTEGER primary key AUTOINCREMENT, user int NOT NULL, website text NOT NULL, username text NOT NULL, password text NOT NULL, updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, FOREIGN KEY(user) REFERENCES User(id) on Delete cascade, UNIQUE(website, username))")
        
    def query(self, query, params):
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            self.conn.commit()
            return {"status": True, "rows" : rows, "message": None}
        except sqlite3.IntegrityError:
            return {"status":False, "message": "Duplicate Entry"}
        except:
            return {"status": False, "message" : "something went wrong in query"}

    def close(self):
        self.conn.close()
