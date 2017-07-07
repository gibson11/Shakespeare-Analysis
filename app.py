import urllib.request
import xml.etree.ElementTree as ET
import os
import cgi
from collections import OrderedDict
from flask import Flask, render_template, Markup, request
import requests


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    errors = []
    speakerDict = {}
    sortedSpeakerDict = {}

    if request.method == "POST":
        r = ""
        url = ""
        # get url that the person has entered
        try:
            url = request.form['url']
            if "static" in url:
                r = url
            else:
                r = requests.get(url)
        except:
            getErrors("Unable to get URL. Please make sure it's valid and try again.", errors)
        if r:
            data = ""
            if "static" in url:
                try:
                    file = open(url)
                    data = file.read()
                    file.close()
                except:
                    getErrors("No such file or directory. Please make sure it's a valid file and try again", errors)
            else:
                file = urllib.request.urlopen(url)
                data = file.read()
                file.close()
            
            root = ""
            try:
                root = ET.fromstring(data)
                #find all speeches
                for speech in root.findall('./ACT/SCENE/SPEECH'): 
                    #find the speaker name
                    speaker = speech.find('SPEAKER').text 
                    #skip if speaker name is ALL
                    if speaker == "ALL": 
                        continue 
                    #convert speaker label to CamelCase for graph
                    speaker = speaker.title() 
                    #find all the lines by this speaker as a list
                    lineList = speech.findall('LINE') 
                    numberOfLines = len(lineList) 

                    #if the speaker is already on the dict add to their number of lines
                    if speaker in speakerDict:
                        speakerDict[speaker] += numberOfLines 
                    else:
                        speakerDict[speaker] = numberOfLines
            except:
                getErrors("The XML file has a bad format. Please make sure it's a valid file and try again", errors)

             
            if len(speakerDict) == 0:
                getErrors("URL does not have any speakers. Please make sure it's a valid URL and try again.", errors)

    


    #sort the speakers according to their number of lines in descending order
    sortedSpeakerDict = OrderedDict(sorted(speakerDict.items(), key=lambda x: -x[1]))
    labels = list(sortedSpeakerDict.keys())
    values = list(sortedSpeakerDict.values())
    for i in range(len(labels)):
        return render_template('chart.html', values=values, labels=labels)
    
    return render_template('index.html', errors=errors)


def getErrors(error, errors):
    errors.append(error)
    return render_template('index.html', errors=errors)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
