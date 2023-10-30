from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get('https://nextspaceflight.com/launches/')

all_names = []
all_owners = []
all_years = []
all_countries = []
all_details = []


new_timeout = 12


while new_timeout > 0:
    try:
        next_label = driver.find_element(By.XPATH,'/html/body/div/div/main/div/div[2]/div[2]/span/div/button[1]')
    except:
        # names
        names = driver.find_elements(By.CLASS_NAME,'header-style')
        for name in names:
            all_names.append(name.text)

            
         # details
        details = driver.find_elements(By.CLASS_NAME, 'mdl-card__supporting-text')
        for detail in details:
            all_details.append(detail.text.split(','))

        # owners
        owners = driver.find_elements(By.CLASS_NAME,'mdl-card__title-text')

        for owner in owners:
            all_owners.append(owner.text)
        
        driver.quit()
        break
    else:
        # names
        names = driver.find_elements(By.CLASS_NAME,'header-style')
        for name in names:
            all_names.append(name.text)

            
         # details
        details = driver.find_elements(By.CLASS_NAME, 'mdl-card__supporting-text')
        for detail in details:
            all_details.append(detail.text.split(','))

        # owners
        owners = driver.find_elements(By.CLASS_NAME,'mdl-card__title-text')

        for owner in owners:
            all_owners.append(owner.text)
    finally:
        new_timeout -= 1
        next_label.send_keys(Keys.ENTER)

        


# years and countries
for detail in all_details:
    all_countries.append(detail[-1])
    all_years.append(detail[1][:5])

# LAST PAGE

temp_all_details = []  
temp_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
temp_driver = driver.get('https://nextspaceflight.com/launches/?page=13&search=')

# names
names = driver.find_elements(By.CLASS_NAME,'header-style')
for name in names:
    all_names.append(name.text)

            
# details
details = driver.find_elements(By.CLASS_NAME, 'mdl-card__supporting-text')
for detail in details:
    temp_all_details.append(detail.text.split(','))

# owners
owners = driver.find_elements(By.CLASS_NAME,'mdl-card__title-text')

for owner in owners:
        all_owners.append(owner.text)
        
driver.quit()

for detail in temp_all_details:
    all_countries.append(detail[-1])
    all_years.append(detail[1][:5])



all_owners = all_owners[1::2]
print(len(all_names))
print(len(all_years))
print(len(all_countries))
print(len(all_owners))



# CREATING DATABASE
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///station-database.db'
db = SQLAlchemy(app)
app.app_context().push()



class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
        
    
if not inspect(db.engine).has_table('station'):
    db.create_all()
    
    
for n in range(len(all_names)):
    new_station = Station(
        name = all_names[n],
        owner = all_owners[n],
        country = all_countries[n],
        year = all_years[n]
    )
    db.session.add(new_station)
    db.session.commit()
