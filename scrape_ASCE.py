import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import matplotlib.pylab as plt


# Scrape journal of computing in civil engineering website
volumes = range(23,33)
issues = range(1,7)
dic = {}

for vol in volumes:
    titleList = []
    for issue in issues: 
        url = "https://ascelibrary.org/toc/jccee5/"+str(vol)+"/"+str(issue)
        #get url
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        #find all paper titles in current issue
        issueTitles = soup.find_all(attrs={'class': 'hlFld-Title'})
        for title in issueTitles:
            titleList.append(re.search('<span class="hlFld-Title">(.+?)</span>', str(title)).group(1).lower())     
    dic[vol] = titleList

#define ML and DL keywords
mlKwds = ['machine learning', 'svm', 'support vector', 'gradient boosting', 'random forest', 'deep learning', 
          'big data', 'neural network', 'deep neural', 'artificial intelligence', 'convolutional', 'reinforcement learning']
dlKwds = ['deep learning', 'deep neural', 'convolutional', 'reinforcement learning']

#count volume of ML keyword appearces in each year
countDicML = {}
for key in dic.keys():
    count = 0
    for title in dic[key]:
        for word in mlKwds:
            if word in title:
                count +=1
    countDicML[key] = count

#count volume of DL keyword appearces in each year
countDicDL = {}
for key in dic.keys():
    count = 0
    for title in dic[key]:
        for word in dlKwds:
            if word in title:
                count +=1
    countDicDL[key] = count

#plot results
t = range(2009,2019)
alpha = 0.8
plt.figure(figsize=(16,9))
plt.plot(t, [countDicML[k] for k in sorted(countDicML.keys())], 
         lw=2.5, color='#333A56', label="machine learning")
plt.plot(t, [countDicDL[k] for k in sorted(countDicDL.keys())],
         ls='--', lw=2.5, color='#53658F', label="deep learning")
plt.title('Penetration of AI in Civil Engineering research', loc='left', alpha=alpha)
plt.ylabel('Number of papers', alpha=alpha)
plt.yticks(alpha=alpha)
plt.xlabel('Year', alpha=alpha)
plt.xticks(alpha=alpha)
plt.legend(loc='upper center', ncol=2)
plt.show()