import tornado.ioloop
import tornado.web
import tornado.ioloop
import tornado.httpclient
import loginFilter
import urllib

class LogoutHandler(loginFilter.LoginFilter):
	def get(self):
		self.clear_cookie("user")
		self.redirect("/")	

class LoginHandler(loginFilter.LoginFilter):
	nick = ""
	@tornado.gen.coroutine
	def post(self):
		if(len(self.get_argument("nick"))>0 and len(self.get_argument("passwd"))):
			post_data = { 'pass': str(self.get_argument("passwd")) }
			body = urllib.parse.urlencode(post_data)
			client = tornado.httpclient.AsyncHTTPClient()
			tmpnick=self.get_argument("nick")
			try:
				response = yield client.fetch("http://192.168.1.21:8888/login/"+tmpnick,method='POST',body=body)	
				self.set_secure_cookie("user", self.get_argument("nick"))
				self.redirect("/")	
			except Exception as e:
			#	self.write(str(e))
#				self.render("strony/login.html",title="login",nick=self.nick,error="bledne dane")
				self.render("strony/login.html",title="login",nick=self.nick,error=str(e))
			#	self.write("blada zlapany")
#			self.nick=self.get_argument("nick")
#			nick=""
		else:
			self.render("strony/login.html",title="login",nick=self.nick,error="")
	def get(self):
		self.render("strony/login.html",title="login",nick=self.nick,error="")

