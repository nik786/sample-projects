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
args = parser.parse_args()


PreParse()

testFile = open('testEscaped.yml', 'r')
parsed = runYaml.load(testFile)
testFile.close()
if parsed['eurekazuul']['serviceClientVersionMap'][args.api]['clientVersionRules'].get(args.id):
    print("data is already present")
    quit()

keyToInsert = args.id
valueToInsert = {'defaultMajorMinorVersion': '\'%s\''%args.v1, 'versionRules':{1:{'defaultMinorVersion':'\'%s\''%args.v2}}}
parsed['eurekazuul']['serviceClientVersionMap'][args.api]['clientVersionRules'][keyToInsert] = valueToInsert

outFile = open("output.yml","w+")
runYaml.dump(parsed, outFile)
outFile.close()
PostParse()
print("Data has been added")
os.remove("testEscaped.yml")
os.rename("output.yml","test3.yml")
