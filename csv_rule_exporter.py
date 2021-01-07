# The utility scrip takes content export in XML and JSON format as input
# The output produces csv export of the content stored under content directory, rules_export.csv 

import os
import csv
import fnmatch
import json
import xml.etree.ElementTree as ET

namespaces = {'end': 'http://sampleschema.com/schema/content/2008'}

basePath = 'content\Test Rules'                                                                     # input directory of the xml, json content
pattern = 'content.xml'                                                                             # JSON content file filter
boost_rules_data = open(basePath+'/rules_export.csv', 'w', newline='',  encoding="utf-8")           # open a file for writing
csvwriter = csv.writer(boost_rules_data)                                                            # create the csv writer object
csvwriter.writerow(["name", "keywords", "skus"])                                                    # CSV Header

def keywordsReader(jsonfile):
    keywords = []

    kw_file = open(jsonfile, encoding="utf-8")

    data = json.load(kw_file)
    triggers = data['triggers']

    for keywordDict in triggers:
        keywords.append(keywordDict['keyword'])

    kw_file.close
    return keywords


for dirpath, dirs, files in os.walk(basePath):
    for filename in fnmatch.filter(files, pattern):
        currentFile=os.path.join(dirpath, filename)

        tree = ET.parse(currentFile)
        root = tree.getroot()

        skuItem = []
        recordItem = []
    
        name = root.find('end:Name', namespaces).text

        for stringVal in root.iterfind('end:Property/end:String', namespaces):
            if stringVal.text is not None:
                skuItem.append(stringVal.text)

        
        kw_file = os.path.join(dirpath, "_.json")
        
        recordItem.append(name)
        recordItem.append(keywordsReader(kw_file))
        recordItem.append(skuItem)

        csvwriter.writerow(recordItem)

boost_rules_data.close()