

import datetime
import sys

import contextlib
import sqlalchemy
# import sqlalchemy.ext
import sqlalchemy.ext.declarative
import sqlalchemy.dialects.mysql
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker


conn_str = "mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8mb4"
OK = 10
Base = sqlalchemy.ext.declarative.declarative_base()


class Test(Base):
    __tablename__ = 'test1'
    mysql_charset = "utf8mb4"

    s = sqlalchemy.Column(sqlalchemy.String(32), primary_key=True)
    i = sqlalchemy.Column(sqlalchemy.INT)  # 2020/3/31 客户端标识
    i2 = sqlalchemy.Column(sqlalchemy.INT)
    create_time = sqlalchemy.Column(sqlalchemy.DATETIME, default=datetime.datetime.now())


class DataBase(object):
    def __init__(self):
        self.engine = sqlalchemy.create_engine(
            conn_str,
            # echo=True,
            pool_recycle=3600
        )
        self.Session = sessionmaker(self.engine)
        try:
            self.create_tables()
        except Exception as e:
            print("database initialize failed")
            print("Exception: {}".format(e))
            sys.exit(-1)
        else:
            # 创建数据库表成功，继续往下执行
            pass

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def destroy_session(self):
        self.engine.dispose()

    @contextlib.contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            print("exception occurs: {}, {}".format(type(e), e))
            if type(e) is sqlalchemy.exc.IntegrityError:
                ecode = e.orig.args[0]
                if ecode == 1062:  # Duplicate key
                    raise Exception
                else:
                    session.rollback()
                    print("> session commit failed 1, rollback")
                    raise Exception
            else:
                session.rollback()
                print("> session commit failed 2, rollback")
                raise Exception
        finally:
            session.close()


db = DataBase()
