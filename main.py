import snscrape.modules.twitter as sntwitter
import snscrape.modules.reddit as snreddit
import pandas as pd
pd.set_option('display.max_colwidth', None)
import flair

VALID_SOCIAL_MEDIA = {'twitter', 'reddit'}

class CalculateScore():
    def scrapper(query, site):
        if site in VALID_SOCIAL_MEDIA:
            lst = []
            scraper = None


            # Implement pushshift for reddit scrape
            if site == 'twitter':
                scraper = sntwitter.TwitterSearchScraper(query)
            else:
                scraper = snreddit.RedditSearchScraper(query)

            for i, tweet in enumerate(scraper.get_items()):
                if i > 1000:
                    break
                lst.append(tweet.rawContent)

            df = pd.DataFrame(lst)

            return df
            
        else:
            raise ValueError("twitter_scraper: site argument must be one of %r." % VALID_SOCIAL_MEDIA)


    def sentiment_analysis(query, df):
        
        sentiment_model = flair.models.TextClassifier.load('en-sentiment')
        positive_count = 0
        total_count = 0

        sentiment = []
        confidence = []

        for excerpt in df[0]:
            if not excerpt.strip() == '':
                
                sample = flair.data.Sentence(excerpt)
                sentiment_model.predict(sample)

                sentiment.append(sample.labels[0].value)
                confidence.append(sample.labels[0].score)

                if sample.labels[0].score >= 0.9:
                    
                    if sample.labels[0].value == 'POSITIVE':
                        positive_count += 1
                    
                    total_count += 1

        df['sentiment'] = sentiment
        df['confidence'] = confidence

        score = (positive_count / total_count) * 100

        return score

q = 'avengers endgame movie review lang:en -filter:links'