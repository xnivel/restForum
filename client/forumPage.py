import tornado.ioloop
import tornado.web
import tornado.ioloop
import tornado.httpclient
import http.client
import loginFilter
import urllib

class ForumPageHandler(loginFilter.LoginFilter):
#	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		#if nick != self.current_user:
		#	serf.redirect('/')
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield client.fetch("http://192.168.1.21:8888/subforums")	
		lista = str(response.body)
		lista=lista.replace('<br>','')
		lista=lista.replace('\'','')
		lista=lista[1:]
		listaw = lista.split('\\n')
		listawyn = []
		for a in listaw:
			listawyn.append(a.split('\\t'))
		admin=0
		try:
			client = tornado.httpclient.AsyncHTTPClient()
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			admin=1
		except Exception as e:
			admin=0
#				self.write(e)o	
		finally:
			self.render("strony/forumList.html",title="no cos mojego z pythona",nick=self.current_user,danen=listawyn,admin=admin)

class DeleteForumHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr):
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
		except Exception as e:
			self.redirect("/")
		self.render("strony/deleteForum.html",title="no cos mojego z pythona",nick=self.current_user)

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,fnr):
		if self.get_argument("option")!="yes":
                                self.redirect("/")
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
		except Exception as e:
			self.redirect("/")
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr,method='DELETE')	
			self.redirect("/")
		except Exception as e:
			self.redirect("/")

class ForumChangeDataHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr):
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
		except Exception as e:
			self.redirect("/")
			return
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+str(fnr))
		except Exception as e:
			self.redirect("/")
			return
		lista = str(response.body)
		lista=lista.replace('<br>','')
		lista=lista.replace('\'','')
		lista=lista[1:]
		listawyn = lista.split('\\t')
		self.render("strony/forumChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=listawyn[2],olddescri=listawyn[4])

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,fnr):
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
		except Exception as e:
			self.redirect("/")
			return
		if ( len(self.get_argument("topic",default=""))<1 ) or ( len(self.get_argument("desc",default=""))<1) or ( len(self.get_argument("pass",default=""))<1):
			self.render("strony/forumChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""))
			return
		post_data = { 'pass': str(self.get_argument("pass")) }
		body = urllib.parse.urlencode(post_data)
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/login/"+str(self.current_user.decode()),method='POST',body=body)
		except Exception as e:
			self.render("strony/forumChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""))
			return
		post_data_final = {'temat': str(self.get_argument("topic")),'descri': str(self.get_argument("desc"))}
		body_final = urllib.parse.urlencode(post_data_final)
		headerss = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			print("asd");
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr,method='PUT',headers=headerss,body=body_final)
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.render("strony/forumChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""))
			return
		self.redirect("/")
class ForumAddHandler(loginFilter.LoginFilter):
	@tornado.gen.coroutine
	def get(self):
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
		except Exception as e:
			self.redirect("/")
			return
		self.render("strony/forumChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic="",olddescri="")

	@tornado.gen.coroutine
	def post(self):
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
		except Exception as e:
			self.redirect("/")
			return
		try:
			response = yield client.fetch("http://192.168.1.21:8888/user/"+str(self.current_user.decode()))
		except Exception as e:
			self.redirect("/")
			return
		lista = str(response.body)
		lista=lista.replace('\'','')
		lista=lista[1:]
		listaw = lista.split('\\t')
		unr=listaw[4]
		if ( len(self.get_argument("topic",default=""))<1 ) or ( len(self.get_argument("desc",default=""))<1) or ( len(self.get_argument("pass",default=""))<1):
			self.render("strony/forumAdd.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""))
			return
		post_data = { 'pass': str(self.get_argument("pass")) }
		body = urllib.parse.urlencode(post_data)
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/login/"+str(self.current_user.decode()),method='POST',body=body)
		except Exception as e:
			self.render("strony/forumChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""))
			return
		
		post_data_u = { 'uid': unr }
		body_u = urllib.parse.urlencode(post_data_u)
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforums",method='POST',body=body_u)
		except Exception as e:
			raise e
			print("asd");
			self.redirect("/")
			return
#		print(response.body.decode())
#		return

		post_data_final = {'temat': str(self.get_argument("topic")),'descri': str(self.get_argument("desc"))}
		body_final = urllib.parse.urlencode(post_data_final)
		headerss = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			print("asdd");
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+response.body.decode(),method='PUT',headers=headerss,body=body_final)
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.render("strony/forumChangeData.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""))
			return
		self.redirect("/")
"""
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
"""
