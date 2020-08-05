import math, struct, random, array

pi = math.pi

def getFIRrectFilterCoeff(fc, sampRate, filterLen=20):
	ft = float(fc) / sampRate
	m = float(filterLen - 1)

	weights = []
	for n in range(filterLen):
		try:
			weight = math.sin( 2 * pi * ft * (n - (m / 2))) / (pi * (n - (m / 2)))
			hamming = 0.54 - 0.46 * math.cos( 2 * pi * n / m)
			weight = weight * hamming
		except:
			weight = 2 * ft
			hamming = 0.54 - 0.46 * math.cos( 2 * pi * n / m)
			weight = weight * hamming
		weights.append(weight)

	return weights

def filterPCMaudio(fc, sampRate, filterLen, sampWidth, numCh, data):
	samples = array.array('h',data)
	filtered = bytearray()

	w = getFIRrectFilterCoeff(fc, sampRate, filterLen)

	for n in range(len(w), len(samples) - len(w)):
		acc = 0
		for i in range(len(w)):
			acc += w[i] * samples[n - i]
		filtered += struct.pack('<h', int(math.floor(acc)))

	return filtered

def convertdbFStoInt( level, sampWidth):
	return math.pow(10, (float(level) / 20)) * 32767

def generateSimplePCMToneData(startfreq, endfreq, sampRate, duration, sampWidth, peakLevel, numCh):
	phase = 0 * pi
	level = convertdbFStoInt(peakLevel, sampWidth)
	pcm_data = bytearray()
	freq = startfreq
	slope = 0.5 * (endfreq - startfreq) / float(sampRate * duration)
	fade_len = int(0.001 * sampRate) * 0
	numSamples = int( round( sampRate * duration))

	for i in range(0, numSamples):
		freq = slope * i + startfreq
		fade = 1.0
		if i < fade_len:
			fade = 0.5 * (1 - math.cos(pi * i / (fade_len - 1)))
		elif i > (numSamples - fade_len):
			fade = 0.5 * (1 - math.cos(pi * (numSamples - i) / (fade_len - 1)))

		for ch in range(numCh):
			sample =  int(( fade * level * math.sin((freq * 2 * pi * i)/ sampRate + phase) ))
			dat = struct.pack('<h', sample)
			pcm_data += dat

	return pcm_data

def generateDualTonePCMData(freq1, freq2, sampRate, duration, sampWidth, peakLevel, numCh):
	phase = 0 * pi
	level = convertdbFStoInt(peakLevel, sampWidth)
	pcm_data = bytearray()
	fade_len = int(0.001 * sampRate) * 0
	numSamples = int( round( sampRate * duration))


	for i in range(0, numSamples):
		fade = 1.0

		if i < fade_len:
			fade = 0.5 * (1 - math.cos(pi * i / (fade_len - 1)))
		elif i > (numSamples - fade_len):
			fade = 0.5 * (1 - math.cos(pi * (numSamples - i) / (fade_len - 1))) 

		for ch in range(numCh):
			sample =  int(( fade * level * (0.5 * math.sin((freq1 * 2 * pi * i)/ sampRate + phase) + 0.5 * math.sin((freq2 * 2 * pi * i)/ sampRate + phase) )))
			dat = struct.pack('<h', sample)
			pcm_data += dat

	return pcm_data

def generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel, numCh, stringData):
	pcm_data = bytearray()
	bitstream = ''
	bitduration = 1.0 / bitrate
	for byte in stringData:
		bytebits = "{0:08b}".format(ord(byte))
		bitstream += bytebits[::-1]

	one_bit = generateSimplePCMToneData(markF, markF, sampRate, bitduration, sampWidth, peakLevel, numCh)
	zero_bit = generateSimplePCMToneData(spaceF, spaceF, sampRate, bitduration, sampWidth, peakLevel, numCh)

	for bit in bitstream:
		pcm_data +=  one_bit if bit == '1' else zero_bit

	return pcm_data