import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
from google.appengine.ext import db
import re
import random
from  flickrAPI import ColorOfWordsAPI


class Word(db.Model):
	text = db.StringProperty(required = True)
	hue = db.ListProperty(int,default=[random.randrange(0,256),random.randrange(0,256),random.randrange(0,256)])
	saturation = db.ListProperty(int,default=[random.randrange(0,256),random.randrange(0,256),random.randrange(0,256)])
	value = db.ListProperty(int,default=[random.randrange(0,256),random.randrange(0,256),random.randrange(0,256)])
	publicFlickrURL = db.StringProperty(default="http://flickr.com")
	flickrAPISuccess = db.BooleanProperty(default=False)
	created = db.DateTimeProperty( auto_now_add = True)
	
#demo of new entry page where a user enters a word for analysis
class NewWord(webapp.RequestHandler):
	path = os.path.join(os.path.dirname(__file__), 'templates/beta_newword.html')	

	def renderPage(self,word="",error=""):
		html = template.render(self.path,{"word":word,"error":error})
		self.response.out.write(html)
				
	def get(self):
		self.renderPage()

	def post(self):
		word = cgi.escape(self.request.get("word"))
		word = word.strip()
		word = word.split(' ')[0] #only focus on first word in multiword string			
		if len(word) == 0:
			self.renderPage("","please enter a word")
		else:
			matchingWords = db.GqlQuery("SELECT * FROM Word where text = :1",word)
			if matchingWords.count() == 0:
				#this word doesn't exist in the DB
				
				#Grab Data from Flickr
				flickrWrapper = ColorOfWordsAPI()
				flickrData = flickrWrapper.queryFlickrAPI(word)
				hueData = [int(i) for i in flickrData["hue"].split(",")]
				saturationData = [int(i) for i in flickrData["saturation"].split(",")]
				valueData = [int(i) for i in flickrData["value"].split(",")]
				publicFlickrURL = flickrData["publicFlickrURL"]
				flickrAPISuccess = flickrData["flickrAPISuccess"]
				
				#Create a new entry in Database
				w = Word(text = word, hue = hueData, saturation = saturationData, value=valueData, publicFlickrURL = publicFlickrURL, flickrAPISuccess = flickrAPISuccess)
				w.put()
				self.redirect("/beta/word/%s" % w.key().id())
				
			if matchingWords.count() == 1:
				#this word already exists in the DB just jump to permalink page
				match = matchingWords.get()
				self.redirect("/beta/word/%s" % match.key().id())
		
				
#admin page where we can see all words that have been entered
class AllWords(webapp.RequestHandler):
	path = os.path.join(os.path.dirname(__file__), 'templates/beta_allwords.html')	

	def renderPage(self,wordcollection=""):
		html = template.render(self.path,{"wordcollection":wordcollection})
		self.response.out.write(html)


	def get(self):
		words = db.GqlQuery("SELECT * FROM Word ORDER BY created DESC")			
		self.renderPage(wordcollection=words)

#permlink to a single word whose colour we've determined (or made up!)
class SingleWord(webapp.RequestHandler):
	path = os.path.join(os.path.dirname(__file__), 'templates/beta_singleword.html')	
		
	def get(self,word_id):
		word = db.GqlQuery("SELECT * FROM Word where __key__ = KEY('Word',:1)",int(word_id))
		if word.get():  #check to see whether word exists in datastore
			wordEntered = word.get().text
			flickrURL = word.get().publicFlickrURL
			hueColor = [int(i) for i in  word.get().hue]
			html = template.render(self.path,{"word":wordEntered,"flickrLink":flickrURL,"hueData":hueColor})
			self.response.out.write(html)
		else:
			self.redirect("/beta")
		
	
app = webapp.WSGIApplication([('/beta', NewWord),('/beta/', NewWord),('/beta/enterword',NewWord),(r'/beta/word/(\d+)',SingleWord),('/beta/listallwords',AllWords)], debug=True)

def main():
	run_wsgi_app(app)

if __name__ == '__main__':
	main()


