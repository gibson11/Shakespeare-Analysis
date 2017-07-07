import urllib2
import xml.etree.ElementTree as ET
import os
from collections import OrderedDict
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def readPlay():
	file = urllib2.urlopen(' http://www.ibiblio.org/xml/examples/shakespeare/macbeth.xml')
	data = file.read()
	file.close()

	speakerDict = {}
	sortedSpeakerDict = {}
	listS = []
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

    #sort the speakers according to their number of lines in descending order
    sortedSpeakerDict = OrderedDict(sorted(speakerDict.items(), key=lambda x: -x[1]))
    
    
    labels = list(sortedSpeakerDict.keys())
    values = list(sortedSpeakerDict.values())
    for i in range(len(labels)):
    	print labels[i], values[i]
    	return render_template('chart.html', values=values, labels=labels)

    	if __name__ == "__main__":
    		port = int(os.environ.get("PORT", 5000))
    		app.run(host='0.0.0.0', port=port)
