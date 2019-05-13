from smartninja_nosql.odm import Model

class User(Model):
    def __init__(self, email, password, secret_number, session_token, **kwargs):
        self.email = email
        self.password = password
        self.secret_number = secret_number
        self.session_token = session_token

        super().__init__(**kwargs)
