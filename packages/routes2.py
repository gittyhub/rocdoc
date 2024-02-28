from flask import Flask, render_template, request
from packages import app
import pandas as pd
import requests
import re


df = pd.DataFrame({'A':[1,2,3],
    'B':[5,6,7],
    'C':[8,9,0]})

@app.route("/")
def index():

#  doctors = request.args.get("doctors", "")
#  if doctors:
#    doc_data = google_doc(doctors)
#  else:
#    doc_data = ""
#  return (
#    """<form action="" method="get">
#        Enter Doctors Name: <input type="text" name="doctors">
#        <input type="submit" value="Get google doctor link">
#    </form>"""
#       + "Doctor Link: "
#       + str(doc_data)
#        )
  return render_template('layout.html', name="James")

@app.route("/get_doc", methods=["POST", "GET"])
def html_table():
    #return render_template('simple.html', tables=[df.to_html(classes='data')], titles = "Doctors")

  name =request.form["doc_input"]
  #doctors = request.args.get("doctors", "")
  if name:
    doc_df = google_doc(name)
  else:
    doc_df = pd.DataFrame()

  return render_template('layout.html', docF=[doc_df.to_html(classes='data')], titles=doc_df.columns.values)


def google_doc(doctors):
    """Add google to the doctors name for search"""
    strip_name = doctors.replace(" ","+")
    doc = 'https://www.google.com/search?q='+strip_name
    header = {'User-agent':'Mozilla/5.0'}
    request = str(requests.get(doc,headers = header).content)

    with open('RockDoc_Find_Column.txt', 'w') as outfile:
      outfile.write(request)
  
    rate_pattern = re.compile("(?<=Rated )(?:[0-9]\.[0-9])")
    r = re.findall(rate_pattern,request)
    col = len(r)
                          
    p = pd.DataFrame(r).T
    p.index = [doctors]
                   
    return p 

