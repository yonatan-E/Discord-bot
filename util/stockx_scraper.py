from selenium import webdriver
from bs4 import BeautifulSoup

class stockx_scraper:

	def __init__(self, page_finder, page_scraper):
		self.__page_finder = page_finder
		self.__page_scraper = page_scraper

	def get_product_json(self, product):
		product_page = self.__page_finder.get_product_page(product)
		return self.__page_scraper.scrape_product_page(product_page)

class stockx_page_scraper:

	def scrape_product_page(self, product_page):
		soup = BeautifulSoup(product_page, 'lxml')

		product_json = {}

		product_json['product-name'] = soup.find('h1', attrs={'data-testid' : 'product-name'}).text

		bids = soup.find_all('div', class_='en-us stat-value stat-small css-k008qs')
		product_json['lowest-bid'] = bids[0].text
		product_json['highest-bid'] = bids[1].text

		product_json['last-sale'] = soup.find('div', class_='sale-value').text
		product_json['retail-price'] = soup.find('span', attrs={'data-testid' : 'product-detail-retail price'}).text
		product_json['release-date'] = soup.find('span', attrs={'data-testid' : 'product-detail-release date'}).text

		product_json['image-url'] = soup.find('img', attrs={'data-testid' : 'product-detail-image'})['src']

		product_json['prices'] = {}
		for item in soup.find_all('div', class_='inset css-8atqhb'):
			try:
				size = int(item.find('div', class_='title').text[3:])
				price = item.find('div', class_='subtitle').text
				product_json['prices'][size] = price
			except:
				pass

		return product_json

class stockx_page_finder:

	STOCKX_URL = 'https://stockx.com'

	def get_product_page(self, product):
		
		WEBDRIVER_PATH = '/home/yonatan/Projects/geckodriver'

		options = webdriver.FirefoxOptions()
		options.headless = True
		options.add_argument('--disable-blink-features=AutomationControlled')
		web_driver = webdriver.Firefox(executable_path=WEBDRIVER_PATH, options=options)

		web_driver.get(f'{self.STOCKX_URL}/search?s={product.replace(" ", "%20")}')
		soup = BeautifulSoup(web_driver.page_source, 'lxml')
		url = soup.find('div', class_='tile css-yrcab6-Tile e1yt6rrx0').a['href']
		web_driver.get(self.STOCKX_URL + url)

		product_page = web_driver.page_source

		web_driver.quit()

		return product_page