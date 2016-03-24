import tornado.ioloop
import tornado.web
import tornado.ioloop
import tornado.httpclient
import http.client
import loginFilter
import urllib

class UserPageHandler(loginFilter.LoginFilter):
#	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,nickurl):
		#if nick != self.current_user:
		#	serf.redirect('/')
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield client.fetch("http://192.168.1.21:8888/user/"+nickurl)	
		lista = str(response.body)
		lista=lista.replace('<br>','')
		lista=lista.replace('\'','')
		lista=lista[1:]
		listawyn = lista.split('\\t')
		owner=1
		if nickurl != self.current_user.decode():
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
				owner=1
			except Exception as e:
				owner=0
#				self.write(e)o	
			finally:
				self.render("strony/userPage.html",title="no cos mojego z pythona",nick=self.current_user,danen=listawyn,choseuser=nickurl,owner=owner)
		else:
			self.render("strony/userPage.html",title="no cos mojego z pythona",nick=self.current_user,danen=listawyn,choseuser=nickurl,owner=owner)

class DeleteUserHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,nickurl):
		if nickurl != self.current_user.decode():
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			except Exception as e:
				self.redirect("/")
		self.render("strony/deleteUser.html",title="no cos mojego z pythona",nick=self.current_user,danen=nickurl,choseuser=nickurl)

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,nick):
		if self.get_argument("option")!="yes":
                                self.redirect("/")
		if nick != self.current_user.decode():
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			except Exception as e:
				self.redirect("/")
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/user/"+nick,method='DELETE')	
		except Exception as e:
			self.redirect("/")
		if nick == self.current_user.decode():
			self.redirect("/logout")

class UserChangeDataHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,nickurl):
		if nickurl != self.current_user:
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			except Exception as e:
				self.redirect("/")
			try:
				response = yield client.fetch("http://192.168.1.21:8888/user/"+str(nickurl))
			except Exception as e:
				self.redirect("/")
			lista = str(response.body)
			lista=lista.replace('<br>','')
			lista=lista.replace('\'','')
			lista=lista[1:]
			listawyn = lista.split('\\t')
		self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=listawyn[0],oldname=listawyn[1],oldname2=listawyn[2],oldmail=listawyn[3])

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,nick):
		if nick != self.current_user:
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			except Exception as e:
				self.redirect("/")
				return
		if ( len(self.get_argument("nick"))<1 ) or ( len(self.get_argument("name"))<1) or ( len(self.get_argument("name2"))<1) or ( len(self.get_argument("mail"))<1) or ( len(self.get_argument("pass"))<1):
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=self.get_argument("nick"),oldname=self.get_argument("name"),oldname2=self.get_argument("name2"),oldmail=self.get_argument("mail"))
			return
		post_data = { 'pass': str(self.get_argument("pass")) }
		body = urllib.parse.urlencode(post_data)
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/login/"+nick,method='POST',body=body)
		except Exception as e:
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=self.get_argument("nick"),oldname=self.get_argument("name"),oldname2=self.get_argument("name2"),oldmail=self.get_argument("mail"))
		post_data_final = {'imie': str(self.get_argument("name")),'nazwisko': str(self.get_argument("name2")),'email': str(self.get_argument("mail")),'nick': str(self.get_argument("nick"))}
#		post_data_final = {'imie': "przykladowe imie"}
		body_final = urllib.parse.urlencode(post_data_final)
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
		        response = yield client.fetch("http://192.168.1.21:8888/user/"+nick,method='PUT',headers=headers,body=body_final)
	        	self.redirect("/user/"+self.get_argument("nick"))
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=self.get_argument("nick"),oldname=self.get_argument("name"),oldname2=self.get_argument("name2"),oldmail=self.get_argument("mail"))

class UserChangePassHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,nickurl):
		if nickurl != self.current_user:
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			except Exception as e:
				self.redirect("/")
		self.render("strony/userChangePass.html",title="no cos mojego z pythona",nick=self.current_user)

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,nick):
		if nick != self.current_user:
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			except Exception as e:
				self.redirect("/")
				return
		if ( len(self.get_argument("oldpass"))<1 ) or ( len(self.get_argument("newpass1"))<1) or ( len(self.get_argument("newpass2"))<1) or (self.get_argument("newpass1")!=self.get_argument("newpass2")):
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=self.get_argument("nick"),oldname=self.get_argument("name"),oldname2=self.get_argument("name2"),oldmail=self.get_argument("mail"))
			return
		post_data = { 'pass': str(self.get_argument("oldpass")) }
		body = urllib.parse.urlencode(post_data)
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/login/"+nick,method='POST',body=body)
		except Exception as e:
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=self.get_argument("nick"),oldname=self.get_argument("name"),oldname2=self.get_argument("name2"),oldmail=self.get_argument("mail"))
#		post_data_final = {'imie': str(self.get_argument("name")),'nazwisko': str(self.get_argument("name2")),'email': str(self.get_argument("mail")),'nick': str(self.get_argument("nick"))}
		post_data = { 'pass': str(self.get_argument("passnew1")) }
#		post_data_final = {'imie': "przykladowe imie"}
		body_final = urllib.parse.urlencode(post_data_final)
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
		        response = yield client.fetch("http://192.168.1.21:8888/user/"+nick,method='PUT',headers=headers,body=body_final)
	        	self.redirect("/user/"+self.get_argument("nick"))
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=self.get_argument("nick"),oldname=self.get_argument("name"),oldname2=self.get_argument("name2"),oldmail=self.get_argument("mail"))

class UserRegisterHandler(loginFilter.LoginFilter):
	@tornado.gen.coroutine
	def get(self):
		self.render("strony/userRegister.html",title="no cos mojego z pythona",nick=self.current_user,nnick="",nname="",nname2="",nmail="")

	@tornado.gen.coroutine
	def post(self):
		if ( len(self.get_argument("nick"))<1 ) or ( len(self.get_argument("name"))<1) or ( len(self.get_argument("name2"))<1) or ( len(self.get_argument("mail"))<1) or ( len(self.get_argument("pass1"))<1) or (len(self.get_argument("pass2"))<1) or (self.get_argument("pass1")!=self.get_argument("pass2")):
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,nnick=self.get_argument("nick"),nname=self.get_argument("name"),nname2=self.get_argument("name2"),nmail=self.get_argument("mail"))
			return
		post_data = {'nick': str(self.get_argument("nick"))}
#		post_data_final = {'imie': "przykladowe imie"}
		body = urllib.parse.urlencode(post_data)
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
		        response = yield client.fetch("http://192.168.1.21:8888/users",method='POST',headers=headers,body=body)
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=self.get_argument("nick"),oldname=self.get_argument("name"),oldname2=self.get_argument("name2"),oldmail=self.get_argument("mail"))
			return
		post_data_final = {'imie': str(self.get_argument("name")),'nazwisko': str(self.get_argument("name2")),'email': str(self.get_argument("mail")),'nick': str(self.get_argument("nick")), 'pass': str(self.get_argument("pass1"))}
#		post_data_final = {'imie': "przykladowe imie"}
		body_final = urllib.parse.urlencode(post_data_final)
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
		        response = yield client.fetch("http://192.168.1.21:8888/user/"+self.get_argument("nick"),method='PUT',headers=headers,body=body_final)
	        	self.redirect("/")
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.render("strony/userChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldnick=self.get_argument("nick"),oldname=self.get_argument("name"),oldname2=self.get_argument("name2"),oldmail=self.get_argument("mail"))
