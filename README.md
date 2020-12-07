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

#### Data Model

#### Crawler

### Twitter Data Processor

#### Exploratory Data Analysis (EDA)

#### Sentiment Analysis


### API Definition and Structure

### Frontend UI and UX Design