import requests
from bs4 import BeautifulSoup

"""
TODO

	BOOT!!!!!!
"""

class ParserSite:
	def __init__(self, source_link, link):
		self.source_link = source_link
		self.link = link
		self.get_site_page()
		self.get_last_news_block()

	def get_site_page(self):
		response = requests.get(self.link)
		self.soup = BeautifulSoup(response.text, 'lxml')


	def get_last_news_block(self):
		block = self.soup.find(class_="landingPagePrimaryFeature")
		self.block = block.find(class_="presentationIntent-desktop")


	def get_img(self):
		img_block = self.block.find(class_="syn-img pnr")

		return img_block.find("img")["src"]


	def get_title(self):
		title_block = self.block.find(class_="syn-body pnr")

		return title_block.find("h3").text


	def get_url(self):
		url_block = self.block.find(class_="syn-body pnr")
		self.url = self.source_link + url_block.find("a")["href"]

		return self.url

	def get_introduction(self):
		response = requests.get(self.url)
		content_page = BeautifulSoup(response.text, 'lxml')
		content_block = content_page.find(class_="contentBody")
		intro = "\n" + content_block.find(class_="p2").text + "\n\n" + content_block.find(class_="p3").text

		return intro



async def parse():
	source_link = 'https://www.jw.org'
	link = 'https://www.jw.org/ro/stiri/jw/'

	parser_site = ParserSite(source_link, link)

	page = parser_site.get_site_page()
	last_news_block = parser_site.get_last_news_block()

	img = parser_site.get_img()
	title = parser_site.get_title()
	url = parser_site.get_url()
	introduction = parser_site.get_introduction()

	dict_news = {"img": img, "title": title.strip(), "intro": introduction, "url": url}

	return dict_news


if __name__ == "__main__":
	response = parse()
	print("IMG = ", response["img"])
	print("Title = ", response["title"])
	print("intro = ", response["intro"])
	print("URL = ", response["url"])

