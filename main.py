import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from google.colab import drive
drive.mount('/content/drive/')


def select_fnct_value(soup,css_condition,value=""):
  result=[]
  data=soup.select(css_condition)
  if value!="":
    for line in data :
      result.append(line[value])
    return result
  else:
    for line in data :
      result.append(line.text)
    return result

def Modify_links(tab_links,prefix):
   for i in range(0,len(tab_links)):
     tab_links[i]=prefix+tab_links[i]
   return tab_links



content=requests.get("https://pll.harvard.edu/catalog?page=15").text
data=BeautifulSoup(content,"html.parser")


fields = select_fnct_value(data,".field-name-subject-area > a")
related_courses_Link = select_fnct_value(data,".field-name-subject-area > a","href")
course_type=select_fnct_value(data,".field-name-modality > span")
names=select_fnct_value(data,".field-name-title-qs > h3 > a")
course_details_link=select_fnct_value(data,".field-name-title-qs > h3 > a","href")
infos=select_fnct_value(data,".group-bottom-fields.field-group-div")
images=select_fnct_value(data,".b-lazy","data-src") 
description=select_fnct_value(data,".field-name-field-course-summary")
related_courses_Link=Modify_links(related_courses_Link,"https://pll.harvard.edu")
course_details_link=Modify_links(course_details_link,"https://pll.harvard.edu")
 
price=[]
availability=[]

for elt in infos:
    if "Free" in elt:
      price.append("Free")
    else:
      price.append("paid $")
    if "Available now" in elt:
      availability.append("Available now")
    else:
        availability.append("Not Available")

data={
    "img":images,
    "name":names,
    "field":fields,
    "related_courses_Link":related_courses_Link,
    "course_type":course_type,
    "course_details_link":course_details_link,
    "price":price,
    "availability":availability,
    "description":description
     } 
     
print(data)
df=pd.DataFrame(data)
print(df.shape)
PATH = "/content/drive/MyDrive/web_scrapping_courses/"
df.to_csv(f"{PATH}course15.csv")