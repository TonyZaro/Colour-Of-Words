import os
import sys
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import simplejson as json
from xml.etree import ElementTree as ET
import credentials #contains details for for flickrAPI calls

class ColorOfWordsAPI():

	api_key = credentials.api_key
	api_secret = credentials.api_secret
	my_dict = {} #dictionary to hold all data

	#URL of "image color summarizer" used to get color composition informaiton about flickr image
	#http://mkweb.bcgsc.ca/color_summarizer/
	
	
	def queryFlickrAPI(self,targetWord):
		
		#1. Get user's target word from query string & place it in data dictionary
		#targetWord = self.request.get('word',default_value='lasagna') #if no input given will use lasagna
		#targetWord = targetWord.strip()
		#targetWord = targetWord.split(' ')[0] #only focus on first word in multiword string
		#targetWord = 'lasagna' if len(targetWord) == 0 else targetWord #handle empty string given as input
		self.my_dict['targetWord'] = targetWord
		
		#2. Query flickr api with target word
		flickrSearchURL = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='+self.api_key+'&text=' + targetWord + '&sort=relevance&format=json&nojsoncallback=1'
		result = urlfetch.fetch(flickrSearchURL)
		self.my_dict['url'] = flickrSearchURL
		
		if result.status_code != 200:
			#call to flickr API has failed generate random colours and return
			self.my_dict['flickrAPISuccess'] = False
			self.my_dict["hue"] = ','.join((str(random.randrange(0,256)),str(random.randrange(0,256)),str(random.randrange(0,256))))
			self.my_dict["saturation"] = ','.join((str(random.randrange(0,256)),str(random.randrange(0,256)),str(random.randrange(0,256))))
			self.my_dict["value"] = ','.join((str(random.randrange(0,256)),str(random.randrange(0,256)),str(random.randrange(0,256))))
			self.my_dict["publicFlickrURL"] = "http://flickr.com"
		
		else:
			data = json.loads(result.content)
			self.my_dict['flickrAPISuccess'] = True
			self.my_dict['id'] = data['photos']['photo'][0]['id']  #id of the photo retrieved needed for subsequent API calls
			self.my_dict['title'] = data['photos']['photo'][0]['title']
			
			flickrGetInfoURL = 'http://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key='+self.api_key+'&photo_id='+self.my_dict['id']+'&format=json&nojsoncallback=1'
			result = urlfetch.fetch(flickrGetInfoURL)
			if result.status_code == 200:
				data = json.loads(result.content)
				self.my_dict['publicFlickrURL'] = data['photo']['urls']['url'][0]['_content'] #have to link to this url for copyright reasons
		
			flickrGetSizeURL =  'http://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key='+self.api_key+'&photo_id='+self.my_dict['id']+'&format=json&nojsoncallback=1'
			result = urlfetch.fetch(flickrGetSizeURL)
			if result.status_code == 200:
				data = json.loads(result.content)
				self.my_dict['imageURL'] = data['sizes']['size'][1]['source'] #url for image file to be analyzed

			#3. Use "image color summarizer" to get hsv info about image
			analyzerURL = "http://mkweb.bcgsc.ca/color_summarizer/?xml=1&url="+self.my_dict['imageURL']+"&precision=medium"
			self.my_dict['analyzerURL'] = analyzerURL
		
			result = urlfetch.fetch(analyzerURL)
			root = ET.XML(result.content)		    #initialzie Element Tree lib with XML returned		
			variableset = root.findall('variable')  #finds all elements of type variable
		
			for variable in variableset:
				if variable.attrib['name'] == 'h':
					for statistic in variable.getchildren():
						if statistic.attrib['name'] == 'avg':
							rgbelement = statistic.findall('rgb')[0]
							self.my_dict['hue'] = rgbelement.text
				if variable.attrib['name'] == 's':
					for statistic in variable.getchildren():
						if statistic.attrib['name'] == 'avg':
							rgbelement = statistic.findall('rgb')[0]
							self.my_dict['saturation'] =  rgbelement.text
				if variable.attrib['name'] == 'v':
					for statistic in variable.getchildren():
						if statistic.attrib['name'] == 'avg':
							rgbelement = statistic.findall('rgb')[0]
							self.my_dict['value'] =  rgbelement.text
		
		
		

			#4. Convert the dictionary to JSON and return it to user
			#self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
			#my_json = json.dumps(self.my_dict)
			#self.response.out.write(my_json)
			return self.my_dict
		
"""
app = webapp.WSGIApplication([('/api', ColorOfWordsAPI)], debug=True)

def main():
	run_wsgi_app(app)

if __name__ == '__main__':
	main()
"""
