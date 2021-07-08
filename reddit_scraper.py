import praw

def scrape_reddit():
    """Individual Credentials"""
    # In final product, obtain these variables from main script/gui
    client_id = 'ktRlJUIQO8Hw_g'
    client_secret = 'APyndeyhsU_nQ3kySSkfOLYTGRz1XQ'
    user_agent = 'StockBot'


    r = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subreddits = ['pennystocks', 'CanadianInvestor', 'wallstreetbets', 'Investing', 'Stocks', 'StockMarket']
    tickers = {}
    reject_chars = set(",<>./?'!;:[{]}}]-_=+@#%^&*()1234567890`~")


    """Retreive tickers mentioned that start with a '$' (e.g. $VST)"""
    limit = 5
    for subreddit in subreddits:
        for post in r.subreddit(subreddit).hot(limit=limit):
            for comments in post.comments:
                try:
                    for word in comments.body.split(' '):
                        try:
                            if len(word) > 2 and len(word) < 10:
                                if "$" == word[0] and word.count('$') == 1:
                                    if not any((c in reject_chars) for c in word):
                                        try:
                                            tickers[word] += 1
                                        except:
                                            tickers[word] = 1
                        except:
                            pass
                except:
                    pass
            for word in post.title.split(' '):
                try:
                    if len(word) > 2 and len(word) < 10:
                        if "$" == word[0] and word.count('$') == 1:
                            if not any((c in reject_chars) for c in word):
                                try:
                                    tickers[word] += 1
                                except:
                                    tickers[word] = 1
                except:
                    pass


    tickers_letters_only = [ticker.upper().replace('$', '') for ticker in list(tickers.keys())]


    """Check if tickers mentioned in comments without '$' (e.g. VST, TSLA, aapl)"""
    for subreddit in subreddits:
        for post in r.subreddit(subreddit).hot(limit=limit):
            for comment in post.comments:
                try:
                    for word in comment.body.split(' '):
                        if word.upper() in tickers_letters_only:
                            try:
                                tickers[('$' + word.upper())] += 1
                            except:
                                pass
                except:
                    pass

    tickers_letters_only = [ticker.upper().replace('$', '') for ticker in list(tickers.keys())]
    return tickers