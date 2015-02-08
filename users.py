from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty()

    @classmethod
    def get_by_user(cls, user):
        return cls.get_by_id(user.user_id())

    @classmethod
    def create_or_update(cls, user, username):
        instance = cls(username=username, id=user.user_id())
        instance.put()
        return instance

    def delete(self):
        self.key.delete()