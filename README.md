# IND ENG 135 Final Project

## Volvo Social Media Analyzer - Twitter

Team Member:

- Xingyu Jin < xingyu.jin21@berkeley.edu >
- Mingyue Tang < mingyue_tang@berkeley.edu >
- Ruochen Liu < ruochen99@berkeley.edu >
- Ilene Kung < ilenekung@berkeley.edu >
- Yichu Chen < sterlingyichuchen@berkeley.edu >
- Neil Rabb < neil.rabb@berkeley.edu >

### Code Structure

```
.
|____data_processing_notebooks     # Previous versions of data processing functions in ipython notebook
|
|____full_stack_server             # Main functions rending final product (frontend + backend)
| |____dao                         # Data Access Objects
| | |____mysql_processor.py        # processor handling reading and writing to database
| | |____twitter_crawler.py        # real-time web crawler for obtaining Twitter Data
| | |____twitter_processor.py      # data processor to abstract storage layer and provide essential data upon request
| |
| |____handler                     # All handler functions dealing with main server logic
| | |____account_page_handler.py   # All functions related to handling account page API requests
| | |____mention_page_handler.py   # All functions related to handling mention page API requests
| |
| |____idl                         # Interface Description Language
| | |____service.proto             # ProtoBuf messages defining RPC services
| | |____view.proto                # ProtoBuf messages defining API request & response elements
| |
| |____pbgen                       # Serializer and structured data generated by ProtoBuf
| | |____service_pb2.py            
| | |____view_pb2.py
| |
| |____templates                   # Frontend Server Body handling styles and interaction functions
| |
| |____volvo_social_media_analyzer # Backend Server Body handling routings and requests
| | |____[__init__.py]             
| | |____settings.py               # Related Server settings for Django framework
| | |____urls.py                   # Router to handler HTTP requests
| | |____views.py                  # Request handling views
| | |____wsgi.py                   # Exposes the WSGI callable as a module-level variable
| |
| |____cronjob.py                  # Cronjob framework for keeping database updated
| |____manage.py                   # Main function to run server and listen to http requests
```

### Twitter Web Crawler

In order to bypass restrictions of Twitter API, such amount of tweets, QPS and time range, our crawler fetching the content directly from the HTML public pages, then parse the content we want. We built a pipeline to scrape, pre-preproces and output sentiment scores. We are using two main datasets, one includes all tweets about Volvo for 3 months (volvo701-1001.csv), one includes tweets from @VolvoCarUSA for 4 years(VolvoCarUSA.csv). 

### Twitter Data Processor

#### Data cleaning 

We start with filtering out ads. Our cleaning function removes mentions, punctuation, digits, stopwords and urls, changes emoji into one words, change letters to lowercase, and normalize text. 

#### Exploratory Data Analysis (EDA)

  ##### Tweets about Volvo: 
    1. Pie chart for main sources (geographically) 
    2. Major statistics (Num of tweets, retweets, likes, replies per day) 
    3. Time series : Daily and weekly tweet freq count 
    4. Histogram for Tweets sent by weekday and Tweets sent by hour of the day (in UTC) 
    6. Tweets that got top 10 retweeted/ repied/ liked 
    7. Bar chart for top active and influential users 
    8. wordcloud 
    
   ##### Tweets from Volvo: 
    1. Most mentioned users
    2. Most used hastags
    3. Tweets with most likes/ retweets/ replies 
 
 

#### Sentiment Analysis

First, we ranked the frequency of positive, neutral, and positive words with a labeled dataset. After deleting stop words, punctuations, and filler words, we were left with the most commonly appeared words from the three categories. Based on the frequency, we then assigned a specific score representing the strength/relevance of that word to a specific sentiment (positive: 0-1, neutral:0, negative:-1-0). Based on this logic, we utilized TextBlob to calculate subjectivity and polarity of each sentence and evaluate the sentiment of each tweet after EDA. We also added “slightly positive” and “slightly negative” to further classify tweets based on the magnitude of their sentiments, making it easier for the team to prioritize the most pressing issues in the Dashboard.

We grouped the tweets by car models that were provided by the mentors from Volvo. Then, by giving a sentiment score to every tweet in each group, Volvo will know that each car model’s feedback is positive or negative. We also group the tweets by country and analyze their sentiment scores, so Volvo knows which countries they need to target in order to improve its performance.

### API Definition and Structure

### Frontend UI and UX Design
