import pymysql 
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world!<br>")
		conn = pymysql.Connection("localhost",user="ruser",passwd="pass",db='restforum')
		cur= conn.cursor()
		cur.execute("select * from users")
		for article in cur: 
			#self.write(''.join(map(str,article)));
			for i in range(len(article)):
				self.write(str(article[i])+' ')

if __name__ == "__main__":
	application = tornado.web.Application([
		("/", MainHandler),
	])
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
