import os, argparse
import ruamel.yaml
from pprint import pprint 

def PreParse():
    testFile = open('test3.yml', 'r')
    lines = testFile.readlines()
    escapedLines = []
    for line in lines:
         escapedLines.append(line.replace("'","\'\'\'"))
    with open("testEscaped.yml","w+") as out:
        for escapedLine in escapedLines:
             out.write(escapedLine)

def PostParse():
    outFile = open("output.yml","r")
    lines = outFile.readlines()
    outFile.close()
    fixedLines = []
    for line in lines:
        fixedLines.append(line.replace("\'\'\'","\'"))
    outFile = open("output.yml","w+")
    for fixedLine  in fixedLines:
        outFile.write(fixedLine.replace('"',''))
    outFile.close()

runYaml = ruamel.yaml.YAML()
parser = argparse.ArgumentParser()
parser.add_argument("-api")
parser.add_argument("-id")
parser.add_argument("-v1")
parser.add_argument("-v2")
parser.add_argument("-action", required=True)
args = parser.parse_args()
PreParse()
testFile = open('testEscaped.yml', 'r')
parsed = runYaml.load(testFile)
testFile.close()

if args.action == "with_client":
    if parsed['eurekazuul']['serviceClientVersionMap'][args.api]['clientVersionRules'].get(args.id):
        print("data is already present")
        quit()
elif args.action == "without_client":
    if parsed['eurekazuul']['serviceClientVersionMap'][args.api].get(args.id) and parsed['eurekazuul']['serviceClientVersionMap'][args.api].get('clientVersionRules'):
        print("data is already present")
        quit()

keyToInsert = args.id
valueToInsert = {'defaultMajorMinorVersion': '\'%s\''%args.v1, 'versionRules':{1:{'defaultMinorVersion':'\'%s\''%args.v2}}}

if args.action == "update_version":
    parsed['eurekazuul']['serviceClientVersionMap'][args.api]['clientVersionRules'][keyToInsert]['defaultMajorMinorVersion'] = '\'%s\''%args.v1
    parsed['eurekazuul']['serviceClientVersionMap'][args.api]['clientVersionRules'][keyToInsert]['versionRules'][1]['defaultMinorVersion'] = '\'%s\''%args.v2

elif args.action == "with_client":
    parsed['eurekazuul']['serviceClientVersionMap'][args.api]['clientVersionRules'][keyToInsert] = valueToInsert

elif args.action == "without_client":
    parsed['eurekazuul']['serviceClientVersionMap'][args.api]['clientVersionRules'] = {}
    parsed['eurekazuul']['serviceClientVersionMap'][args.api]['clientVersionRules'][keyToInsert] = valueToInsert

outFile = open("output.yml","w+")
runYaml.dump(parsed, outFile)
outFile.close()
PostParse()
if args.action == "update_version":
    print("Version has been updated")
else:
    print("Data has been added")
os.remove("testEscaped.yml")
os.rename("output.yml","test3.yml")
