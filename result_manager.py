import time
from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException
from webdriver_manager.chrome import ChromeDriverManager


def search_song_url(artist, title):
    song_url = ''
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--disable-gpu')

        # driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = 'https://www.youtube.com/results?search_query=' + title + '+' + artist

        driver.get(url=url)
        driver.implicitly_wait(time_to_wait=1)
        time.sleep(0.5)

        xpath = '//*[@id="video-title"]'
        song_url = driver.find_element_by_xpath(xpath).get_attribute('href')
    except InvalidSelectorException:
        print('Invalid selector. Please select other selector!')
        song_url = '-'
    finally:
        driver.quit()

    return song_url


if __name__ == "__main__":
    print(search_song_url('거북이', '비행기'))
