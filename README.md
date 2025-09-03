# Welcome to the Spider's lair!
```
           ____                      ,
          /---.'.__             ____//
               '--.\           /.---'
          _______  \\         //
        /.------.\  \|      .'/  ______
       //  ___  \ \ ||/|\  //  _/_----.\__
      |/  /.-.\  \ \:|< >|// _/.'..\   '--'
         //   \'. | \'.|.'/ /_/ /  \\
        //     \ \_\/" ' ~\-'.-'    \\
       //       '-._| :H: |'-.__     \\
      //           (/'==='\)'-._\     ||
      ||                        \\    \|
      ||                         \\    '
      |/                          \\
                                   ||
                                   ||
                                   \\
                                    '
```

## This is a webscraper built using python
Crawl sites and scrap for specific data to report on.

## Instructions
Run the main.py file with 3 arguments:
1. The URL you wish to crawl
2. The maximum number of concurrent pages to process
3. The maximum total number of web pages/urls to crawl


Template: ```python 3 main.py <URL> <max concurrent> <max total>```

Example: ```python 3 main.py https://wikipedia.org 5 40```

###### Project Dependancies:
1. aiohttp
2. asyncio
3. BeautifulSoup
4. urllib