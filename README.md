# PowerDNS-Admin Scraping

PowerDns-Admin is a web interface that helps to manage a PowerDNS service. 
This tools aims to get informations about a dns zone in scraping the web page.


## Usage

Clone the repository and execute the following commands:

``` 
psa-scraping $ virtualenv .venv
psa-scraping $ source .venv/bin/activate
(.venv) psa-scraping $ pip install -r requirements.txt
(.venv) psa-scraping $ cp settings.json{.example,}
(.venv) psa-scraping $ python psa-scraping.py
```

