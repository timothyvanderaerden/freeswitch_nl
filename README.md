# freeswitch_nl
International Audioprompts for FreeSwitch

Although this started as a project to create only Dutch audioprompts for Freeswitch, this project is now open for other translations.  
The csv file contains all prossible translations and the python script generates audiofiles from the text by using Google TTS.

Manual:
- Run python script freeswitch_nl_translation.py
- Add to /etc/freeswitch/freeswitch.xml:     &lt;X-PRE-PROCESS cmd="include" data="languages/nl/*.xml"/&gt;
- copy output/nl to /usr/share/freeswitch/sounds
- copy xml/nl to /etc/freeswitch/languages

Dependencies:
- sox
- python-csv
- python-os
- python-requests

Contributors:
- Hsing-Foo Wang <hsingfoo@gmail.com>
- Jeroen Hermans <github@epsys.nl>
- Kevin Moesker
