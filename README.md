# TheGreatSpaceRace
The "Great Space Race" is a small project intended to incorporate web scraping, data analysis and graph plotting into one signle web application.
The 'scraper_past.py' and 'scraper_upcoming.py' files serve as integral components of our web scraping process. 'scraper_past.py' leverages Selenium libraries to extract data, while 'scraper_upcoming.py' utilizes Flask and Sqlalchemy libraries to create a new database and seamlessly store the scraped data within it. Together, these scripts enable us to efficiently collect and manage web data for our project.

(all of the original data can be found at https://nextspaceflight.com/launches/)

In 'main.py,' we access both databases, integrating and presenting all pertinent data on a web page. This dynamic presentation is achieved through the utilization of Flask and Plotly, enabling a user-friendly interface to explore and interact with the collected information.
