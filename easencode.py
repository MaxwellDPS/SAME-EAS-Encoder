#!/usr/bin/python3

import argparse, sys, os, re, time, wave
import audioroutines



def generateEASpcmData(org, event, fips, eventDuration, timestamp, stationId, sampRate, sampWidth, peakLevel, numCh, msgaudio=None, customMsg=None, eom=True):
	markF, spaceF, bitrate  = 2083.3, 1562.5, 520.3
	pcm_data = []

	preamble = '\xab' * 16
	if not eom:
		message = 'ZCZC-{0}-{1}-{2}+{3}-{4}-{5: <8}-'.format(org, event, "-".join(fips[0:31]), eventDuration, timestamp, stationId[0:8])
		header = audioroutines.generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel, numCh, preamble + message.upper())
		silence = audioroutines.generateSimplePCMToneData(10000, 10000, sampRate, 1, sampWidth, -94, numCh)	
		begintones = audioroutines.generateDualTonePCMData(markF, markF, sampRate, 0.015, sampWidth, peakLevel, numCh)
		
		pcm_data = silence+ begintones + header + begintones + silence
		for i in range(2):
			pcm_data = pcm_data + begintones + header + begintones + silence
		
		attn_tones = audioroutines.generateDualTonePCMData(960, 853, sampRate, 8, sampWidth, peakLevel, numCh)
		pcm_data = pcm_data + silence + attn_tones + silence

		return pcm_data
	else:
		message = 'ZCZC-{0}-{1}-{2}+{3}-{4}-{5: <8}-'.format(org, event, "-".join(fips[0:31]), eventDuration, timestamp, stationId[0:8])
		header = audioroutines.generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel, numCh, preamble + message.upper())
		silence = audioroutines.generateSimplePCMToneData(10000, 10000, sampRate, 1, sampWidth, -94, numCh)	
		begintones = audioroutines.generateDualTonePCMData(markF, markF, sampRate, 0.015, sampWidth, peakLevel, numCh)
		
		pcm_data = silence+ begintones + header + begintones + silence
		for i in range(2):
			pcm_data = pcm_data + begintones + header + begintones + silence
		
		attn_tones = audioroutines.generateDualTonePCMData(960, 853, sampRate, 8, sampWidth, peakLevel, numCh)
		pcm_data = pcm_data + silence + attn_tones + silence

		EOM = 'NNNN'
		headerEOM = audioroutines.generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel, numCh, preamble + EOM.upper())

		pcm_data = pcm_data + silence + silence + begintones + headerEOM + begintones + silence
		for i in range(2):
			pcm_data = pcm_data + begintones + headerEOM + begintones + silence

		return pcm_data

def main():
	numCh = 1
	peakLevel = -0.001
	sampWidth = 16
	sampRate = 48000
	msgaudio = None

	for option, value in args.__dict__.items():
		if value is not None:
			if option == 'fips': value = " ".join(value)
			if not re.match(arg_patterns[option], str(value), re.I):
				parser.error("Invalid {0} '{1}'".format(option, str(value)))
		if len(args.fips) > 31: print("WARNING: only 31 FIPS codes allowed. Truncating...")
		if len(args.callsign) > 8: print("WARNING: callsign max width is 8 characters. Truncating...")

	if args.audioin is not None:
		infile = wave.open(args.audioin, 'rb')
		numCh, sampWidth, sampRate, audio_dur, compression, comment = infile.getparams()
		sampWidth = sampWidth * 8
		msgaudio = infile.readframes(infile.getnframes())
		infile.close()
	else:
		infile = None
	ts_val = time.strftime('%j%H%M', time.strptime(args.timestamp, r'%m/%d/%Y %H:%M')) if re.match(r'\d{2}/\d{2}/(\d{4})\s+\d{2}:\d{2}', args.timestamp, re.I) else time.strftime('%j%H%M', time.gmtime())

	data = generateEASpcmData(args.originator, args.event, args.fips, args.duration, ts_val, args.callsign, sampRate, sampWidth, peakLevel, numCh, msgaudio, args.custom_msg, args.eom)
	data = audioroutines.filterPCMaudio(3000, sampRate, 20, sampWidth, numCh, data)
	file = wave.open(args.outputfile, 'wb')
	file.setparams((numCh, int(sampWidth/8), sampRate, 0, 'NONE', ''))
	file.writeframes(data)
	file.close()


events = ('ean', 'eat', 'nic', 'npt', 'rmt', 'rwt', 'toa', 'tor', 'sva', 'svr',
			'svs', 'sps', 'ffa', 'ffw', 'ffs', 'fla', 'flw', 'fls', 'wsa', 'wsw',
			'bzw', 'hwa', 'hww', 'hua', 'huw', 'hls', 'tsa', 'tsw', 'evi', 'cem',
			'dmo', 'adr', 'blw', 'txf', 'txo', 'txb', 'txp', 'bzw', 'cfa', 'cfw',
			'dsw', 'smw', 'tra', 'trw', 'nat', 'nst', 'ava', 'avw', 'cae', 'eqw',
			'frw', 'hmw', 'lew', 'lae', 'toe', 'nuw', 'rhw', 'spw', 'vow', 'nmn', 
			'eww', 'ssa', 'ssw', 'fsw', 'fzw', 'smw', 'bhw', 'bww', 'chw', 'cww', 
			'dba', 'dbw', 'dew', 'eva', 'fcw', 'ibw', 'ifw', 'lsw', 'pos', 'wfa',
			'wfw', 'sqw', 'blu')

originators = ('pep', 'wxr', 'civ', 'eas', 'ean')

arg_patterns = {'event':r'|'.join(events), 'fips':r'^(\d{6})(\s+\d{6})*$', 
			'timestamp':r'(now)|(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', 'originator':r'|'.join(originators), 
		'duration':r'[0-9][0-9][0-9][0-9]',
		'callsign':r'.*', 'audioin':r'.+\.wav', 'outputfile':r'.+\.wav',
		'custom_msg':r'.*', 'eom':r'.*', 'type':r'.*'}

first_parser = argparse.ArgumentParser(add_help=False)
first_parser.add_argument("-z", "--fuzz", dest="custom_msg")

parser = argparse.ArgumentParser(description="A script to generate SAME CODED AFSK EAS messages", formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""Usage examples:
	Generate a simple test, 15 minute duration
		%(prog)s -e RWT -f 029177 -d 0015 -c WXYZ eas-rwt.wav
		%(prog)s -e RWT -f 029177 -d 0015 -t now -c "WXYZ FM" eas-rwt.wav

	Generate a test in the future
		%(prog)s -e RWT -f 029177 -d 0100 -t "12/31/2020 15:30" -c "WXYZ" eas-rwt.wav

	Generate a test with a voice message from input.wav
		%(prog)s -e RWT -f 037124 -d 0015 -c KXYZ -a input.wav eas-rwt.wav

	Fuzz mode: Generate a test with a non-standard EAS message using -z or --fuzz
		%(prog)s --fuzz "WXR-RAT-012345-111111+0123-BLAHBLAH-" output_eas.wav
""")

parser.add_argument("-z", "--fuzz", dest="custom_msg", help="pass a non-standard EAS message string to encoder")
parser.add_argument("-x", "--EOM", dest="eom", 	help="Exclude an EOM Signal",action='store_false')
parser.add_argument("-o", "--org", dest="originator",  help="Set the message originator ie WXR CIV EAS PEP EAN", default='WXR')
parser.add_argument("-e", "--event", dest="event", help="set the event type", default='RWT')
parser.add_argument("-f", "--fips", dest="fips", nargs='+', metavar=('FIPS','FIPS2'), help="set the destination fips codes", required=True)
parser.add_argument("-d", "--dur", dest="duration",	help="set the event duration HHMM, 15 minute increment work up to one hour, after that it is 30 minutes, i.e. 0015, 0130, etc.", default='0000')
parser.add_argument("-t", "--start", dest="timestamp", default="now", help="override the start timestamp, format is 'MM/DD/YYYY HH:MM' UTC timezone or use 'now' (default)")
parser.add_argument("-c", "--call", dest="callsign", help="set the originator call letters or id", default="NFM/FM")
parser.add_argument("-a", "--audio-in", dest="audioin", type=str, help="insert audio file between EAS header and eom; max length is 2 minutes")
parser.add_argument('outputfile', metavar='OUTPUT.WAV', default="OUTPUT.wav", type=str)


args1, args2 = first_parser.parse_known_args()
if args1.custom_msg is None:
	args = parser.parse_args(args2)
else:
	default_cmd = ['-z', args1.custom_msg, '-e', 'RWT', '-f', '000000', '-d', '0030', '-c', 'KACN/NWS', '-x', 'yes', 'output.wav']
	default_cmd.extend(args2)
	args = parser.parse_args(default_cmd)

timeslanguage = { r'now': time.time(), r'tomorrow': time.time() + 24 * 60 * 60, r'1 days*': time.time() + 24 * 60 * 60  }

if __name__ == "__main__":
	main()

