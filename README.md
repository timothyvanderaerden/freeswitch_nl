# freeswitch_nl
Dutch Audioprompts for FreeSwitch

Manual:
- Run python script freeswitch_nl_translation.py (this takes a LONG time)
- Add to /etc/freeswitch/freeswitch.xml:     <X-PRE-PROCESS cmd="include" data="lang/nl/*.xml"/>
- copy output/nl to /usr/share/freeswitch/sounds
- copy xml/nl to /etc/freeswitch/lang

Dependancies:
- ffmpeg
- sox
- python-csv
- python-os
- python-urllib
