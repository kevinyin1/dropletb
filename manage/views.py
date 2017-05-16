from manage import *
from db.models import *
from google.appengine.api import users
from __init__ import *
import webapp2, jinja2
from google.appengine.ext import ndb


class MainHandler(AdminBaseHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {}
        if user:
            self.redirect('/admin/overview')
            # greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
            #     nickname, logout_url)
        else:
            template_values = {
                'login_url': users.create_login_url('/admin')
            }
            self.redirect(template_values['login_url'])
        #     greeting = '<a href="{}">Sign in</a>'.format(login_url)
        #
        # self.response.write(
        #     '<html><body>{}</body></html>'.format(greeting))

class LogoutHandler(AdminBaseHandler):

    def get(self):
        template_values = {}
        if users.get_current_user():
            self.redirect(users.create_logout_url('/admin'))
        else:
            self.redirect('/admin')


class AdminHandler(AdminBaseHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {}
        if user:
            if users.is_current_user_admin():
                self._serve_page()
            else:
                self.response.write('You are not an administrator.')
        else:
            self.response.write('You are not logged in.')


    def attendee_keys(self, attendees):
        if ',' not in attendees:
            return attendees
        elif attendees == None:
            return attendees
        else:
            return attendees.split(',')
            
    def get_user_profile(self, user_keys):
        user_profiles = []
        users = Profile.query().fetch()
        for user in users:
            for user_key in user_keys:
                if user.key.id() == user_key:
                    user_profiles.append(user)
        return user_profiles            
            
    def get_users_attending(self, event, attendees):
        if attendees == None:
            return [event.key.id(), 'No Attendees']
        else:
            return [event.key.id(), self.get_user_profile(attendees)]
        
#    def _serve_page(self):
#        events = Event.query().fetch()
#        users = Profile.query().fetch()
#        all_attendees = []
#        for event in events:
#            all_attendees.append(self.get_users_attending(event, self.attendee_keys(event.attendees)))
#                        
#        template_values = {
#            'results': events,
#            'users': users,
#            'attendees': all_attendees
#        }
#        self.render_template('admin-overview.html',template_values)



    def _serve_page(self):
            events = Event.query().fetch()
            users = Profile.query().fetch()
            total_data = []
            profile_list = []
            myList = []
            for event in events:
                total_data.append((event.key.id()))
                if event.attendees != None:
                    data = event.attendees.split(',')
                    for attendee_key in data:
                        for profile in users:
                            if attendee_key == str(profile.key.id()):
                                profile_list.append(profile)
                                
                    total_data.append(profile_list)
                    profile_list = []
                myList.append(total_data)
                total_data = []

            template_values = {
                'results': events,
                'users': users,
                'attendees': myList
            }
            self.render_template('admin-overview.html',template_values)

class CreateHandler(AdminBaseHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {}
        if user:
            if users.is_current_user_admin():
                self._serve_page()
            else:
                self.response.write('You are not an administrator.')
        else:
            self.response.write('You are not logged in.')

    def post(self):
        event = Event(event_title = self.request.get('event-title'),
            event_description = self.request.get('event-description'),
            address = self.request.get('event-address'),
            city = self.request.get('event-city'),
            zip_code = self.request.get('event-zip_code'),
            event_date = self.request.get('event-date'),
            event_time = self.request.get('event-time'))
        event.put()
        self.redirect(self.uri_for("create"))
        self._serve_page()

    def _serve_page(self):
            query_event = Event.query()
            results = query_event.fetch()
            template_values = {
                'results': results,
                'users': Profile.query().fetch()
            }
            self.render_template('create.html',template_values)


app = webapp2.WSGIApplication([
    webapp2.Route('/admin', MainHandler),
    webapp2.Route('/admin/overview', AdminHandler),
    webapp2.Route('/admin/logout', LogoutHandler),
    webapp2.Route('/admin/create', CreateHandler, name="create")
], debug=True)
