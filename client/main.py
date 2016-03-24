import tornado.ioloop
import tornado.web
import tornado.ioloop
import tornado.httpclient
import loginFilter
import urllib

class MainHandler(loginFilter.LoginFilter):
	def get(self):
		self.render("strony/base.html",title="no cos mojego z pythona",nick=self.current_user)
#		self.write("Hello, world!")
