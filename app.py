#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Mar 19 12:05 2022

@author: Simas Janusas
"""
from distutils.log import debug
from nltk import PorterStemmer
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from flask import Flask, request, make_response, send_file, render_template, redirect, url_for
from io import BytesIO
import time
import zipfile


app = Flask(__name__)

def cleanse_text(text):
    if text:
        #whitespaces
        clean = ' '.join(text.split())
        
        # Stemming
        red_text = [PorterStemmer().stem(word) for word in clean.split()]
        print(red_text)
        # Done. return
        return ' '.join(red_text)

    else:
        return text

@app.route('/')
def home_page():
    return '''<h2>Hello stranger!</h2>\nThis is a text clustering application. 
    To cluster your text go to page `/cluster` and provide your input text to predict and get the clustered text zip results in excel spreadsheet.
    \n
    Example: /cluster?col=text \n
    /cluster: endpoint \n
    col=text: column name that contains text data. \n
    '''

@app.route('/cluster')
def cluster():
    return render_template('cluster_file.html')

@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    
    print('ARGS:\n{args}\nFILES:\n{files}'.format(
        args=request.args, files=request.files))

    data = pd.read_csv(request.files['file'])
    
    # process data

    unstructure = 'text'
    if 'col' in request.args:
        unstructure = request.args.get('col')
    no_of_clusters = 2
    if 'no_of_clusters' in request.args:
        no_of_clusters = int(request.args.get('no_of_clusters'))
        
    # continue to process
    data = data.fillna('NULL')

    # clean the data
    data['clean_sum'] = data[unstructure].apply(cleanse_text)
    
    # prep for modelling
    vectorizer = CountVectorizer(analyzer='word',
                                 stop_words='english')
    counts = vectorizer.fit_transform(data['clean_sum'])
    # make model
    kmeans = KMeans(n_clusters=no_of_clusters)
    # fit model
    data['cluster_num'] = kmeans.fit_predict(counts)
    data = data.drop(['clean_sum'], axis=1)
    
    # prepare result output
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Clusters', 
                  encoding='utf-8', index=False)
    
    # build result output
    clusters = []
    for i in range(np.shape(kmeans.cluster_centers_)[0]):
        data_cluster = pd.concat([
            pd.Series(vectorizer.get_feature_names()),
            pd.DataFrame(kmeans.cluster_centers_[i])
            ],
            axis=1)
        data_cluster.columns = ['keywords', 'weights']
        data_cluster = data_cluster.sort_values(by=['weights'], ascending=False)
        data_clust = data_cluster.head(n=10)['keywords'].tolist()
        clusters.append(data_clust)
    pd.DataFrame(clusters).to_excel(writer, sheet_name='Top_Keywords', encoding='utf-8')
    
    #Pivot
    data_pivot = data.groupby(['cluster_num'], as_index=False).size()
    data_pivot.name = 'size'
    data_pivot = data_pivot.reset_index()
    data_pivot.to_excel(writer, sheet_name='Cluster_Report', 
                  encoding='utf-8', index=False)
    
    # insert chart
    workbook = writer.book
    worksheet = writer.sheets['Cluster_Report']
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
            'values': '=Cluster_Report!$B$2:$B'+str(no_of_clusters+1)
            })
    worksheet.insert_chart('D2', chart)
    
    # save output
    writer.save()
    
    # prepare final output
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        names = ['cluster_output.xlsx']
        files = [output]
        for i in range(len(files)):
            data = zipfile.ZipInfo(names[i])
            data.date_time = time.localtime(time.time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, files[i].getvalue())
    memory_file.seek(0)
    
    # make a response file to be sent back
    response = make_response(send_file(
        memory_file, 
        download_name='cluster_output.zip',
        as_attachment=True
    ))
    
    # (CORS) allow requests from any IP
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response    
    
if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)
