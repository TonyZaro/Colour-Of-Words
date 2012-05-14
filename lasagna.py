import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import simplejson as json
from xml.etree import ElementTree as ET

class LasagnaAPIOutput(webapp.RequestHandler):

	
	#dictionary to hold all data
	my_dict = {
	"hue" : "255,94,0",
	"saturation" : "255,153,94",
	"value" : "217,79,0",
	"publicFlickrURL" : "http://www.flickr.com/photos/dippy_duck/7060788361/",
	"imageURL": "http://farm8.staticflickr.com//7095//7060788361_409972d2b1_q.jpg",
	"analyzerURL": "http://mkweb.bcgsc.ca/color_summarizer/?xml=1&url=http://farm8.staticflickr.com//7095//7060788361_409972d2b1_q.jpg&precision=medium",
	"targetWord": "lasagna", 
	"title": "lasagna",
	"flickrAPISucces": "yes",
	"id": "7060788361"
	}



	
	
	def get(self):
		
		#4. Convert the dictionary to JSON and return it to user
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		my_json = json.dumps(self.my_dict)
		self.response.out.write(my_json)
	
		

app = webapp.WSGIApplication([('/lasagna', LasagnaAPIOutput)], debug=True)

def main():
	run_wsgi_app(app)

if __name__ == '__main__':
	main()







