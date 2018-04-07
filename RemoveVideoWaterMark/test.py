# /usr/bin/python

import ConfigParser
import string, os, sys

cf = ConfigParser.ConfigParser()
cf.read("config.conf")

resolutionConfig = {}

resolutionConfig['360P'] = {}
resolutionConfig['360P']['x'] = cf.get("360P", "x")
resolutionConfig['360P']['y'] = cf.get("360P", "y")
resolutionConfig['360P']['w'] = cf.get("360P", "w")
resolutionConfig['360P']['h'] = cf.get("360P", "h")

resolutionConfig['480P'] = {}
resolutionConfig['480P']['x'] = cf.get("480P", "x")
resolutionConfig['480P']['y'] = cf.get("480P", "y")
resolutionConfig['480P']['w'] = cf.get("480P", "w")
resolutionConfig['480P']['h'] = cf.get("480P", "h")

resolutionConfig['504P'] = {}
resolutionConfig['504P']['x'] = cf.get("504P", "x")
resolutionConfig['504P']['y'] = cf.get("504P", "y")
resolutionConfig['504P']['w'] = cf.get("504P", "w")
resolutionConfig['504P']['h'] = cf.get("504P", "h")

resolutionConfig['720P'] = {}
resolutionConfig['720P']['x'] = cf.get("720P", "x")
resolutionConfig['720P']['y'] = cf.get("720P", "y")
resolutionConfig['720P']['w'] = cf.get("720P", "w")
resolutionConfig['720P']['h'] = cf.get("720P", "h")

resolutionConfig['1080P'] = {}
resolutionConfig['1080P']['x'] = cf.get("1080P", "x")
resolutionConfig['1080P']['y'] = cf.get("1080P", "y")
resolutionConfig['1080P']['w'] = cf.get("1080P", "w")
resolutionConfig['1080P']['h'] = cf.get("1080P", "h")

print(resolutionConfig)

# # modify one value and write to file
# cf.set("db", "db_pass", "xgmtest")
# cf.write(open("test.conf", "w"))