#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import os
import requests
import config
import json
import base64
import sys

class GoogleTTS:
    def __init__(self):
        self.url          = "https://texttospeech.googleapis.com/v1/text:synthesize"
        self.apiKey       = config.config['googleAPIkey']
        self.voice        = {'name': None, 'languageCode': None}
        self.httpSession  = requests.session()
        self.audioConfig  = {'audioEncoding':    config.config['audioEncoding'], 
                             'speakingRate':     config.config['speakingRate'],
                             'pitch':            config.config['pitch'],
                             'volumeGainDb':     config.config['volumeGainDb'],
                             'sampleRateHertz':  config.config['sampleRateHertz'],
                             'effectsProfileId': config.config['effectsProfileId']
                            }
    def setVoice(self, name, languageCode):
        self.voice['name']         = name
        self.voice['languageCode'] = languageCode

    def produce(self, text=None, ssml=None):
        if text is None and ssml is None:
                print("No text or ssml to produce")
                return

        data = {
                "input": {},
                "voice": {"name":  self.voice['name'], "languageCode": self.voice['languageCode']},
                "audioConfig": self.audioConfig
               }
         
        if text is not None:
            data['input']['text'] =  text
        if ssml is not None:
            data['input']['ssml'] =  ssml

        headers = {"content-type": "application/json", "X-Goog-Api-Key": self.apiKey }

        r = self.httpSession.post(url=self.url, json=data, headers=headers)
        content = json.loads(r.content)
        #print(content)
        return base64.b64decode(content['audioContent'])

reDownload = input("Download existing audiofiles again?")
if reDownload == 'Y' or reDownload == 'y':
    reDownload = True
else:
    reDownload = False

tts = GoogleTTS()
tts.setVoice(name='nl-NL-Wavenet-E', languageCode='nl-NL')
#audio = tts.produce(text="Hallo")

fileExt = "wav"
if config.config['audioEncoding'] == 'LINEAR16':
    fileExt = 'wav'
elif config.config['audioEncoding'] == 'MP3':
    fileExt = 'mp3'

#with open('test.'+fileExt, 'wb') as audioFile:
#    audioFile.write(audio)

processLanguages = ['nl-nl']   #columns from csv to process

with open('freeswitch_nl_translations.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    languages = list( next(csvreader).keys() )
    languages.remove('folder')
    languages.remove('filename')
    #print(languages)
    csvfile.seek(0)
    _ = next(csvreader)
    for lang in languages:
        if lang not in processLanguages:
            print("Skipping language %s"%(lang))
            continue
        tts.setVoice(name=config.languages[lang]['name'], languageCode=config.languages[lang]['languageCode'])

        for row in csvreader:
            colLang, colDialect = lang.split('-')
            targetDir = os.path.join('google', colLang, colDialect, row['folder'].strip('/') )
            #print(targetDir)

            try:
              os.stat(targetDir)
            except:
              print('Creating folder %s'%(targetDir) )
              os.makedirs(targetDir)

            #import os.path
            file_exists = os.path.isfile( os.path.join(targetDir, row['filename']+'.'+fileExt) )

            if (reDownload and file_exists) or not file_exists:
                if row[lang] is not None and row[lang] != '':
                    audio = tts.produce(text=row[lang])
                    with open(os.path.join(targetDir, row['filename']+'.'+fileExt), 'wb') as audioFile:
                        audioFile.write(audio)
            else:
                print("skipping download: %s"%( os.path.join(targetDir, row['filename']+'.'+fileExt) ) )

                for samplerate in [8000,16000,32000,48000]:
                  targetDir2 = os.path.join('output', colLang, colDialect, config.languages[lang]['name'], row['folder'].strip('/'), str(samplerate) )
                  try:
                    os.stat(targetDir2)
                  except:
                    print('Creating folder %s'%(targetDir2) )
                    os.makedirs(targetDir2)
                  #print 'Converting %s/%s to %s/%s'%(targetdir,wavfile,targetdir2,wavfile)
                  os.system( 'sox %s -r %d -c 1 -e signed-integer %s'%(os.path.join(targetDir, row['filename']+'.'+fileExt),samplerate,os.path.join(targetDir2, row['filename']+'.'+fileExt)) )

                continue


