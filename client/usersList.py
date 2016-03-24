import tornado.ioloop
import tornado.web
import tornado.ioloop
import tornado.httpclient
import loginFilter
import urllib

class UsersListHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		lista = ["user1","user2","user3"]
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield client.fetch("http://192.168.1.21:8888/users")	
		lista = str(response.body)
		lista=lista.replace('<br>','')
		lista=lista.replace('\'','')
		lista=lista[1:]
		listawyn = lista.split('\\n')
		self.render("strony/userslist.html",title="no cos mojego z pythona",nick=self.current_user,userslist=listawyn)
