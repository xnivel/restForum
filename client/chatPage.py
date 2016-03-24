import tornado.ioloop
import tornado.websocket
import tornado.web
import tornado.ioloop
import tornado.httpclient
import http.client
import loginFilter
import urllib

class ChatHandler(tornado.websocket.WebSocketHandler,loginFilter.LoginFilter):
	klienci=[]
#	@tornado.web.authenticated
	@tornado.gen.coroutine
	def open(self):
		print("nie")
		#klienci.append(self)
		ChatHandler.klienci.append(self)
		print("cos")
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield client.fetch("http://192.168.1.21:8888/chat")	
		lista = str(response.body)
		lista=lista.replace('<br>','')
		lista=lista.replace('\'','')
		lista=lista[1:]
		listaw = lista.split('\\n')
		for a in listaw:
			if len(a)>0:
				self.write_message(a)
#	@tornado.web.authenticated
	@tornado.gen.coroutine
	def on_message(self,message):
#		if not self.get_secure_cookie("user"):
		if not self.current_user:
			print("login")
			return
		if(len(message)<1):
			print("mess")
			return
# pobieranie unr
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			response = yield client.fetch("http://192.168.1.21:8888/user/"+str(self.current_user.decode()))
		except Exception as e:
			return
		lista = str(response.body)
		lista=lista.replace('\'','')
		lista=lista[1:]
		listaw = lista.split('\\t')
		unr=listaw[4]
		print(unr)
#ok koniec unr
		post_data_final = {'uid': unr,'value': message}
		body_final = urllib.parse.urlencode(post_data_final)
		headerss = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			print("asdd");
			response = yield client.fetch("http://192.168.1.21:8888/chat",method='POST',headers=headerss,body=body_final)
			lista = str(response.body)
			lista=lista.replace('<br>','')
			lista=lista.replace('\'','')
			lista=lista[1:]
			listaw = lista.split('\\n')
			for a in listaw:
				if len(a)>0:
					for k in ChatHandler.klienci:
						k.write_message(a)
		except Exception as e:
			raise e
		
		print("next")
	def on_close(self):
		ChatHandler.klienci.remove(self)
		print("wyszlo")
