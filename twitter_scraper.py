"""twitter_scraper.py requires selenium and your browser's corresponding webdriver"""
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome

number_of_reloads = 40 # This tells script how many times you reload the page (while scrolling down, essentially how far you go down)

"""Login Info"""
my_password = 'matt101010' # Use yall own login info if we end up using this on our own computers
my_username_or_email = 'mattanatorisms@gmail.com'

"""Dictionary of scraped tickers"""
tickers = {}
posts = []

"""Load Functions"""
def parseText(words):
    """Split text by word (all symbols except '.' for ticker scraping purposes)"""
    text = words.replace(',', '').\
        replace('?', '').replace('!', '').\
        replace('&', '').replace('-', '').\
        replace('_', '').split(' ')
    """Trying to make exceptions for tickers mentioned as 'VST.CN' so we can incorporate '.' in parser"""
    # for word in text:
    #     text
    #     while word[-1] == '.':
    #         index = text.index(word)
    #         new_word = word[:-1]
    #         text[index] = new_word
    return text

def getTickers():
    """Extract tickers from current page"""
    reject_chars = set(",.<>/?'!;:[{]}}]-_=+@#%^&*()1234567890`~")
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards[-15:]:
        try:
            post = card.find_elements_by_xpath('./div[2]/div[2]/div[1]/div[1]')[0]
            if post not in posts:
                posts.append(post)
                ticker_extensions = ['.CN', '.V', '.TO']
                for hashtag_or_cashtag in post.find_elements_by_class_name('r-18u37iz'):
                    try:
                        if hashtag_or_cashtag.text[0] == '$': # If pulled word is cashtag
                            cashtag = hashtag_or_cashtag.text.upper()
                            current_tickers = tickers # for reference later on
                            if len(cashtag) >= 3 and len(cashtag) <= 8: # There are tickers with one letter but so few to matter e.g. len($NM):len($VSBY.CN)_
                                try:
                                    tickers[cashtag] += 1 # if ticker is already in tickers try to add 1
                                except: # if no ticker in tickers, returns error and moves along
                                    for extension in ticker_extensions: # for extension ('.CN') in ticker extensions check if its in cashtag
                                        if extension in cashtag:
                                            parsed_ticker = cashtag.split(extension)[0] # if extension is in, grab the root ticker symbol (w/out extension)
                                            try:
                                                tickers[parsed_ticker] += 1 # try add if already in
                                            except:
                                                tickers[parsed_ticker] = 1 # else add new
                                    if current_tickers == tickers:
                                        tickers[cashtag] = 1
                        if hashtag_or_cashtag.text[0] == '#':  # If pulled word is hashtag
                            cashtag = hashtag_or_cashtag.text.upper().replace('#', '$') # make cashtag, because were dealing with many words, need to find way to isolate tickers. could compare to database of all tickers
                            current_tickers = tickers  # for reference later on
                            if cashtag in tickers.keys():
                                tickers[cashtag] += 1
                            else:
                                for extension in ticker_extensions:
                                    if extension in cashtag:
                                        parsed_ticker = '$' + cashtag.split(extension)[0]
                                        try:
                                            tickers[parsed_ticker] += 1
                                        except:
                                            tickers[parsed_ticker] = 1
                                # if current_tickers == tickers:
                                # if cashtag.count('$') > 1:
                    except Exception as err:
                        print(err, 'poo')
                try:
                    text = post.text.upper()
                    for word in parseText(text):
                        if len(word) >= 3 and len(word) <= 8: # There are tickers with one letter but so few to matter
                            if word.count('$') == 1:    # Omit phrases like '$$$'
                                if '$' == word[0]:      # grab tickers formatted like '$VST'
                                    if word in tickers.keys(): # if in tickers, add to ticker count
                                        tickers[word] += 1
                                    elif not any((c in reject_chars) for c in word): # if only letters in word, add to tickers
                                        tickers[word] = 1
                                    else:
                                        for extension in ticker_extensions:
                                            if extension in word: # if word has ticker extension, remove extension and add to tickers
                                                parsed_ticker = word.split(extension)[0] # grab ticker root, remove extension
                                                try:
                                                    tickers[parsed_ticker] += 1
                                                except:
                                                    tickers[parsed_ticker] = 1
                            if '$' + word in tickers.keys():
                                tickers['$' + word] += 1
                except Exception as err:
                    print(err, 'p')
        except Exception as err:
            print(err, 'o')


### Running Bot ###

"""Open Chrome"""
driver = Chrome('/usr/local/bin/chromedriver')
driver.get('http://twitter.com/login')
sleep(3)

"""Login"""
username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys(my_username_or_email)
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)
sleep(3)

"""Load stocks discussions"""
driver.get('http://twitter.com/explore')
sleep(3)
search_text = '($BUY OR stocks) -sell -bear (#stocks OR #pennystocks)'
search_bar = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
search_bar.send_keys(search_text)
search_bar.send_keys(Keys.RETURN)
sleep(3)
driver.find_element_by_link_text('Latest').click()
sleep(3)

"""Begin ticker scraping"""
for i in range(number_of_reloads):
    getTickers()
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(1)
