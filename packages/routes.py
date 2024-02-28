from flask import Flask, render_template, request
from packages import app
import pandas as pd
import requests
import re
import numpy as np

@app.route("/")
def index():

  return render_template('layout.html')

@app.route("/get_doc", methods=["POST", "GET"])
def html_table():

  name1 =request.form["doc_input"]
  name = name1.split(",") 
  d = []

  if len(name) <= 3:
    for i in name:  
      d.append(google_doc(i))
  else:
    #d.append(pd.DataFrame(['Please enter max of 3 doctors']))
    return render_template('search_overage.html')
  
  doc_df = pd.concat(d, axis=1)
  #doc_df = doc_df.fillna(0)
  #doc_df = doc_df.astype('float').applymap('{:,.2f}'.format)
  doc_df = doc_df.astype('float')
  #doc_df = np.round(doc_df, decimals=2)
  df_mean = doc_df.mean().astype('float').round(2)
  doc_df.loc['Average Rating'] = df_mean
  #doc_df.iloc[0] = doc_df.iloc[0].astype('float').round(2)
  #doc_df.loc['mean'] = doc_df.mean()

  return render_template('query.html', docF=[doc_df.to_html(classes='data')], titles=doc_df.columns.values)


def google_doc(doctors):
    """Add google to the doctors name for search"""
    strip_name = str(doctors).replace(" ","+")
    doc = 'https://www.google.com/search?q='+strip_name
    header = {'User-agent':'Mozilla/5.0'}
    request = str(requests.get(doc,headers = header).content)

    with open('RockDoc.txt', 'w') as outfile:
      outfile.write(request)
  
    f_link = []
    rate = []

    all_links_pat  = r'(?=<a\ href\=\"\/url\?q=https).*?(?=\"Gx5Zad)'
    #get_rate_pat = re.compile("(?<=Rated )(?:[0-9]\.[0-9])")  #oqSTJd us this instead of Rated
    get_rate_pat = re.compile("(?<=oqSTJd\"\>)(?:[0-9]\.[0-9])")  #oqSTJd us this instead of Rated
    site_pat = r'(?=https://).*?(.com=?|.org=?)'
    
    all_links = re.findall(all_links_pat, request)

    for i in all_links:
      if "Rated" in i:
        try:
          f_link.append(re.search(site_pat, i).group().replace('https://','').replace('www.',''))
          #f_link.append(re.search(site_pat, i).group())
          rate.append(re.search(get_rate_pat, i).group())
        except:
          pass
      else:
        continue

    if len(f_link) >= 1: 
      p = pd.DataFrame(rate)
      p.columns = [str(doctors)]
      p.index = f_link
      p.sort_values(str(doctors), ascending=False, inplace=True)
    else:
      #p = pd.DataFrame(['No Available Data'])
      p = pd.DataFrame([0])
                          
    return p 

