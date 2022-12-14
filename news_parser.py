import requests
from bs4 import BeautifulSoup

import asyncio
import aiohttp


async def get_site_page(link):
	async with aiohttp.ClientSession() as session:
		async with session.get(link) as resp:
			response =  await resp.text()

	soup = BeautifulSoup(response, 'lxml')

	return soup


async def get_last_news_block(soup):
	block = soup.find(class_="landingPagePrimaryFeature")
	block = block.find(class_="presentationIntent-desktop")
	return block


async def get_img(block):
	img_block = block.find(class_="syn-img pnr")

	return img_block.find("img")["src"]


async def get_title(block):
	title_block = block.find(class_="syn-body pnr")

	title = title_block.find("h3").text
	return title


async def get_url(block, source_link):
	url_block = block.find(class_="syn-body pnr")
	url = source_link + url_block.find("a")["href"]

	return url


async def get_introduction(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			response =  await resp.text()

	content_page = BeautifulSoup(response, 'lxml')

	content_block = content_page.find(class_="contentBody")
	intro = "\n" + content_block.find(class_="p2").text + "\n\n" + content_block.find(class_="p3").text

	return intro


async def get_dict(source_link, link):
	soup = await get_site_page(link)
	block = await get_last_news_block(soup)
	img = await get_img(block)
	title = await get_title(block)
	url = await get_url(block, source_link)
	intro = await get_introduction(url)

	list_item = [img, title, url, intro]
	return list_item


async def parse():
	source_link = 'https://www.jw.org'
	link = 'https://www.jw.org/ro/stiri/jw/'

	dict_news = await get_dict(source_link, link)

	img = dict_news[0]
	title = dict_news[1]
	url = dict_news[2]
	introduction = dict_news[3]

	dict_news = {"img": img, "title": title.strip(), "intro": introduction, "url": url}

	return dict_news






import os
import sqlite3
def get_list_users():
	conn = sqlite3.connect('data.db')
	conn.row_factory = lambda cursor, row: row[0]
	cur = conn.cursor()
	cur.execute(f'SELECT * FROM users')
	result = cur.fetchall()
	
	conn.close()
	return result



if __name__ == "__main__":
	if not os.path.exists("data.db"):
		conn = sqlite3.connect('data.db')
		cur = conn.cursor()
		cur.execute('CREATE TABLE users(user_id INTEGER, username TEXT)')
		conn.close()

	list_users = get_list_users()
	print(list_users)
	if not 749333822 in list_users:

		try:
			conn = sqlite3.connect('data.db')
			cur = conn.cursor()
			cur.execute(f'INSERT INTO users VALUES("{749333822}", "@{"andyrei"}")')
			conn.commit()
			conn.close()
		except Exception as e:
			print(e)
			conn = sqlite3.connect('data.db')
			cur = conn.cursor()
			cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}")')
			conn.commit()
			conn.close()


