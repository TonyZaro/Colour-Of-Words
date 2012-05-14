import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class IndexPage(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/page.html')
		html = template.render(path,{})
		self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', IndexPage)], debug=True)

def main():
	run_wsgi_app(app)

if __name__ == '__main__':
	main()