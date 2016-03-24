import tornado.ioloop
import tornado.web
import tornado.ioloop
import tornado.httpclient

class LoginFilter(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")

