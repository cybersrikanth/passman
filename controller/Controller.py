from DB import DB

class Controller:
    db = None
    def dbQuery(self, query):
        if self.db==None:
            self.db = DB()
        self.db.query(query)
