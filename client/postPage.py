import tornado.ioloop
import tornado.web
import tornado.ioloop
import tornado.httpclient
import http.client
import loginFilter
import urllib

class PostPageHandler(loginFilter.LoginFilter):
#	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr,tnr):
		self.redirect("/forum/"+fnr+"/topic/"+tnr+"/1");
class PostPageSHandler(loginFilter.LoginFilter):
#	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr,tnr,page):
		#if nick != self.current_user:
		#	serf.redirect('/')
		admin=0
		topic=""
		topicname=""
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
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr)
			lista = str(response.body)
			lista=lista.replace('<br>','')
			lista=lista.replace('\'','')
			lista=lista[1:]
			listaw = lista.split('\\t')
			topicname=listaw[3]
			topicid=listaw[0]
			topicdesc=listaw[5]
			topicval=listaw[6]
			topicnick=listaw[7]
			topicimie=listaw[8]
			topicnazwisko=listaw[9]
			#print(listaw[7])
		except Exception as e:
			self.redirect("/forum/"+fnr+"/topics")
			pass
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr)	
			lista = str(response.body)
			lista=lista.replace('<br>','')
			lista=lista.replace('\'','')
			lista=lista[1:]
			listaw = lista.split('\\t')
			forum = listaw[2]
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
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr+"/"+page)
			lista = str(response.body)
			lista=lista.replace('<br>','')
			lista=lista.replace('\'','')
			lista=lista[1:]
			listaw = lista.split('\\n')
			listawyn = []
			for a in listaw:
				listawyn.append(a.split('\\t'))
	#print(listaw[7])
		except Exception as e:
			self.redirect("/forum/"+fnr+"/topics")
			pass
		self.render("strony/postsList.html",title="no cos mojego z pythona",nick=self.current_user,forum=forum,topic=topicname,topicdesc=topicdesc,topicval=topicval,fnr=fnr,danen=listawyn,admin=admin,topicnick=topicnick,topicimie=topicimie,topicnazwisko=topicnazwisko,tnr=tnr,topicid=topicid)
class DeletePostHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr,tnr,post):
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
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr+"/post/"+post)
				lista = str(response.body)
				lista=lista.replace('<br>','')
				lista=lista.replace('\'','')
				lista=lista[1:]
				listaw = lista.split('\\t')
				#print(listaw[7])
				if listaw[5]==self.current_user.decode(): 
					admin=1;
			except Exception as e:
				pass
		if admin ==0:
			self.redirect("/")

			
		self.render("strony/deletePost.html",title="no cos mojego z pythona",nick=self.current_user)

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,fnr,tnr,post):
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
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr+"/post/"+post)
				lista = str(response.body)
				lista=lista.replace('<br>','')
				lista=lista.replace('\'','')
				lista=lista[1:]
				listaw = lista.split('\\t')
				#print(listaw[7])
				if listaw[5]==self.current_user.decode(): 
					admin=1;
			except Exception as e:
				pass
		if admin ==0:
			self.redirect("/")
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr+"/post/"+post,method='DELETE')	
			self.redirect("/")
		except Exception as e:
			self.redirect("/")

class PostChangeDataHandler(loginFilter.LoginFilter):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self,fnr,tnr,pnr):
		client = tornado.httpclient.AsyncHTTPClient()
		admin=0;
		oldval=""
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			admin=1;
		except Exception as e:
			#self.redirect("/")
			pass

		if admin !=2:
			try:
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr+"/post/"+pnr)
				lista = str(response.body)
				lista=lista.replace('<br>','')
				lista=lista.replace('\'','')
				#lista=lista[1:]
				listaw = lista.split('\\t')
				oldval=listaw[3]
			
				#print(listaw[7])
				if listaw[5]==self.current_user.decode(): 
					admin=1;
			except Exception as e:
				raise e
				pass
		if admin ==0:
			self.redirect("/")
			return
		self.render("strony/postChangeData.html",title="no cos mojego z pythona",nick=self.current_user,fnr=fnr,tnr=tnr,pnr=pnr,oldval=oldval)
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self,fnr,tnr,pnr):
		client = tornado.httpclient.AsyncHTTPClient()
		admin=0;
		oldval=""
		try:
			response = yield client.fetch("http://192.168.1.21:8888/admin/"+str(self.current_user.decode()))
			admin=1;
		except Exception as e:
			#self.redirect("/")
			pass

		if admin !=2:
			try:
				response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr+"/post/"+pnr)
				lista = str(response.body)
				lista=lista.replace('<br>','')
				lista=lista.replace('\'','')
				#lista=lista[1:]
				listaw = lista.split('\\t')
				#print(listaw[7])
				if listaw[5]==self.current_user.decode(): 
					admin=1;
			except Exception as e:
				raise e
				pass
		if admin ==0:
			self.redirect("/")
			return
#przeslane dane czy sa puste
		if ( len(self.get_argument("value",default=""))<1):
			self.render("strony/postChangeData.html",title="no cos mojego z pythona",nick=self.current_user,fnr=fnr,tnr=tnr,pnr=pnr,oldval=self.get_argument("value",default=""))
			return
# post		
# PUT
		post_data_final = {'value': str(self.get_argument("value"))}
		body_final = urllib.parse.urlencode(post_data_final)
		headerss = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			print("asdd");
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr+"/post/"+pnr,method='PUT',headers=headerss,body=body_final)
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.redirect("/forum/"+fnr+"/topic/"+tnr)
			return
		self.redirect("/forum/"+fnr)

class PostAddHandler(loginFilter.LoginFilter):
	@tornado.gen.coroutine
	def post(self,fnr,tnr):
## dostaje unr
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
#przeslane dane czy sa puste
		if ( len(self.get_argument("value",default=""))<1):
			self.redirect("/forum/"+fnr+"/topic/"+tnr)
			return
# post		
		post_data_u = { 'uid': unr }
		body_u = urllib.parse.urlencode(post_data_u)
		try:
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr,method='POST',body=body_u)
		except Exception as e:
			raise e
			print("asd");
			self.redirect("/")
			return
		print(response.body.decode())
		#return
# PUT
		post_data_final = {'value': str(self.get_argument("value"))}
		body_final = urllib.parse.urlencode(post_data_final)
		headerss = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			print("asdd");
			response = yield client.fetch("http://192.168.1.21:8888/subforum/"+fnr+"/topic/"+tnr+"/post/"+response.body.decode(),method='PUT',headers=headerss,body=body_final)
		except Exception as e:
			raise e
			print("asdddddddddddddddddddd")
			self.redirect("/forum/"+fnr+"/topic/"+tnr)
			return
		self.redirect("/forum/"+fnr)
