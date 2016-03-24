import tornado.ioloop
import tornado.websocket
import tornado.web
import tornado.ioloop
import tornado.httpclient
import urllib
import loginFilter
import main
import login
import usersList
import userPage
import forumPage
import topicPage
import postPage
import chatPage



settings = {
	"cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
	"login_url": "/login",
}

if __name__ == "__main__":
	application = tornado.web.Application([
		(r"/css/(.*)", tornado.web.StaticFileHandler, {"path": "css/"}),
		(r"/img/(.*)", tornado.web.StaticFileHandler, {"path": "img/"}),
		("/", forumPage.ForumPageHandler),
		("/forum/([0-9]+)/topic/([0-9]+)", postPage.PostPageHandler),
		("/forum/([0-9]+)/topic/([0-9]+)/([0-9]+)", postPage.PostPageSHandler),
		("/forum/([0-9]+)/topic/([0-9]+)/Add", postPage.PostAddHandler),
		("/forum/([0-9]+)/topic/([0-9]+)/post/([0-9]+)/edit", postPage.PostChangeDataHandler),
		("/forum/([0-9]+)/topic/([0-9]+)/post/([0-9]+)/delete", postPage.DeletePostHandler),
		("/forum/([0-9]+)", topicPage.TopicPageHandler),
		("/forum/([0-9]+)/topic/([0-9]+)/delete", topicPage.DeleteTopicHandler),
		("/forum/([0-9]+)/topic/([0-9]+)/edit", topicPage.TopicChangeDataHandler),
		("/forum/([0-9]+)/([0-9]+)", topicPage.TopicPageSHandler),
		("/forum/([0-9]+)/Add", topicPage.TopicAddHandler),
		("/forumEdit/([0-9]+)", forumPage.ForumChangeDataHandler),
		("/forumDelete/([0-9]+)", forumPage.DeleteForumHandler),
		("/forumAdd", forumPage.ForumAddHandler),
		("/userslist", usersList.UsersListHandler),
		("/user/([0-9a-z]+)", userPage.UserPageHandler),
		("/userRegister", userPage.UserRegisterHandler),
		("/userChangeData/([0-9a-z]+)", userPage.UserChangeDataHandler),
		("/userChangePass/([0-9a-z]+)", userPage.UserChangePassHandler),
		("/userDelete/([0-9a-z]+)", userPage.DeleteUserHandler),
		("/login", login.LoginHandler),
		("/logout", login.LogoutHandler),
		("/chat", chatPage.ChatHandler),
	], **settings)
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
