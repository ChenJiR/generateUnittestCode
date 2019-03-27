import unittest
import redis
import pymysql
import unittestMain.config as config


class tool():
    __env = 'dev'

    __db = None
    __db_name = None
    __redis = None
    __redis_db = 0

    __token = None

    def setEnv(self, env):
        self.__env = env

    def setDbName(self, db_name):
        self.__db_name = db_name

    def setRedisDb(self, redis_db):
        self.__redis_db = redis_db

    def __DB_drive(self, db_name):
        if self.__db_name is None and db_name is None:
            raise RuntimeError('数据库名称未设置')

        db_config = config.get_db_config(self.__env)

        self.__db = pymysql.connect(
            db_config['host'],
            db_config['username'],
            db_config['password'],
            db_name if db_name is not None else self.__db_name
        )

    def DB_select(self, sql, db_name=None):
        self.__DB_drive(db_name)

        cursor = self.__db.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except:
            print("Error: unable to fetch data")
            self.__db.close()
            exit()

    def DB_execute(self, sql, db_name=None):
        self.__DB_drive(db_name)

        cursor = self.__db.cursor()
        try:
            cursor.execute(sql)
            self.__db.commit()
        except:
            print("Error: unable to execute data")
            self.__db.rollback()
            self.__db.close()
            exit()

    def __redis_drive(self, db=None):
        redis_config = config.get_redis_config(self.__env)
        pool = redis.ConnectionPool(
            host=redis_config['hostname'],
            port=redis_config['port'],
            password=redis_config['password'],
            decode_responses=True,
            db=db if db is not None else self.__redis_db
        )
        self.__redis = redis.Redis(connection_pool=pool)

    def redis_set(self, key, value, db=None):
        self.__redis_drive(db)
        return self.__redis.set(key, value)

    def redis_get(self, key, db=None):
        self.__redis_drive(db)
        return self.__redis.get(key)

    def getRedis(self, db=None):
        self.__redis_drive(db)
        return self.__redis

    def get_token(self):
        pass

    def get_url(self, modules, api):
        host = config.get_host(modules, self.__env)
        return host + api
