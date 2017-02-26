from website import db

class User(object):

    def __init__(self, userinfo):
        self._id = None
        self._name = None
        self._password = None
        self._email = None
        self._face = None

        if userinfo:
            self._userid = str(userinfo['userid'])
            self._name = userinfo['username']
            self._password = userinfo['password']
            self._email = userinfo['email']
            self._face = userinfo['face']

    @classmethod
    def validate_and_login(cls, username, password):
        cursor = db.cursor()
        cursor.execute(
            'select id as userid, username, password, email, face \
            from user where username=%s and password=%s',
            (username, password,))
        fetch_res = cursor.fetchone()
        if fetch_res is not None:
            return cls(fetch_res)

    @classmethod
    def validate_and_register(cls, username, email, password):
        cursor = db.cursor()
        cursor.execute(
            'select id as userid from user where username=%s or email=%s',
            (username, email,))
        fetch_res = cursor.fetchone()
        if fetch_res is not None:
            return False
        User.save(username, email, password)
        return True

    @classmethod
    def get_user_by_user_id(cls, user_id):
        cursor = db.cursor()
        cursor.execute('select id as userid, username, password, email, face from user where id=%s',
                       (user_id,))
        fetch_res = cursor.fetchone()
        if fetch_res is not None:
            return cls(fetch_res)

    @classmethod
    def get_user_by_name(cls, username):
        cursor = db.cursor()
        cursor.execute(
            'select id as userid, username, password, email, face \
            from user where username=%s',
            (username, ))
        fetch_res = cursor.fetchone()
        if fetch_res is not None:
            return cls(fetch_res)

    @staticmethod
    def save(username, email, password, face=None):
        cursor = db.cursor()
        cursor.execute(
            'insert user (username, email, password, face) values (%s, %s, %s, %s)',
            (username, email, password, face,)
        )
        db.commit()
        return True

    @property
    def userid(self):
        return self._userid

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password

    @property
    def email(self):
        return self._email

    @property
    def face(self):
        return self._face

    def __str__(self):
        return 'userid: ' + self._userid + '\n' + \
            'username: ' + self._name + '\n' + \
            'email: ' + self._email + '\n'
