import tornado.ioloop
import tornado.web
import tornado.ioloop
import tornado.httpclient
import http.client
import loginFilter
import urllib

class TopicPageHandler(loginFilter.LoginFilter):
#	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr):
		self.redirect("/forum/"+fnr+"/1");
class TopicPageSHandler(loginFilter.LoginFilter):
#	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr,page):
		#if nick != self.current_user:
		#	serf.redirect('/')
		admin=0
		topic=""
		unr=-1
		if self.current_user!=None and self.current_user!="":
			client = tornado.httpclient.AsyncHTTPClient()
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
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topics/"+page)	
		lista = str(response.body)
		print(lista)
		lista=lista.replace('<br>','')
		lista=lista.replace('\'','')
		lista=lista[1:]
		listaw = lista.split('\\n')
		listawyn = []
		for a in listaw:
			listawyn.append(a.split('\\t'))
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr)	
			lista = str(response.body)
			lista=lista.replace('<br>','')
			lista=lista.replace('\'','')
			lista=lista[1:]
			listaw = lista.split('\\t')
			topic = listaw[2]
		except Exception as e:
	        	self.redirect("/")
#			return
		admin=0
		try:
			client = tornado.httpclient.AsyncHTTPClient()
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			admin=1
		except Exception as e:
			admin=0
#				self.write(e)o	
		self.render("strony/topicsList.html",title="no cos mojego z pythona",nick=self.current_user,topic=topic,fnr=fnr,danen=listawyn,unr=unr,admin=admin)

class DeleteTopicHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr,tnr):
		client = tornado.httpclient.AsyncHTTPClient()
		admin=0;
		topicname=""
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			admin=1;
		except Exception as e:
			#self.redirect("/")
			pass

		if admin !=2:
			try:
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr)
				lista = str(response.body)
				lista=lista.replace('<br>','')
				lista=lista.replace('\'','')
				lista=lista[1:]
				listaw = lista.split('\\t')
				topicname=listaw[3]
				#print(listaw[7])
				if listaw[7]==self.current_user.decode(): 
					admin=1;
			except Exception as e:
				pass
		if admin ==0:
			self.redirect("/")

			
		self.render("strony/deleteTopic.html",title="no cos mojego z pythona",topic=topicname,nick=self.current_user)

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,fnr,tnr):
		if self.get_argument("option")!="yes":
                                self.redirect("/")
		client = tornado.httpclient.AsyncHTTPClient()
		admin=0;
		topicname=""
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			admin=1;
		except Exception as e:
			#self.redirect("/")
			pass

		if admin !=2:
			try:
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr)
				lista = str(response.body)
				lista=lista.replace('<br>','')
				lista=lista.replace('\'','')
				lista=lista[1:]
				listaw = lista.split('\\t')
				topicname=listaw[3]
				#print(listaw[7])
				if listaw[7]==self.current_user.decode(): 
					admin=1;
			except Exception as e:
				pass
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr,method='DELETE')	
			self.redirect("/")
		except Exception as e:
			self.redirect("/")
class TopicChangeDataHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr,tnr):
		client = tornado.httpclient.AsyncHTTPClient()
		admin=0;
		topicname=""
		topicdesc=""
		topicval=""
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			admin=1;
		except Exception as e:
			#self.redirect("/")
			pass

		if admin !=2:
			try:
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr)
				lista = str(response.body)
				lista=lista.replace('<br>','')
				lista=lista.replace('\'','')
				lista=lista[1:]
				listaw = lista.split('\\t')
				topicname=listaw[3]
				topicdesc=listaw[5]
				topicval=listaw[6]
				#print(listaw[7])
				if listaw[7]==self.current_user.decode(): 
					admin=1;
			except Exception as e:
				pass
		if admin ==0:
			self.redirect("/")
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr)	
		except Exception as e:
	        	self.redirect("/")
#			return
		lista = str(response.body)
		lista=lista.replace('<br>','')
		lista=lista.replace('\'','')
		lista=lista[1:]
		listaw = lista.split('\\t')
		topic = listaw[2]
		self.render("strony/topicAdd.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=topicname,olddescri=topicdesc,oldvalue=topicval,topic=topic,fnr=fnr)
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,fnr,tnr):
		client = tornado.httpclient.AsyncHTTPClient()
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
		if ( len(self.get_argument("topic",default=""))<1 ) or ( len(self.get_argument("value",default=""))<1):
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr)	
			except Exception as e:
	        		self.redirect("/")
#			return
			lista = str(response.body)
			lista=lista.replace('<br>','')
			lista=lista.replace('\'','')
			lista=lista[1:]
			listaw = lista.split('\\t')
			topic = listaw[2]
			self.render("strony/topicAdd.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""),oldvalue=self.get_argument("value",default=""),topic=topic,fnr=fnr)
			return

		post_data_final = {'temat': str(self.get_argument("topic")),'value': str(self.get_argument("value")),'description': str(self.get_argument("desc"))}
		body_final = urllib.parse.urlencode(post_data_final)
		headerss = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			print("asdd");
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr,method='PUT',headers=headerss,body=body_final)
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.render("strony/topicAdd.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""),oldvalue=self.get_argument("value",default=""),topic=topic,fnr=fnr)
			return
		self.redirect("/forum/"+fnr)

class TopicAddHandler(loginFilter.LoginFilter):
	@tornado.gen.coroutine
	def get(self,fnr):
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr)	
		except Exception as e:
	        	self.redirect("/")
#			return
		lista = str(response.body)
		lista=lista.replace('<br>','')
		lista=lista.replace('\'','')
		lista=lista[1:]
		listaw = lista.split('\\t')
		topic = listaw[2]
		self.render("strony/topicAdd.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic="",olddescri="",oldvalue="",topic=topic,fnr=fnr)

	@tornado.gen.coroutine
	def post(self,fnr):
		client = tornado.httpclient.AsyncHTTPClient()
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
		if ( len(self.get_argument("topic",default=""))<1 ) or ( len(self.get_argument("value",default=""))<1):
			client = tornado.httpclient.AsyncHTTPClient()
			try:
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr)	
			except Exception as e:
	        		self.redirect("/")
#			return
			lista = str(response.body)
			lista=lista.replace('<br>','')
			lista=lista.replace('\'','')
			lista=lista[1:]
			listaw = lista.split('\\t')
			topic = listaw[2]
			self.render("strony/topicAdd.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""),oldvalue=self.get_argument("value",default=""),topic=topic,fnr=fnr)
			return
		
		post_data_u = { 'uid': unr }
		body_u = urllib.parse.urlencode(post_data_u)
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topics",method='POST',body=body_u)
		except Exception as e:
			raise e
			print("asd");
			self.redirect("/")
			return
		print(response.body.decode())
#		return

		post_data_final = {'temat': str(self.get_argument("topic")),'value': str(self.get_argument("value")),'description': str(self.get_argument("desc"))}
		body_final = urllib.parse.urlencode(post_data_final)
		headerss = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			print("asdd");
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+response.body.decode(),method='PUT',headers=headerss,body=body_final)
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.render("strony/topicAdd.html",title="no cos mojego z pythona",nick=self.current_user,oldtopic=self.get_argument("topic",default=""),olddescri=self.get_argument("desc",default=""),oldvalue=self.get_argument("value",default=""),topic=topic,fnr=fnr)
			return
		self.redirect("/forum/"+fnr)

