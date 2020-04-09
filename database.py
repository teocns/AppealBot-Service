import pymysql
import pymysql.cursors



class Database:
    
    db = None
    
    @staticmethod
    def instance():
        if Database.db is None:
            Database.db = pymysql.connect(host="localhost", user="root", passwd="", db="recap", use_unicode=True, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            Database.db.autocommit(True)
            Database.db.ping(True)
        return Database.db
        

