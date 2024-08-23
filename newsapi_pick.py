import os
import requests
from bs4 import BeautifulSoup
from IndusNLPToolkit import Toolkit
import re

tk = Toolkit()

# This function helps to remove english words and converts numbers to 
# hindi format from a text
#Use save_option = 1 if you wish to save a local file
hindi_punctuations = ['।',',',';','?','!','-','"',':-','#','.']
sundry_stops = ['|','[',']','{','}','!','@','#','#','$','%','^','&','*','(',')','_','↑']
header_list = ['Home','National','International','State','Business','Sports','Miscellaneous','Archives',' Audios: News & Current Affairs',' Special Campaigns',
               ' Transcripts',' News in Regional Languages (Audios & Text)',' Text Archive Search','Talks','Podcasts',
                'News Schedule','Contact Us','Screen Reader Access','Akashvani ,  news, All India Radio News',
                'English','Hindi','Gujarati','Marathi','Urdu','Tamil','Dogri','Assamese','Rajasthani','youtube','news on air youtube live',
                'download mobile App','Facebook live','Twitter live','Tweets by airnewsalerts','listen News','Whatsapp',
                'Connect with us','Press Release','DD News','AIR','Contractual Engagements','Prasar Bharati Policy for','Prasar Bharati',
                'PTC Guidelines','Non RNU','RNU',
                'Site Maintained by: Website Cell, NSD and IT Division, Prasar Bharati (Broadcasting Corporation of India) NSD AIR, New Delhi, India.  Website Policy',
                'Site Maintained by: Website Cell, NSD and IT Division,  (Broadcasting Corporation of India) NSD , New Delhi, India.  Website Policy',
                'MORNING NEWS','MIDDAY NEWS','EVENING NEWS']

def word_tokenize(input_text):
    _word_list = input_text.split(u" ")
    return _word_list


def hindi_news_drop(text,seed):
    if u'मुख्य समाचार' in text:  
        print("Found in....." , str(seed))
        #Cleaning the text 
        for head in header_list:
            text = text.replace(head,'')
        text = text.replace('\n','')
        text = text.replace('\r','')
        #Final cleaning of English 
        text = tk.clean_text(text)
        with open("Data\\news\\news_hindi_AIR_"+str(seed)+".txt","w",encoding="UTF-8") as f:
            f.write(text)
            print("----------------------------")
            print('news_hindi_AIR_'+str(seed)+'.txt file written')

# This function takes the request url and seed to loop through 
def loop_through_news(req,seed,seed_end):
    while seed <= seed_end:
        text = ''
        url = req+str(seed)
        res = requests.get(url)
        if res.status_code == 200:
            #Site found ...start the loop of seed
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            for element in soup.select('div'):
                text += element.text   

            hindi_news_drop(text,seed)    
            seed +=1




#Usage
if __name__== "__main__":
    REQ_URL = "https://newsonair.gov.in/Text-Bulletin-Details.aspx?id="

    loop_through_news(REQ_URL ,2000,3000)