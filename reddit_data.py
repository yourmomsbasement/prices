import requests
import pandas as pd
import time
from datetime import datetime, timedelta

subreddits = ['CryptoCurrency', 'Bitcoin', 'ethtrader']
headers = {'User-Agent': 'crypto_research_bot/1.0'}
all_posts = []

for sub in subreddits:
    print(f"Pulling r/{sub}...")
    url = f'https://www.reddit.com/r/{sub}/top.json?t=all&limit=100'
    try:
        r = requests.get(url, headers=headers, timeout=15)
        posts = r.json()['data']['children']
        for p in posts:
            d = p['data']
            all_posts.append({
                'subreddit':    sub,
                'date':         datetime.fromtimestamp(d['created_utc']).date(),
                'score':        d['score'],
                'num_comments': d['num_comments'],
                'title':        d['title'],
            })
        print(f"  Got {len(posts)} posts")
        time.sleep(2)
    except Exception as e:
        print(f"  Error: {e}")

df = pd.DataFrame(all_posts)
daily = df.groupby(['date','subreddit']).agg(
    posts=('score','count'),
    total_score=('score','sum'),
    avg_comments=('num_comments','mean')
).reset_index()

daily.to_csv('reddit_data.csv', index=False)
print(f"Done! {len(df)} posts → {len(daily)} daily rows")
