import json
import os

import object.jsondict
from misc import Utils

server = 'raw/server'

index = json.load(open(server + '/' + 'index.json'), object_hook=object.jsondict.JSONObject)

filesDir = server + index.root
folders = [folder for folder in os.listdir(filesDir) if os.path.isdir(os.path.join(filesDir, folder))]

featureList = []

for folder in folders:
    feature = {"name": folder}
    versions = [f1 for f1 in os.listdir(filesDir + "/" + folder) if os.path.isdir(os.path.join(filesDir, folder))]
    versionNumbers = []
    for version in versions:
        versionNumbers.append(int(version.strip(index.version_prefix)))

    featureDir = filesDir + "/" + folder + "/" + index.version_prefix + str(max(versionNumbers))
    feature_json_texts = [file for file in os.listdir(featureDir) if os.path.isfile(os.path.join(featureDir, file))]

    list_of_features = []
    for feature_json in feature_json_texts:
        hash_of_single_feature_text = Utils.hash_file(featureDir + '/' + feature_json)
        list_of_features.append(
            {'name': feature_json, 'url': featureDir + "/" + feature_json, 'hash': hash_of_single_feature_text,
             'version': max(versionNumbers)})
        feature['list'] = list_of_features

    featureList.append(feature)

print(featureList)

index_recalculated = {'root': index.root, 'version_prefix': index.version_prefix}
index_recalculated['list'] = featureList
json_data = json.dumps(index_recalculated, indent=4)
fileWrite = open('raw/server/index.json', 'w')
fileWrite.write(json_data)
fileWrite.close()

# samplejson.close()
#
# jsonWrite = {}
# jsonIn = {'key2': 'value2'}
# jsonWrite['key'] = jsonIn
# json_data = json.dumps(jsonWrite)
#
# fileWrite = open('raw/newFile01.json', 'w')
# fileWrite.write(json_data)
# fileWrite.close()
#
# print(json.load(open('raw/newFile01.json')))
