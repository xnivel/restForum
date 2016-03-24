import pymysql 
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world!<br>")

class UsersHandler(tornado.web.RequestHandler):
	def get(self):
#		self.write("Lista uzytkownikow<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select nick from users")
#		self.write("ilosc: "+str(cur.rowcount)+"<br>")
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+'\n')
			self.write("<br>")
	def post(self):
		#self.write("Lista uzytkownikow<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		#cur.execute("select nick from users")
		cur.execute("insert into users(nick,data) values (%s,curdate())",self.get_argument("nick"))
		if cur.rowcount <1:
			raise tornado.web.HTTPError(400)
		self.set_status(200)
		self.set_header("Content-Type", "text/plain")
		self.add_header("X-Example-Counter", 10)
		self.write("Return code: 200\n")
		conn.commit();

class AdminUserHandler(tornado.web.RequestHandler):
	def get(self, nick):
#		self.write("Uzytkownik "+nick+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select * from users where nick=%s and admin=1",nick)
		if cur.rowcount <1:
			raise tornado.web.HTTPError(400)
		self.set_status(200)
		self.set_header("Content-Type", "text/plain")
		self.add_header("X-Example-Counter", 10)
		self.write("Return code: 200\n")

class LoginUserHandler(tornado.web.RequestHandler):
	def post(self, nick):
#		self.write("Uzytkownik "+nick+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select * from users where nick=%s and pass=md5(%s)",[nick,self.get_argument("pass")])
		if cur.rowcount <1:
			raise tornado.web.HTTPError(400)
		self.set_status(200)
		self.set_header("Content-Type", "text/plain")
		self.add_header("X-Example-Counter", 10)
		self.write("Return code: 200\n")


class UserHandler(tornado.web.RequestHandler):
	def get(self, nick):
#		self.write("Uzytkownik "+nick+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select nick,imie,nazwisko,email,admin,iloscp,unr from users where nick=%s",nick)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+'\t')
	def post(self, nick):
		print(self.request.arguments)

	def put(self, nick):
		print(self.request.arguments)
		wynik = 0
		self.write("Uzytkownik "+nick+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		print(self.request.arguments)
#		try:
		if self.get_argument("imie",default="")!="":
			cur.execute("update users set imie=%s where nick=%s",[self.get_argument("imie"),nick])
		if self.get_argument("nazwisko",default="")!="":
			cur.execute("update users set nazwisko=%s where nick=%s",[self.get_argument("nazwisko"),nick])
		if self.get_argument("email",default="")!="":
			cur.execute("update users set email=%s where nick=%s",[self.get_argument("email"),nick])
		if self.get_argument("pass",default="")!="":
			cur.execute("update users set pass=md5(%s) where nick=%s",[self.get_argument("pass"),nick])
		if self.get_argument("avatar",default="")!="":
			cur.execute("update users set avatar=%s where nick=%s",[self.get_argument("avatar"),nick])
		if self.get_argument("nick",default="")!="":
			cur.execute("update users set nick=%s where nick=%s",[self.get_argument("nick"),nick])
#		except Exception as e:
#			conn.close()
#			raise tornado.web.HTTPError(405)
		self.set_status(200)
		self.set_header("Content-Type", "text/plain")
		self.add_header("X-Example-Counter", 10)
		self.write("Return code: 200\n")
		conn.commit()
		self.write(str(wynik))
	def delete(self, nick):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("delete from users where nick=%s",nick)
		conn.commit()
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+' ')
			self.write("<br>")

class UserMsgHandler(tornado.web.RequestHandler):
	def get(self, user,nrid):
		self.write("Uzytkownik "+id+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select * from messages where mnr=%d",nrid)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+' ')
			self.write("<br>")
	def delete(self, user,nrid):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("delete from messages where mnr=%d",nrid)
		conn.commit()
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+' ')
			self.write("<br>")

class UserMsgSHandler(tornado.web.RequestHandler):
	def post(self, userid):
		self.write("Uzytkownik "+user+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("input into messages (unro) values(%d)",userid)
		conn.commit()
		cut.execute("select mnr from messages where unro=%d and tresc=null",userid)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+' ')
			self.write("<br>")

class UserMsgSENDPAGEHandler(tornado.web.RequestHandler):
	def get(self, user,strid):
		self.write("Uzytkownik "+user+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select * from messages where unrt=%s limit %d,%d",user,10*strid,10*strid+10)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+' ')
			self.write("<br>")

class UserMsgRECVPAGEHandler(tornado.web.RequestHandler):
	def get(self, user,strid):
		self.write("Uzytkownik "+user+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select * from messages where unro=%s limit %d,%d",user,10*strid,10*strid+10)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+' ')
			self.write("<br>")

class PostsHandler(tornado.web.RequestHandler):
	def get(self, userid,strid):
		self.write("Uzytkownik "+userid+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select * from users where nick=%s limit %s,%s",userid,10*strid,10*strid+10)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+' ')
			self.write("<br>")

class SubforumsHandler(tornado.web.RequestHandler):
	def get(self):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select * from forums")
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+'\t')
			self.write("\n")
	def post(self):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("insert into forums (unr,data) values (%s,curdate())",self.get_argument("uid"))
		conn.commit();
		cur.execute("select fnr from forums where unr=%s and data=curdate()",self.get_argument("uid"))
		if cur.rowcount>0:
			self.set_status(200)
			self.set_header("Content-Type", "text/plain")
			self.add_header("X-Example-Counter", 10)
			tmp=cur.fetchone()[0]
			conn.close()
			self.write(str(tmp))
		else:
			conn.close()
			raise tornado.web.HTTPError(400)

class SubforumHandler(tornado.web.RequestHandler):
	def delete(self, fnr):
		print("asd")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("delete from forums where fnr=%s",fnr)
		if cur.rowcount <1:
			raise tornado.web.HTTPError(400)
		self.set_status(200)
		self.set_header("Content-Type", "text/plain")
		self.add_header("X-Example-Counter", 10)
		self.write("Return code: 200\n")
		conn.commit()
	def put(self,fid):
		print("weszlo do puta");
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		print("if1");
		if (len(self.get_argument("temat",default=""))<1 or len(self.get_argument("descri",default=""))<1):
			print(self.request.arguments)
			raise tornado.web.HTTPError(400)
			return
		cur.execute("update forums set temat=%s, descri=%s where fnr=%s",[self.get_argument("temat"),self.get_argument("descri"),fid])
		print("if2");
		if cur.rowcount >0:
			self.set_status(200)
			self.set_header("Content-Type", "text/plain")
			self.add_header("X-Example-Counter", 10)
			self.write("Return code: 200\n")
		else:
			conn.close()
			raise tornado.web.HTTPError(400)
		conn.commit()
	def get(self,fid):
#		self.write("Uzytkownik "+fid+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		nr=1
		cur.execute("select * from forums where fnr=%s",int(fid))
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+'\t')
			self.write("\n")

class SubforumTopicSHandler(tornado.web.RequestHandler):
	def post(self,fid):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("insert into topics (fnr,unr,data) values(%s,%s,curdate())",[fid,self.get_argument("uid")])
		conn.commit()
		cur.execute("select tnr from topics where fnr=%s and unr=%s and data=curdate()",[fid,self.get_argument("uid")])
		if cur.rowcount>0:
			self.set_status(200)
			self.set_header("Content-Type", "text/plain")
			self.add_header("X-Example-Counter", 10)
			tmp=cur.fetchone()[0]
			conn.close()
			self.write(str(tmp))
		else:
			conn.close()
			raise tornado.web.HTTPError(400)

class SubforumTopicSPAGEHandler(tornado.web.RequestHandler):
	def get(self,fid,strid):
		#self.write("Uzytkownik "+fid+"<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		llimit=10*int(strid)-10
		rlimit=int(llimit)+10
		#print("ll "+str(llimit)+" rl "+str(rlimit))
		tmp=10
		cur.execute("select t.*,u.nick from topics t join users u on t.unr=u.unr where fnr=%s limit %s,%s",[fid,llimit,rlimit])
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				if isinstance(article[i],bytes):
					self.write(article[i].decode()+'\t')
				else:
					self.write(str(article[i])+'\t')
			self.write('\n')

class SubforumTopicHandler(tornado.web.RequestHandler):
	def delete(self, fnr,tnr):
		print("asd")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("delete from topics where tnr=%s",tnr)
		if cur.rowcount <1:
			raise tornado.web.HTTPError(400)
		self.set_status(200)
		self.set_header("Content-Type", "text/plain")
		self.add_header("X-Example-Counter", 10)
		self.write("Return code: 200\n")
		conn.commit()
	def put(self,fid,tid):
		print("weszlo do puta");
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		print("if1");
		if (len(self.get_argument("temat",default=""))<1 or len(self.get_argument("description",default=""))<1):
			print(self.request.arguments)
			raise tornado.web.HTTPError(400)
			return
		cur.execute("update topics set temat=%s, description=%s,value=%s where tnr=%s",[self.get_argument("temat",default=""),self.get_argument("description",default=""),self.get_argument("value",default=""),tid])
		print("if2");
		if cur.rowcount >0:
			self.set_status(200)
			self.set_header("Content-Type", "text/plain")
			self.add_header("X-Example-Counter", 10)
			self.write("Return code: 200\n")
		else:
			conn.close()
			raise tornado.web.HTTPError(400)
		conn.commit()
	def post(self,fid,tid):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("insert into posts (tnr,unr,data) values(%s,%s,curdate())",[tid,self.get_argument("uid")])
		conn.commit()
		cur.execute("select pnr from posts where tnr=%s and unr=%s and tresc is NULL and data=curdate()",[tid,self.get_argument("uid")])
		if cur.rowcount>0:
			self.set_status(200)
			self.set_header("Content-Type", "text/plain")
			self.add_header("X-Example-Counter", 10)
			tmp=cur.fetchone()[0]
			conn.close()
			self.write(str(tmp))
		else:
			conn.close()
			raise tornado.web.HTTPError(400)
	def get(self,fid,tid):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select t.*,u.nick,u.imie,u.nazwisko from topics t join users u on t.unr=u.unr where tnr=%s order by t.data DESC;",tid)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				if isinstance(article[i],bytes):
					self.write(article[i].decode()+'\t')
				else:
					self.write(str(article[i])+'\t')
			self.write("<br>")

class SubforumTopicPAGEHandler(tornado.web.RequestHandler):
	def get(self,fid,tid,strid):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		llimit=10*int(strid)-10
		rlimit=int(llimit)+10
		cur.execute("select p.*,u.nick,u.imie,u.nazwisko from posts p join users u on p.unr=u.unr where tnr=%s limit %s,%s",[tid,llimit,rlimit])
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				if isinstance(article[i],bytes):
					self.write(article[i].decode()+'\t')
				else:
					self.write(str(article[i])+'\t')
			self.write('\n')

class SubforumTopicPostHandler(tornado.web.RequestHandler):
	def get(self,fid,tid,strid):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select p.*,u.nick from posts p join users u on p.unr=u.unr where pnr=%s",strid)
		if cur.rowcount <1:
			raise tornado.web.HTTPError(400)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				if isinstance(article[i],bytes):
					self.write(article[i].decode()+'\t')
				else:
					self.write(str(article[i])+'\t')
			self.write('\n')
	def delete(self,fid,tid,strid):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("delete from posts where pnr=%s",strid)
		if cur.rowcount <1:
			raise tornado.web.HTTPError(400)
		self.set_status(200)
		self.set_header("Content-Type", "text/plain")
		self.add_header("X-Example-Counter", 10)
		self.write("Return code: 200\n")
		conn.commit()
	def put(self,fid,tid,strid):
		print("weszlo do puta poprawnego");
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		print("if12");
		if (len(self.get_argument("value",default=""))<1 ):
			print(self.get_argument("value"))
			print(self.request.arguments)
			raise tornado.web.HTTPError(400)
			return
		cur.execute("update posts set tresc=%s where pnr=%s",[self.get_argument("value",default=""),strid])
		print("if22");
		if cur.rowcount >0:
			self.set_status(200)
			self.set_header("Content-Type", "text/plain")
			self.add_header("X-Example-Counter", 10)
			self.write("Return code: 200\n")
		else:
			conn.close()
			raise tornado.web.HTTPError(400)
		conn.commit()
class ChatHandler(tornado.web.RequestHandler):
	def get(self):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select u.nick,c.data,c.value from chat c join users u on c.unr=u.unr limit 10")
		if cur.rowcount <1:
			raise tornado.web.HTTPError(400)
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				if isinstance(article[i],bytes):
					self.write(article[i].decode()+'\t')
				else:
					self.write(str(article[i])+'\t')
			self.write('\n')
	def post(self):
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("insert into chat (unr,value) values(%s,%s)",[self.get_argument("uid"),self.get_argument("value")])
		conn.commit()
		cur.execute("select u.nick,c.data,c.value from chat c join users u on c.unr=u.unr where c.unr=%s and c.value=%s order by data desc limit 1",[self.get_argument("uid"),self.get_argument("value")])
		if cur.rowcount>0:
			for article in cur: 
			#self.write(''.join(map(str,article)));
				for i in range(len(article)):
					if isinstance(article[i],bytes):
						self.write(article[i].decode()+'\t')
					else:
						self.write(str(article[i])+'\t')
				self.write('\n')
			self.set_status(200)
			self.set_header("Content-Type", "text/plain")
			self.add_header("X-Example-Counter", 10)
			conn.close()
		else:
			conn.close()
			raise tornado.web.HTTPError(400)

if __name__ == "__main__":
	application = tornado.web.Application([
		("/", MainHandler),
		("/users", UsersHandler),
		("/admin/([0-9 a-z]+)", AdminUserHandler),
		("/user/([0-9 a-z]+)", UserHandler),
		("/login/([0-9 a-z]+)", LoginUserHandler),
		("/user/([0-9 a-z]+)/msgs", UserMsgSHandler),
		("/user/([0-9 a-z]+)/msgssend/([0-9]+)", UserMsgSENDPAGEHandler),
		("/user/([0-9 a-z]+)/msgsrecv/([0-9]+)", UserMsgRECVPAGEHandler),
		("/user/([0-9 a-z]+)/msg/([0-9]+)", UserMsgHandler),
		("/posts/([0-9 a-z]+)/([0-9]+)", PostsHandler),
		("/subforums", SubforumsHandler),
		("/subforum/([0-9]+)", SubforumHandler),
		("/subforum/([0-9]+)/topics", SubforumTopicSHandler),
		("/subforum/([0-9]+)/topics/([0-9]+)", SubforumTopicSPAGEHandler),
		("/subforum/([0-9]+)/topic/([0-9]+)", SubforumTopicHandler),
		("/subforum/([0-9]+)/topic/([0-9]+)/([0-9]+)", SubforumTopicPAGEHandler),
		("/subforum/([0-9]+)/topic/([0-9]+)/post/([0-9]+)", SubforumTopicPostHandler),
		("/chat", ChatHandler),
	])
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
