from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import threading
import time
import csv
from urllib.parse import urlparse, urljoin
import math

SLEEP_TIME = 0.5

def download_selenium(url, num_retries=3):

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
    except:
        if num_retries > 0:
            driver.close()
            download_selenium(url, num_retries-1)

    return driver

class glassdoor_scraper():
    def __init__(self, url):
        self.start_url = url

        filename = urlparse(self.start_url).path
        filename = filename.split('/')[2].split('-')[0]
        filename = filename + '.csv'
        self.output_file = open(filename, 'w', encoding='utf-8', newline='')
        self.writer = csv.writer(self.output_file)
        headers = ['Title', 'Rating', 'Review Date', 'Current/Past Employee', 'Employee Title',
                   'location', 'Recommends (Y/N)', 'Positive Outlook (Y/N)', 'Approves of CEO (Y/N)',
                   'Full-Time/ Part-Time', 'Time Employed',	'Pros', 'Cons', 'Advice to Management']
        self.writer.writerow(headers)

        self.total_page_links = []

    def firstpage_parsing(self):

        driver = download_selenium(self.start_url)
        reviews_cnt = driver.find_elements_by_class_name('noPadLt')[0].text
        reviews_cnt = reviews_cnt.split('\n')[0].split(' ')[0]
        if ',' in reviews_cnt:
            reviews_cnt = reviews_cnt.replace(',', '')
        reviews_cnt = int(reviews_cnt)
        pages_cnt = math.ceil(reviews_cnt/10)
        #print(reviews_cnt, pages_cnt)
        #print(driver.page_source)

        for i in range(1, pages_cnt+1):
            link = self.start_url.split('.')
            link[-2] = link[-2] + '_P{}'.format(i)
            link = '.'.join(link)
            #print(link)
            self.total_page_links.append(link)

        self.total_page_links.reverse()
        driver.close()

    def eachpage_parsing(self):
        url = self.total_page_links.pop()
        print(url)

        driver = download_selenium(url)

        try:
            more_links = driver.find_elements_by_css_selector('span.link.moreLink')

            for more_link in more_links:
                more_link.click()
        except:
            pass

        hreviews = driver.find_elements_by_css_selector('div.hreview')

        titles = []
        ratings = []
        review_dates = []
        current_past_employees = []
        employee_titles = []
        locations = []
        recommends = []
        positive_outlooks = []
        approves_ceos = []
        full_time_part_times = []
        time_employeds = []
        pros = []
        cons = []
        advice_to_managements = []

        for hreview in hreviews:
            title = ''
            rating = ''
            current_past_employee = ''
            employee_title = ''
            location = ''
            recommend = ''
            outlook = ''
            ceo = ''
            time_employed = ''
            pro = ''
            con = ''
            advice_to_management = ''

            try:
                title = hreview.find_element_by_css_selector('span.summary').text
                #titles.append(title.text)
            except:
                #titles.append('')
                pass

            viewmeta = hreview.find_element_by_css_selector('div.tbl.reviewMeta')
            try:
                rating = viewmeta.find_element_by_css_selector('span.value-title').get_attribute('title')
                #ratings.append(rating.get_attribute('title'))
            except:
                #ratings.append('')
                pass

            try:
                review_date = hreview.find_element_by_css_selector('time.date.subtle.small').get_attribute('datetime')
                # ratings.append(rating.get_attribute('title'))
            except:
                # ratings.append('')
                pass

            try:
                author = viewmeta.find_element_by_css_selector('div.author.minor.tbl')
                authorJobTitle = author.find_element_by_css_selector('span.authorJobTitle.middle.reviewer').text.split('-')
                if len(authorJobTitle) == 2:
                    #current_past_employees.append(authorJobTitle[0])
                    #employee_titles.append(authorJobTitle[1])
                    current_past_employee = authorJobTitle[0]
                    employee_title = authorJobTitle[1]
                else:
                    current_past_employee = authorJobTitle[0]

                try:
                    #locations.append(author.find_element_by_css_selector('span.authorLocation.middle').text)
                    location = author.find_element_by_css_selector('span.authorLocation.middle').text
                except:
                    #locations.append('')
                    pass

            except:
                pass



            try:
                flex_grids = hreview.find_element_by_css_selector('div.flex-grid.recommends').find_elements_by_css_selector('span.middle')
                #print(hreview.find_element_by_css_selector('div.flex-grid.recommends').text)

                for flex_grid in flex_grids:
                    temp = flex_grid.text
                    if 'Recommend' in temp:
                        recommend = temp

                    if 'Outlook' in temp:
                        outlook = temp

                    if 'CEO' in temp:
                        ceo = flex_grid.find_element_by_css_selector('span.showDesk').text + ' CEO'
                        #print(ceo)

            except:
                pass

            try:
                time_employed = hreview.find_element_by_css_selector('p.tightBot.mainText').text
            except:
                pass

            truncateData = hreview.find_element_by_css_selector('div.tbl.fill.prosConsAdvice.truncateData')


            try:
                #pros.append(truncateData.find_element_by_css_selector('p.pros.mainText.truncateThis.wrapToggleStr').text)
                pro = truncateData.find_element_by_css_selector('p.pros.mainText.truncateThis.wrapToggleStr').text
            except:
                #pros.append('')
                pass
            try:
                #cons.append(truncateData.find_element_by_css_selector('p.cons.mainText.truncateThis.wrapToggleStr').text)
                con = truncateData.find_element_by_css_selector('p.cons.mainText.truncateThis.wrapToggleStr').text

            except:
                #cons.append('')
                pass

            try:
                #advice_to_managements.append(truncateData.find_element_by_css_selector('p.adviceMgmt.mainText.truncateThis.wrapToggleStr').text)
                advice_to_management = truncateData.find_element_by_css_selector('p.adviceMgmt.mainText.truncateThis.wrapToggleStr').text

            except:
                #advice_to_managements.append('')
                pass

            titles.append(title)
            ratings.append(rating)
            review_dates.append(review_date)
            current_past_employees.append(current_past_employee)
            employee_titles.append(employee_title)
            locations.append(location)
            recommends.append(recommend)
            positive_outlooks.append(outlook)
            approves_ceos.append(ceo)
            full_time_part_times.append(current_past_employee)
            time_employeds.append(time_employed)
            pros.append(pro)
            cons.append(con)
            advice_to_managements.append(advice_to_management)

        '''
        print('titles: ', titles)
        print('ratings: ', ratings)
        print('review_dates: ', review_dates)
        print('current_past_employees: ', current_past_employees)
        print('employee_titles: ', employee_titles)
        print('locations: ', locations)
        print('recommends: ', recommends)
        print('positive_outlooks: ', positive_outlooks)
        print('approves_ceos: ', approves_ceos)
        print('full_time_part_times: ', full_time_part_times)
        print('time_employeds: ', time_employeds)
        print('pros: ', pros)
        print('cons: ', cons)
        print('advice_to_managements: ', advice_to_managements)
        '''

        driver.close()

        for i in range(len(titles)):
            row = [titles[i], ratings[i], review_dates[i], current_past_employees[i], employee_titles[i],
                   locations[i], recommends[i], positive_outlooks[i], approves_ceos[i], full_time_part_times[i],
                   time_employeds[i], pros[i], cons[i], advice_to_managements[i]]
            self.writer.writerow(row)

    def total_pages_parsing(self):
        self.threads = []
        self.max_threads = 5

        while self.threads or self.total_page_links:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)

            while len(self.threads) < self.max_threads and self.total_page_links:
                thread = threading.Thread(target=self.eachpage_parsing)
                thread.setDaemon(True)
                thread.start()
                self.threads.append(thread)

            time.sleep(SLEEP_TIME)

        self.output_file.close()

if __name__ == '__main__':
    app = glassdoor_scraper('https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202.htm')
    app.firstpage_parsing()
    app.total_pages_parsing()