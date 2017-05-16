import time
import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb
from db import *
from webapp2_extras import security

class User(webapp2_extras.appengine.auth.models.User):
  def set_password(self, raw_password):
    """Sets the password for the current user

    :param raw_password:
        The raw password which will be hashed and stored
    """
    self.password = security.generate_password_hash(raw_password, length=12)

  @classmethod
  def get_by_auth_token(cls, user_id, token, subject='auth'):
    """Returns a user object based on a user ID and token.

    :param user_id:
        The user_id of the requesting user.
    :param token:
        The token string to be verified.
    :returns:
        A tuple ``(User, timestamp)``, with a user object and
        the token timestamp, or ``(None, None)`` if both were not found.
    """
    token_key = cls.token_model.get_key(user_id, subject, token)
    user_key = ndb.Key(cls, user_id)
    # Use get_multi() to save a RPC call.
    valid_token, user = ndb.get_multi([token_key, user_key])
    if valid_token and user:
        timestamp = int(time.mktime(valid_token.created.timetuple()))
        return user, timestamp

    return None, None



class Profile(ndb.Model):
    profile_img = ndb.BlobProperty()
    profile_name = ndb.StringProperty()
    email = ndb.StringProperty()
    blood_type = ndb.StringProperty()
    
    age = ndb.IntegerProperty()
    address = ndb.StringProperty(indexed=False)
    city = ndb.StringProperty(indexed=False)
    zip_code = ndb.StringProperty(indexed=False)
    phone_number = ndb.StringProperty(indexed=False)
    events_going = ndb.IntegerProperty(indexed=False)

class Event(ndb.Model):
    event_title = ndb.StringProperty()
    event_description = ndb.StringProperty()
    address = ndb.StringProperty(indexed=False)
    city = ndb.StringProperty(indexed=False)
    zip_code = ndb.StringProperty(indexed=False)
    event_date = ndb.StringProperty() #look for a date property
    event_time = ndb.StringProperty() #look for a time property
    attendees = ndb.StringProperty()