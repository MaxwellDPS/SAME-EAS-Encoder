from afsk import *

eastestgen_core_version = "0.0.1 BETA"

def generateEASpcmData(org, event, fips, eventDuration, timestamp, stationId, sampRate, sampWidth, 
	                peakLevel, numCh, msgaudio=None, customMsg=None, eom=None):
	"Put together info to generate an EAS message"

	markF = 2083.3
	spaceF = 1562.5
	bitrate = 520.3
	pcm_data = ''

	preamble = '\xab' * 16
	if eom is not None:
		message = 'ZCZC-{0}-{1}-{2}+{3}-{4}-{5: <8}-'.format(org, event, "-".join(fips[0:31]), 
					eventDuration, timestamp, stationId[0:8])
		header = generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel,
						numCh, preamble + message.upper())
		silence = generateSimplePCMToneData(10000, 10000, sampRate, 1, sampWidth, -94, numCh)	
			
		pcm_data = silence
		
		begintones = generateDualTonePCMData(markF, markF, sampRate, 0.015, sampWidth, peakLevel, numCh)
			
		for i in range(3):
			pcm_data = pcm_data + begintones + header + begintones + silence
		attn_tones = generateDualTonePCMData(960, 853, sampRate, 8, sampWidth, peakLevel, numCh)
		pcm_data = pcm_data + silence + attn_tones + silence
		# attn_tones = generateDualTonePCMData(960, 853, sampRate, 8, sampWidth, peakLevel, numCh)
		# pcm_data = pcm_data + silence + attn_tones + silence
		return pcm_data
	else:
		endOfMessage = 'NNNN'
                eom = generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel,
                                                numCh, preamble + endOfMessage)
                silence = generateSimplePCMToneData(10000, 10000, sampRate, 1, sampWidth, -94, numCh)	

                begintones = generateDualTonePCMData(markF, markF, sampRate, 0.02, sampWidth, peakLevel, numCh)
                
                pcm_data = begintones + eom + begintones + silence

                for i in range(2):
                        pcm_data = pcm_data + begintones + eom + begintones + silence
                                
                return pcm_data

if __name__ == "__main__":
    import wave, time

    sampRate = 44100
    duration = 10
    sampWidth = 16
    peakLevel = -0.001
    numCh = 2
    now = time.gmtime()
    timestamp = time.strftime('%j%H%M', now) 

    data = generateEASpcmData('EAS', 'RWT', '029077', '0030', timestamp, 'KXYZ/FM', sampRate, 
	    sampWidth, peakLevel, numCh)
    data = recursiveFilterPCMaudio(4000, sampRate, sampWidth, numCh, data)
    file = wave.open('testfile-filt.wav', 'wb')
    file.setparams( (numCh, sampWidth/8 , sampRate, duration * sampRate, 'NONE', '') )
    file.writeframes(data)
    file.close()

