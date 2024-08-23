###################################################################################
# File_name : IndusNLPTookit.py             #Autor_name: Nikhil Malhotra
#Authoring Start date: 6/9/2023
# Change markers
# M0001 : Putting a code for replacing . with पूर्ण विराम (|)
##################################################################################
import os
import re
import string
import numpy as np

import nltk
from nltk.corpus import indian
from nltk.tag import tnt
import string
from logging import raiseExceptions


class Toolkit:


  # Init function
  def __init__(self):
    #List of punctuations that are available in the language
    # पूर्ण विराम (|) , अल्प विराम (,) , अर्ध विराम (;) , प्रशनवाचक चिन्ह (?)
    # विस्मयादिवाचक चिन्ह (!) , योजक (‐) , उद्धरण चिन्ह (” “), विवरण चिन्ह (:-)
    self.hindi_punctuations = ['।',',',';','?','!','-','"',':-','#','.']
    self.sundry_stops = ['|','[',']','{','}','!','@','#','#','$','%','^','&','*','(',')','_','↑']
    self.numbers = ['१','२','३','४','५','६','७','८','९']
    #List of dialect data
    # hi: Hindi, do: Dogri, ki:Kinnauri,ka:Kangri,ch:Chambeali,gh:Garhwali , ku:Kumaoni
    # ja: Jaunsari,bb: Brij Bhasha, kn: Kannauji, bu:Bundeli,ba:Bagheli,aw:Awadhi,
    # bh: Bhojpuri, ma:Magahi,ml:Maithili,an:Angika,na:Nagpuri,kh:Khortha,km:Kurmali
    # mu: Mundari, pp: Panch Pargania,ch:Chattisgarhi,su:Surgujja,ni:Nimadi,mv: Malvi,
    # mr:Marwari, dh: Dhundhari,ha: Harauti,wa: Wagdi,sh:Shekhawati,da:Hyderabadi Dakhni,
    # mhi : Mumbai hindi
    self.dialects = [
                        'hi','do','ki','ka','ch','gh','ku','ja','bb','kn','bu',
                         'ba','aw','bh','ma','ml','an','na','kh','km','mu','pp',
                         'ch','su','ni','mv','mr','dh','ha','wa','sh','da','mhi']

    #Suffixes for stemming of words
    self.suffixes = [u"ाएंगी",u"ाएंगे",u"ाऊंगी",u"ाऊंगा",u"ाइयाँ",u"ाइयों",u"ाइयां",
                     u"ाएगी",u"ाएगा",u"ाओगी",u"ाओगे",u"एंगी",u"ेंगी",u"एंगे",u"ेंगे",u"ूंगी",u"ूंगा",u"ातीं",u"नाओं",u"नाएं",u"ताओं",u"ताएं",u"ियाँ",u"ियों",u"ियां",
                     u"ाकर",u"ाइए",u"ाईं",u"ाया",u"ेगी",u"ेगा",u"ोगी",u"ोगे",u"ाने",u"ाना",u"ाते",u"ाती",u"ाता",u"तीं",u"ाओं",u"ाएं",u"ुओं",u"ुएं",u"ुआं",
                     u"कर",u"ाओ",u"िए",u"ाई",u"ाए",u"ने",u"नी",u"ना",u"ते",u"ीं",u"ती",u"ता",u"ाँ",u"ां",u"ों",u"ें",
                     u"ो",u"े",u"ू",u"ु",u"ी",u"ि",u"ा"]

    #To be changed as per requirement.Directory is where we keep all dialect files
    self.dir_path = "Data/stopwords/"

  # This function igri scripts an ancillary function to convert English numbers to devna 
  def convert_to_hindi_numbers(self,english_num,dialect='hi'):
    text = ''
    if dialect == 'hi':
      for cnt in range(len(english_num)):
        text = text+english_num[cnt].replace(english_num[cnt],self.numbers[int(english_num[cnt])-1])
    return text

  #This function assumes that the sentences end with "." instead of a purna viram so it would clean those
  # This function would not affect periods within the text
  def put_purna_viram(self,input_text):
    cleaned_sentence = ''
    sentences = input_text.split('.')
    for sentence in sentences:
      if sentence.strip() != '':
        sentence += '।'
        cleaned_sentence += sentence
    return cleaned_sentence
    

  def clean_english(self,token):
    #Remove any punctuations if any
    hashed_word = ''
    for punc in self.hindi_punctuations:
        token = token.replace(punc,'').strip()
    #Remove any sundry stops if any
    for stop in self.sundry_stops:
      token = token.replace(stop,'').strip()
    match = re.search("[a-zA-Z]", token)
    if match:
      #This can be transliterated further if needed
      num_word = len(token)
      for i in range(num_word):
        hashed_word +='#'
      return hashed_word 
    else:
      return token

  # This function helps to remove english words and converts numbers to 
  # hindi format from a text
  #Use save_option = 1 if you wish to save a local file
  def clean_text(self,text , save_option=0):
    #Tokenize the words first
    tokens = self.word_tokenize(text)
    result = map(self.clean_english,tokens)
    text = ' '.join(token for token in list(result))
    english_numbers = re.findall("[1-9]", text)
    for number in english_numbers:
        text = text.replace(number,self.numbers[int(number)-1])
    if save_option == 1:
      with open('saved_cleaned_text.txt','w', encoding='utf-8') as f:
        f.write(text)
        print("File saved")
    return text  

  # This function helps find stopwords in a language and doalect
  def find_stopwords(self,dialect):
    _arrstopwords = []
    if dialect in self.dialects:
      #Figure out the stop words file
      try:
        file_name = dialect + "_stopwords.txt"
        file_path = os.path.join(self.dir_path,file_name)
        with open(file_path,'r' , encoding="UTF-8") as f:
          txt = f.readlines()
        for item in txt:
          _arrstopwords.append(item.replace("\n",""))
      except:
        raise FileNotFoundError("File not found")
    else:
      print("Sorry! The intended dialet and its stopwords is not available")
    return _arrstopwords

  # This function tokenizes given text into words
  def word_tokenize(self,input_text):
    #Remove punctuations if they occur in the text
    for punc in self.hindi_punctuations:
      if punc != "-":
        input_text = input_text.replace(punc,"")
    #White space tokenization
    _word_list = input_text.split(u" ")
    return _word_list

  #This function tokenizes given text into sentences
  def sent_tokenize(self,input_text):
    #Purna Viram tokenization
    #### M0001 starts ###################
    #Use this if necessary..........
      #_sent_list_temp = input_text.replace('.','।')
      #_sent_list = _sent_list_temp.split('।')
    #Use this if necessary.........
    _sent_list = input_text.split(u"।")
    #### M0001 ends
    for sentence in _sent_list:
      if '\n' in sentence:
        _temp = sentence
        #print(_temp)
        _sent_list.remove(sentence)
        _sec_sent_list = sentence.split('\n')
        _sent_list.append(_sec_sent_list)
    return _sent_list

  #This function generates stemmed text from a given devnagri text
  def generate_stemmed_text(self,input_text):
    lemma_text =''
    #Tokenize the text first
    tokens = self.word_tokenize(input_text)
    #print(tokens)
    for token in tokens:
      stem_word = ''
      for suffix in self.suffixes:
        if token.endswith(suffix):
          stem_word = token.replace(suffix,'')
          lemma_text += stem_word + ' '
          break
      if stem_word == '':
        lemma_text += token + ' '
    return lemma_text

  #This funtion provides word freuency
  def word_freq(self,input_text):
    _tokenized_word_list = self.word_tokenize(input_text)
    _frequency_tuple = []
    for word in _tokenized_word_list:
      matches = [match for match in _tokenized_word_list if word in match]
      _frequency_tuple.append((word,len(matches)))
    return _frequency_tuple

  #This function maps words to id and id to tokens
  def mapping(self, tokens):
    word_to_id = {}
    id_to_word = {}

    for i, token in enumerate(set(tokens)):
        word_to_id[token] = i
        id_to_word[i] = token
    return word_to_id, id_to_word


  #Function to train for POS
  def tagger_train(self):
    taggedSet = "hindi.pos"
    wordSet = indian.sents(taggedSet)
    count = 0
    print(wordSet[0])
    for sen in wordSet:
        count = count + 1
        sen = "".join(
            [
                " " + i if not i.startswith("'") and i not in string.punctuation else i
                for i in sen
            ]
        ).strip()
        #print(count, sen, "sentences")
    #print("Total sentences in the tagged file are", count)

    trainPerc = 0.9

    trainRows = int(trainPerc * count)
    testRows = trainRows + 1

    data = indian.tagged_sents(taggedSet)
    train_data = data[:trainRows]
    test_data = data[testRows:]

    print("Training dataset length: ", len(train_data))
    print("Testing dataset length: ", len(test_data))

    pos_tagger = tnt.TnT()
    pos_tagger.train(train_data)
    print("Accuracy: ", pos_tagger.evaluate(test_data))
    return pos_tagger

  #This function helps find POS tags
  def pos_tags(self,input_text):
    tokens = self.word_tokenize(input_text)
    pos_tagger = self.tagger_train()
    _tags = pos_tagger.tag(tokens)
    return _tags

#Usage
if __name__== "__main__":
    text = "संसद के विशेष सत्र (Parliament Special Session) के बीच कल यानी, सोमवार, 18 सितंबर को प्रधानमंत्री नरेंद्र मोदी (PM Narendra Modi) की अध्यक्षता में हुई केंद्रीय कैबिनेट बैठक हुई जिसमें  महिला आरक्षण बिल (Women's Reservation Bill) मंजूरी दे दी गई है. सूत्रों के हिसाब से यह खबर सामने आ रही है. मोदी कैबिनेट की बैठक में लोकसभा और विधानसभाओं जैसी निर्वाचित संस्थाओं में 33 फीसदी महिला आरक्षण (Women Quota Bill 2023) पर मुहर लग गई है. मीडिया रिपोर्ट्स के अनुसार, महिला आरक्षण बिल को आज यानी  मंगलवार को लोकसभा में नए संसद भवन (New Parliament Building) में पेश किया जाएगा."
    tk = Toolkit()

    #If you wish to opne a file of data use the following
    #with open('Data\corpora\hin_mixed_2019_10K-sentences.txt' ,'r', encoding='utf-8') as f:
      #text = f.read()
    #print(tk.convert_to_hindi_numbers("12356464"))
    #print(tk.put_purna_viram(text))
    #print(tk.clean_text(text))
    #print(tk.word_tokenize(text))
    #print(tk.sent_tokenize(text))
    #print(tk.pos_tags(text))
    #print(tk.find_stopwords('hi'))
    print(tk.generate_stemmed_text(text))
    #print("--------------------")
