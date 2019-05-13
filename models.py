from smartninja_nosql.odm import Model

class User(Model):
    def __init__(self, email, **kwargs):
        self.email = email

        super().__init__(**kwargs)
