#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import cookielib
import urllib

cj = cookielib.LWPCookieJar()

def http_request(url=None, data=None, headers=None):
  if url==None:
    return None

  import urllib
  import urllib2
  global cj

  if True:
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

  if 'Content-Type' in headers:
    class ChangeTypeProcessor(urllib2.BaseHandler):
      def http_request(self, req):
        req.unredirected_hdrs["Content-type"] = headers['Content-Type']
        return req
      def https_request(self, req):
        req.unredirected_hdrs["Content-type"] = headers['Content-Type']
        return req

  opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), urllib2.HTTPCookieProcessor(cj))
  if 'Content-Type' in headers:
    opener.add_handler(ChangeTypeProcessor())
  req = urllib2.Request(url, data=data,
        headers=headers)

  try:
    response = opener.open(req)
    return response
  except IOError, e:
    print 'Failed to open "%s".' % url
    if hasattr(e, 'code'):
      import json
      print 'We failed with error code - %s.' % e.code
      print json.load(e)
    elif hasattr(e, 'reason'):
      print "The error object has the following 'reason' attribute :"
      print e.reason

  return None


def get_content(response=None):
  if response == None:
    return None

  if response.info().get('Content-Encoding') == 'gzip':
    import gzip
    from StringIO import StringIO
    compressedstream = StringIO(response.read())
    return gzip.GzipFile(fileobj=compressedstream).read()
  else:
    return response.read()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.naturalreaders.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'}



#There are two Dutch voices
voices=[{'id':21,'name': 'anika'},{'id':22,'name': 'markus'}]

#Talking speed for Natural Readers
speed=0
#folder names for freeswitch (language, dialect)
language=['nl','nl']
#Free API key. May change in the future. Please check website Natural Readers
apikey='b98x9xlfs54ws4k0wc0o8g4gwc0w8ss'

import requests
headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0', 'Origin': 'https://www.naturalreaders.com', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*' }

data = raw_input("Download existing audiofiles again?")

get_params={'l': '0', 'v': 'mac', 'r':voices[0]['id'], 's':speed, 't':''}
with open('freeswitch_nl_translations.csv', 'rb') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
  for row in csvreader:
    if row[2] != '':
      for voice in voices:
        #print row[2]
        get_params['t'] = row[2]
        url = 'https://kfiuqykx63.execute-api.us-east-1.amazonaws.com/Dev/tts?%s'%(urllib.urlencode(get_params))

        targetdir  = 'naturalreaders/%s/%s'%(voice['name'], row[0][1:] if row[0][0]=='/' else row[0])

        if row[1][-4:] == '.wav':
          targetfile = '%s.mp3'%(row[1][0:-4])
        else:
          targetfile = '%s.mp3'%(row[1])

        try:
          os.stat(targetdir)
        except:
          #print 'Creating folder %s'%(targetdir)
          os.makedirs(targetdir)

        print 'Processing %s/%s'%(targetdir,targetfile)

        import os.path
        file_exists = os.path.isfile("%s/%s"%(targetdir,targetfile) )

        if (file_exists and data == 'y') or not file_exists:
          #print 'Downloading %s'%(url)
          postdata = '{"t": "%s" }'%(row[2])

          import time
          response = None
          while response is None:
            response = http_request(url=url, data=postdata, headers=headers)
            if response is None: time.sleep(10)
          content = get_content(response)
          output_file = open("%s/%s"%(targetdir,targetfile),"wb")
          output_file.write(content)
          output_file.close()

        wavfile = "%s.wav"%(targetfile[:-4])
        #print 'Converting %s/%s to %s/%s'%(targetdir,targetfile,targetdir,wavfile)
        os.system( 'ffmpeg -v 0 -y -i %s/%s %s/%s'%(targetdir,targetfile,targetdir,wavfile) )

        for samplerate in [8000,16000,32000,48000]:
          targetdir2  = 'output/%s/%s/%s/%s/%d'%(language[0],language[1],voice['name'], row[0][1:] if row[0][0]=='/' else row[0], samplerate)
          try:
            os.stat(targetdir2)
          except:
            print 'Creating folder %s'%(targetdir2)
            os.makedirs(targetdir2)
          #print 'Converting %s/%s to %s/%s'%(targetdir,wavfile,targetdir2,wavfile)
          os.system( 'sox %s/%s -r %s -c 1 -e signed-integer %s/%s'%(targetdir,wavfile,samplerate,targetdir2,wavfile) )

      print
