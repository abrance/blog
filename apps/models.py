import datetime
import sys

import contextlib
import sqlalchemy
# import sqlalchemy.ext
import sqlalchemy.ext.declarative
import sqlalchemy.dialects.mysql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from apps.log import logger
from apps.utils import worker

conn_str = "mysql+pymysql://blog:111111@127.0.0.1:3306/blog?charset=utf8mb4"
OK = 10
Base = sqlalchemy.ext.declarative.declarative_base()


# class Test(Base):
#     __tablename__ = 'test1'
#     mysql_charset = "utf8mb4"
#
#     s = sqlalchemy.Column(sqlalchemy.String(255)(32), primary_key=True)
#     i = sqlalchemy.Column(sqlalchemy.INT)  # 2020/3/31 客户端标识
#     i2 = sqlalchemy.Column(sqlalchemy.INT)
#     create_time = sqlalchemy.Column(sqlalchemy.DATETIME, default=datetime.datetime.now())


class Primary(Base):
    __tablename__ = 'Person'
    mysql_charset = 'utf8mb4'

    # 注册人id，唯一主键
    primary_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    # 使用字母较好，因为不用作数字运算；暂时不用作唯一标识
    phone_number = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    # 姓名
    name = sqlalchemy.Column(sqlalchemy.String(255))
    # 昵称
    nickname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.BINARY(32), nullable=False)
    # 身份证号 18位
    id = sqlalchemy.Column(sqlalchemy.String(255))
    # 创建账号时间
    create_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now())
    mail = sqlalchemy.Column(sqlalchemy.String(255))
    is_deleted = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=0, nullable=False)


class Title(Base):
    __tablename__ = 'Title'
    mysql_charset = 'utf8mb4'

    title_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    # 副标题可空
    subtitle = sqlalchemy.Column(sqlalchemy.String(255))
    primary_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    nickname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    activity = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now())
    last_modify_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now())


class Label(Base):
    __tablename__ = 'Label'
    mysql_charset = 'utf8mb4'

    label_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    label = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now())


class TitleLabel(Base):
    __tablename__ = 'TitleLabel'
    mysql_charset = 'utf8mb4'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    label_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    title_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now())


class Comment(Base):
    __tablename__ = 'Comment'
    mysql_charset = 'utf8mb4'
    # 评论的唯一id
    comment_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    title_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    # 发言人的信息
    primary_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    # 避免频繁查找，加入昵称
    nickname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    # text
    text = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    preference = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now())


class SecondComment(Base):
    __tablename__ = 'SecondComment'
    mysql_charset = 'utf8mb4'
    # 与一级留言表是彼此独立，但结构相似
    second_comment_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    comment_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    primary_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    nickname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    preference = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now())


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
        except IntegrityError as ie:
            ecode = ie.orig.args[0]
            if ecode == 1062:  # Duplicate key
                raise Exception
            else:
                session.rollback()
                print("> session commit failed 1, rollback")
                raise Exception
        except Exception as e:
            print("exception occurs: {}, {}".format(type(e), e))
            # if type(e) is sqlalchemy.exc.IntegrityError:
            #     ecode = e.orig.args[0]
            #     if ecode == 1062:  # Duplicate key
            #         raise Exception
            #     else:
            #         session.rollback()
            #         print("> session commit failed 1, rollback")
            #         raise Exception
            # else:
            #     session.rollback()
            #     print("> session commit failed 2, rollback")
            #     raise Exception
            session.rollback()
            print("> session commit failed 2, rollback")
            raise Exception
        finally:
            session.close()

    def register(self, phone_num, name, nickname, man_id, mail):
        """
        注册
        :return:
        """
        primary_id = worker.get_id()
        with self.session_scope() as session:
            row_p = Primary(primary_id=primary_id,
                            phone_number=phone_num, name=name, nickname=nickname, id=man_id, mail=mail)
            session.add(row_p)
            return True

    def freeze_account(self, primary_id):
        """
        冻结账户    给予冻结账户选项
        :return: 
        """
        with self.session_scope() as session:
            query_primary = session.query(Primary).filter(
                Primary.primary_id == primary_id, Primary.is_deleted == 0
            )
            row_primary = query_primary.first()
            if row_primary:
                row_primary.is_deleted = 1
                return True
            else:
                return False

    def close_account(self, primary_id):
        """
        注销账户    只有管理员可以销户
        :return:
        """
        with self.session_scope() as session:
            query_primary = session.query(Primary).filter(
                Primary.primary_id == primary_id, Primary.is_deleted == 0
            )
            row_primary = query_primary.first()
            if row_primary:
                session.delete(row_primary)
                return True
            else:
                return False

    def create_label(self, label):
        """
        创建标签
        :return:
        """
        with self.session_scope() as session:
            query_lab = session.query(Label).filter(
                Label.label == label
            )
            row_lab = query_lab.first()
            if row_lab:
                return False
            else:
                row_lab = Label(label=label)
                session.add(row_lab)
                return True

    def remove_label(self, label):
        """
        移除标签
        :return:
        """
        with self.session_scope() as session:
            query_lab = session.query(Label).filter(
                Label.label == label
            )
            row_lab = query_lab.first()
            if row_lab:
                session.delete(row_lab)
                return True
            else:
                return False

    def create_title(self, title, subtitle, primary_id, nickname, label_id_ls):
        """
        创建主题
        :return:
        """
        title_id = worker.get_id()
        with self.session_scope() as session:
            for label_id in label_id_ls:
                query_lab = session.query(Label).filter(
                    Label.label_id == label_id
                )
                if not query_lab.first():
                    return False
            else:
                now = datetime.datetime.now()
                row_t = Title(title_id=title_id, title=title, subtitle=subtitle,
                              primary_id=primary_id, nickname=nickname, create_time=now)
                session.add(row_t)

                for label_id in label_id_ls:
                    row_tl = TitleLabel(label_id=label_id, title_id=title_id, create_time=now)
                    session.add(row_tl)
                return True

    def remove_title(self, title_id):
        """
        删除主题
        :return:
        """
        with self.session_scope() as session:
            query_title = session.query(Title).filter(
                Title.title_id == title_id
            )
            row_title = query_title.first()
            if row_title:
                session.delete(row_title)

                # remove label title
                query_tl = session.query(TitleLabel).filter(
                    TitleLabel.title_id == title_id
                )
                query_tl.delete()
                return True
            else:
                return False

    def add_labels_to_title(self, title_id, label_id_ls):
        """
        新增label到title
        :return:
        """
        with self.session_scope() as session:
            query_tl = session.query(TitleLabel).filter(
                TitleLabel.title_id == title_id
            )

            old_label_ls = [row_tl.label_id for row_tl in query_tl.all()]
            for label_id in label_id_ls:
                if label_id in old_label_ls:
                    continue
                else:
                    row_tl = TitleLabel(label_id=label_id, title_id=title_id)
                    session.add(row_tl)
            return True

    def remove_label_to_title(self, title_id, label_id):
        """
        删除title的label
        :return:
        """
        with self.session_scope() as session:
            query_tl = session.query(TitleLabel).filter(
                TitleLabel.title_id == title_id, TitleLabel.label_id == label_id
            )
            row_tl = query_tl.first()
            if row_tl:
                session.delete(row_tl)
                return True
            else:
                return False

    def create_comment(self, title_id, primary_id, nickname, text):
        """
        创建留言
        :return:
        """
        comment_id = worker.get_id()
        with self.session_scope() as session:
            row_c = Comment(comment_id=comment_id, title_id=title_id, primary_id=primary_id,
                            nickname=nickname, text=text)
            session.add(row_c)
            return True

    def remove_comment(self, comment_id):
        """
        删除留言， 管理员权限
        :return:
        """
        with self.session_scope() as session:
            query_c = session.query(Comment).filter(
                Comment.comment_id == comment_id
            )
            row_c = query_c.first()
            if row_c:
                session.delete(row_c)
                return True
            else:
                return False

    def create_second_comment(self, comment_id, primary_id, nickname, text):
        """
        创建二级留言
        :return:
        """
        second_comment_id = worker.get_id()
        with self.session_scope() as session:
            query_c = session.query(Comment).filter(
                Comment.comment_id == comment_id
            )
            row_c = query_c.first()
            if row_c:
                row_sc = SecondComment(second_comment_id=second_comment_id, comment_id=comment_id,
                                       primary_id=primary_id, nickname=nickname, text=text)
                session.add(row_sc)
                return True
            else:
                return False

    def remove_second_comment(self, second_comment_id):
        """
        删除二级留言
        :return:
        """
        with self.session_scope() as session:
            query_sc = session.query(SecondComment).filter(
                SecondComment.second_comment_id == second_comment_id
            )
            row_sc = query_sc.first()
            if row_sc:
                session.delete(row_sc)
                return True
            else:
                return False

    # -------------------------------------------------
    
    def logging(self, username, _password):
        # db保存的是binary(16)

        bin_password = bytes(_password, encoding='utf-8')
        logger.info('1111 {} {}'.format(username, bin_password))
        with self.session_scope() as session:
            query_primary = session.query(Primary).filter(
                Primary.nickname == username, Primary.password == bin_password, Primary.is_deleted == 0
            )
            row_p = query_primary.first()

            if row_p:
                logger.info('{} {}'.format(row_p.password, type(row_p.password)))
                pass
            else:
                if isinstance(username, str) and len(username) == 18 and username.isdigit():
                    # 用身份证号也可以
                    query_primary = session.query(Primary).filter(
                        Primary.id == username, Primary.password == bin_password, Primary.is_deleted == 0
                    )
                    row_p = query_primary.first()
                    if row_p:
                        pass
                    else:
                        logger.info('username or password wrong')
                        return False
                elif isinstance(username, str) and len(username) == 11 and username.isdigit():
                    query_primary = session.query(Primary).filter(
                        Primary.phone_number == username, Primary.password == bin_password, Primary.is_deleted == 0
                    )
                    row_p = query_primary.first()
                    if row_p:
                        pass
                    else:
                        logger.info('username or password wrong')
                        return False
                else:
                    logger.info('username or password wrong')
                    return False
            info = {
                'nickname': row_p.nickname,
                'primary_id': str(row_p.primary_id),
                'phone_number': row_p.phone_number,
                'name': row_p.name,
                'create_time': row_p.create_time,
                'mail': row_p.mail,
            }
            return info

    def list_title(self, page, limit=30, primary_id=None, create_time=None, title_val_ls=None, subtitle_val_ls=None):
        if primary_id or create_time or title_val_ls or subtitle_val_ls:
            # TODO 搜索功能
            pass
        else:
            with self.session_scope() as session:
                query_title = session.query(Title).order_by(Title.create_time.desc()).\
                    offset(limit * (page - 1)).limit(limit)
                row_t = query_title.first()
                if row_t:
                    query_t_all = query_title.all()
                    title_id_ls = [row_t.title_id for row_t in query_t_all]
                    # TODO check in_ set
                    query_tl = session.query(TitleLabel).filter(
                        TitleLabel.title_id.in_(title_id_ls)
                    )
                    query_tl_all = query_tl.all()
                    # title_id: label_ids
                    title_dc = {}
                    # id的set
                    label_set = set()
                    logger.info(len(query_tl_all))
                    for row_tl in query_tl_all:
                        # label_set 保存包含的所有label_id，避免反复查找
                        label_set.add(row_tl.label_id)
                        title = title_dc.get(row_tl.title_id)
                        if title:
                            if row_tl.label_id in title:
                                continue
                            else:
                                title.add(row_tl.label_id)
                        else:
                            title_dc[row_tl.title_id] = {row_tl.label_id}

                    # 替换 label_id 为 label
                    query_l = session.query(Label.label, Label.label_id).filter(
                        Label.label_id.in_(label_set)
                    )
                    query_l_all = query_l.all()
                    label_dc = {label_id: label for label, label_id in query_l_all}
                    new_title_dc = {}
                    for title_id, t in title_dc.items():
                        for _t in t:
                            if _t in label_dc.keys():
                                if new_title_dc.get(title_id):
                                    new_title_dc[title_id].add((_t, label_dc[_t]))
                                else:
                                    new_title_dc[title_id] = {(_t, label_dc[_t])}
                            else:
                                # 这是意料之外的错误
                                logger.error('unexpect except')
                                return False

                    title_dc = new_title_dc
                    # 装配数据
                    ls = [{
                        # 为了避免js大整数精度丢失，查阅资料后解决方案都很不方便，所以在服务器中做字符串转化
                        'title_id': str(row_t.title_id),
                        'title': row_t.title,
                        'primary_id': str(row_t.primary_id),
                        'nickname': row_t.nickname,
                        'create_time': row_t.create_time,
                        'last_modify_time': row_t.last_modify_time,
                        'label_ls': list(title_dc.get(row_t.title_id))
                    } for row_t in query_t_all]
                    return ls
                else:
                    return []

    def list_label(self):
        with self.session_scope() as session:
            query_label = session.query(Label)
            ret_ls = []
            for row_label in query_label.all():
                ret_ls.append({'id': row_label.label_id, 'text': row_label.label})
            return ret_ls

    def inquiry_title(self, title_id):
        # TODO 每个title的权重
        with self.session_scope() as session:
            query_title = session.query(Title).filter(
                Title.title_id == title_id
            )
            row_title = query_title.first()
            if row_title:
                query_comment = session.query(Comment).filter(
                    Comment.title_id == title_id
                )
                row_comment = query_comment.first()
                comment_ls = []
                if row_comment:
                    for row_comment in query_comment.all():
                        comment_dc = {
                            'comment_id': str(row_comment.comment_id),
                            'primary_id': str(row_comment.primary_id),
                            'nickname': row_comment.nickname,
                            'text': row_comment.text,
                            'create_time': row_comment.create_time
                        }
                        comment_ls.append(comment_dc)

                # 装配数据
                ret_dc = {
                    'title': row_title.title,
                    'title_id': str(row_title.title_id),
                    'subtitle': row_title.subtitle,
                    'primary_id': str(row_title.primary_id),
                    'nickname': row_title.nickname,
                    'create_time': row_title.create_time,
                    'last_modify_time': row_title.last_modify_time,
                    'comment_ls': comment_ls
                }
                return ret_dc
            else:
                logger.error('title no found')
                return False

    def inquiry_comment(self, comment_id, page=1, limit=20):
        with self.session_scope() as session:
            query_c = session.query(Comment).filter(
                Comment.comment_id == comment_id
            )
            row_c = query_c.first()
            if row_c:
                query_sc = session.query(SecondComment).filter(
                    SecondComment.comment_id == comment_id
                )
                row_sc = query_sc.first()
                second_comment_ls = []
                if row_sc:
                    for row_sc in query_sc.all():
                        sc_dc = {
                            'second_comment_id': str(row_sc.second_comment_id),
                            'primary_id': str(row_sc.primary_id),
                            'nickname': row_sc.nickname,
                            'text': row_sc.text,
                            'create_time': row_sc.create_time
                        }
                        second_comment_ls.append(sc_dc)

                ret_dc = {
                    'primary_id': str(row_c.primary_id),
                    'nickname': row_c.nickname,
                    'text': row_c.text,
                    'create_time': row_c.create_time,
                    'second_comment': second_comment_ls
                }
                return ret_dc
            else:
                logger.error('comment no found')
                return False


db = DataBase()
