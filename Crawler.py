#coding=utf-8
#==================================================import============================================================
#import urllib.parse
#import urllib.request
#import urllib.error

#import codecs
#import http.cookiejar
import re
import datetime
#import pymysql

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time
import os
import string
from selenium import webdriver
from splinter import Browser
from itertools import islice


def splinter_zhaogang(url):
	executable_path = {'executable_path': '/usr/local/Cellar/chromedriver/2.25/bin/chromedriver'}
	browser = Browser('chrome', **executable_path)
	browser.visit(url)
    # wait web element loading
	time.sleep(1)
    # fill in account and password
	browser.find_by_id('txt_loginmobile').fill('18610111868')
	browser.find_by_id('txt_loginpwd').fill('jiangmm0702')
    # click the button of login
	browser.find_by_id('btn_login').click()
	time.sleep(3)
	browser.find_by_id('head_mall').click()
	time.sleep(3)
	# selects = []
	windows = []

	windows = browser.windows
	# print(len(windows))

	browser.windows.current = browser.windows[1]

	# Parse the html of the page
	html = browser.html
	# print(html)
	soup = BeautifulSoup(html)

	# Get all districts
	select_districts = soup.find_all('select', attrs={'id':'selWarehouseCtiy'})[0]
	districts = []
	for district in select_districts.find_all('option'):
		if district.text == '全国':
			continue
		else:
			districts.append([district.text,district['value']])
	print(districts)

	# '中天', '三级抗震螺纹钢', 'HRB400E', '28*9', '上海淞铁库(上海)', '4', '2.000', '8.000', '2940', '上海市'
	column_name = ['Factory', 'ItemName', 'Material', 'Type', 'Warehouse', 'Quantity', 'WeightPerUnit', 'TotalWeight', 'Price', 'District', 'Date', 'Platform']
	# df_result = pd.DataFrame(columns=columns)
	df_result = pd.DataFrame()

	now = datetime.datetime.now()

	# Iterate the districts
	for district in districts:
		# Selecting option for the selects without name
		# browser.find_by_xpath('//select[@id="selWarehouseCtiy"]/option[@value="310100"]')._element.click()

		str_par = '//select[@id="selWarehouseCtiy"]/option[@value="{0}"]'.format(int(district[1]))
		# browser.find_by_xpath('//select[@id="selWarehouseCtiy"]/option[@value=@district]')._element.click()
		browser.find_by_xpath(str_par)._element.click()
		browser.find_by_id('btnSearch').click()
		time.sleep(3)

		html = browser.html
		# print(html)
		soup = BeautifulSoup(html)

		# Total Pages
		ls_total_page = soup.find_all('span', attrs={'class': 'total'})
		if len(ls_total_page) > 0:
			total_page = int(soup.find_all('span', attrs={'class':'total'})[0].get_text()[2:-2])

			if total_page > 0:
				# Iterate every page in each district
				for page in range(1,total_page + 1):
					html = browser.html
					# print(html)
					soup = BeautifulSoup(html)
					table = soup.find_all('table', id="goodlist")

					for row in table[0].find_all('tr')[3:]:
						row_result = []
						columns = row.find_all('td')
						for column in columns[0:9]:
							row_result.append(column.get_text())
						# Add the district name
						row_result.append(district[0])
						row_result.append(now.strftime("%Y%m%d %H:%M"))
						row_result.append('找钢网平台')
						# table_result.append(row_result)
						print(row_result)
						df_result = df_result.append(pd.Series(row_result), ignore_index=True)
						# print(df_result)

					# print(new_table)
					browser.find_by_text('下一页')[0].click()
					time.sleep(2)
					# selects = browser.find_by_id('selWarehouseCtiy')
					# print(len(selects))
	df_result.columns = column_name
	print(df_result)

	current_dir = os.getcwd()
	# file_zhaogang = open(current_dir + '\\zhaogang.csv', 'w')
	file_name = current_dir + '/zhaogang.csv'
	# file_zhaogang.write(df_result)
	# df_result.to_csv(file_name, index=False, encoding='utf-8')
	df_result.to_csv(file_name, index=False, encoding = "gb2312")

	#browser.find_by_class_name('group-bins').select('Aisle')
	#browser.find_by_value('Submit').click()
	#browser.find_by_type('submit').click()
	#buttons = browser.find_by_tag('button')


def splinter_gangying(url):
	executable_path = {'executable_path': '/usr/local/Cellar/chromedriver/2.25/bin/chromedriver'}
	browser = Browser('chrome', **executable_path)
	browser.visit(url)
    # wait web element loading
	time.sleep(1)
    # fill in account and password
	browser.find_by_id('uname').fill('18610111868')
	browser.find_by_id('psw').fill('jiangmm0702')
    # click the button of login
	browser.find_by_id('button').click()
	time.sleep(3)
	browser.visit('http://chaoshi.banksteel.com/')

	# windows = []

	# windows = browser.windows
	# print(len(windows))

	# browser.windows.current = browser.windows[1]

	# Parse the html of the page
	html = browser.html
	# print(html)
	soup = BeautifulSoup(html)

	# ['三级螺纹钢', 'Φ10*12', 'HRB400', '永钢', '张家港', '永钢厂提', '2', '-', '3.998', '3040', '20161122 17:04', '钢赢网平台']
	column_name = ['ItemName', 'Type', 'Material', 'Factory', 'District', 'Warehouse', 'Quantity', 'WeightPerUnit', 'TotalWeight', 'Price', 'Date', 'Platform']
	# df_result = pd.DataFrame(columns=columns)
	df_result = pd.DataFrame()

	now = datetime.datetime.now()

	# Total Pages
	ls_total_page = soup.find_all('span', attrs={'id': 'totalSpan'})
	if len(ls_total_page) > 0:
		total_page = int(soup.find_all('span', attrs={'id':'totalSpan'})[0].get_text())
		if total_page > 0:
			# Iterate every page in each district
			for page in range(1,total_page + 1):
				html = browser.html
				# print(html)
				soup = BeautifulSoup(html)
				table = soup.find_all('table', id="resList")

				for row in table[0].find_all('tr')[2:]:
					count = 0
					row_result = []
					columns = row.find_all('td')
					if len(columns) > 0:
						for column in columns[0:10]:
							if count == 0 or count == 5:
								column_item = column.find_all('a')[0].get_text()
								row_result.append(column_item)
							else:
								row_result.append(column.get_text())
							count += 1
						# Add the district name
						row_result.append(now.strftime("%Y%m%d %H:%M"))
						row_result.append('钢赢网平台')
						# table_result.append(row_result)
						print(row_result)
						df_result = df_result.append(pd.Series(row_result), ignore_index=True)

						if page == 50:
							current_dir = os.getcwd()
							# file_zhaogang = open(current_dir + '\\zhaogang.csv', 'w')
							file_name = current_dir + '/gangying.csv'
							# file_zhaogang.write(df_result)
							# df_result.to_csv(file_name, index=False, encoding='utf-8')
							df_result.to_csv(file_name, index=False, encoding="gb2312")
						elif page > 50 and page%50 == 0:
							current_dir = os.getcwd()
							# file_zhaogang = open(current_dir + '\\zhaogang.csv', 'w')
							file_name = current_dir + '/gangying.csv'
							with open(file_name, 'a') as f:
								df_result.to_csv(f, index=False, encoding="gb2312", header=False)
						elif page == total_page:
							current_dir = os.getcwd()
							# file_zhaogang = open(current_dir + '\\zhaogang.csv', 'w')
							file_name = current_dir + '/gangying.csv'
							with open(file_name, 'a') as f:
								df_result.to_csv(f, index=False, encoding="gb2312", header=False)

					# print(df_result)

				# print(new_table)
				browser.find_by_text('下一页')[0].click()
				time.sleep(1)
				# selects = browser.find_by_id('selWarehouseCtiy')
				# print(len(selects))
		df_result.columns = column_name
		print(df_result)

	#browser.find_by_class_name('group-bins').select('Aisle')
	#browser.find_by_value('Submit').click()
	#browser.find_by_type('submit').click()
	#buttons = browser.find_by_tag('button')


def test():
	now = datetime.datetime.now()

	df = pd.DataFrame()
	df = df.append(pd.Series(['中天', '三级抗震螺纹钢', 'HRB400E', '28*9', '上海淞铁库(上海)', '4', '2.000', '8.000', '2940', '上海市']), ignore_index=True)
	df = df.append(pd.Series(['大大', '四级抗震螺纹钢', 'HRB400E', '28*9', '上海淞铁库(上海)', '4', '2.000', '8.000', '2940', '北京市']), ignore_index=True)
	print(df)
	current_dir = os.getcwd()
	file_name = current_dir + '/zhaogang' + now.strftime("%Y%m%d") + '.csv'
	df.to_csv(file_name, index=False, encoding="gb2312")



if __name__ == '__main__':
	# nr_pages = 0
	# page_info = []
	# finish = 0
	zhaogang_url ='https://member.zhaogang.com/Member/Login?Jump=http://www.zhaogang.com/'
	gangying_url = 'http://login.banksteel.com/login.htm?mybackurl=http://www.banksteel.com/'
	
	#current_dir = os.path.split(os.path.realpath(__file__))[0]
	# current_dir = os.getcwd()
	# file = open(current_dir + '\\receiver.csv','w')
	# file_name = current_dir + '\\receiver.csv'
	# print("File {0} has been opened for write.".format(file_name))
	# file.write('AISLE,%USABLE_SPACE,USABLE_SPACE,%EMPTY_LINEAR_SPACE,EMPTY_BINS,%BINS_NOT_AT_ASIN_LIMIT,TOTAL_BINS,%UTILIZATION,%TO_MAX_UNIQUE_ASINS,SPACE_WASTED_BY_ASIN_LIMIT(%)\n')
	#
	# while (finish == 0):
	try:
		# splinter_zhaogang(zhaogang_url)
		splinter_gangying(gangying_url)
		# test()
	except Exception as e:
		print(str(e))
	
	# file.close()
	# print("Total {0} pages are downloaded. Data Download Finished!".format(nr_pages))
			#write_log(file_name = 'Log', message = msg + str(e))

