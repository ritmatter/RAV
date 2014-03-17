#!/usr/bin/python2.7
import numpy as np
from scipy.io import wavfile
#import matplotlib.pyplot as plt
from random import randint
import sys
import os

def pcm2float(sig, sampleSize):
    channels = sig.shape[1]
    new_sig = []
    max_size = (float) (2**(sampleSize-1))
    for x in range(0, len(sig)):
        new_sig.append([])
        for y in range(0, channels):
            new_sig[x].append(sig[x][y]/max_size)
    return new_sig

def float2pcm(pcm_vals, sampleSize, channels):
    new_sig = []
    max_size = 2**(sampleSize-1)
    for x in range(0, len(pcm_vals)):
        new_sig.append([])
        for y in range(0, channels):
            new_sig[x].append((int) (pcm_vals[x][y] * max_size))
    return new_sig

def getSampleSize(sig):
    if sig.dtype == 'int16':
        return 16
    elif sig.dtype == 'int32':
        return 32

def addBlock(randomSig, randomIndex, sig, channels, samples_per_block):
    for i in range(randomIndex, randomIndex + samples_per_block):
        newRow = []
        for y in range(0, channels):
            newRow.append(sig[i][y])

        randomSig.append(newRow)

def scramble(sig, sample_size, sampling_rate, channels, num_samples, shardTime, totalTime):
    # Each sample is really a full row!
    samples_per_block = (int) (shardTime * sampling_rate)   #size of each random block in samples
    total_size = (int) (totalTime * sampling_rate)/samples_per_block    #size of total sound in blocks

    randomSig = []
    size = 0    #current size in blocks
    while size < total_size:
        randomIndex = randint(0, num_samples - samples_per_block)
        addBlock(randomSig, randomIndex, sig, channels, samples_per_block)
        size += 1
    return np.array(randomSig)

def scrambleWithIndex(sig, sample_size, sampling_rate, channels, num_samples, shardTime1, shardTime2, totalTime):
    #Each sample is really a full row!

    print "shardtime1 is " + str(shardTime1)
    print "sampleRate is " + str(sampling_rate)
    print "SampleRate * shardTime is " + str(shardTime1 * sampling_rate)

    lowBound = (int) (shardTime1 * sampling_rate)   #low bound for shard length in samples
    highBound = (int) (shardTime2 * sampling_rate)  #low bound for shard length in samples
    total_size = (int) (totalTime * sampling_rate)  #size of total sound in samples
    randomSig = []
    size = 0    #current size in samples
    while size < total_size:
        randomBlockSize = randint(lowBound, highBound)
        randomIndex = randint(0, num_samples - randomBlockSize)
        addBlock(randomSig, randomIndex, sig, channels, randomBlockSize)
        size += randomBlockSize
    return np.array(randomSig)

def checkArgs(argv, argc):
    if (argc != 5):
        print "Error: Improper command line usage."
        print "Usage: python ./app.py <SRC_FILE> <DST_FILE> <SHARD_LEN> <TOTAL_LEN>"
        sys.exit()

def mix(file, lower, upper, total, clip_name):

    # fname = 'XC135672-Red-winged\ Blackbird1301.mp3'
    # oname = 'temp.wav'
    # cmd = 'lame --decode {0} {1}'.format( fname,oname )
    # os.system(cmd)

    sampling_rate, sig = wavfile.read(file);
    print sampling_rate
    num_samples = sig.shape[0]
    channels = sig.shape[1]
    sample_size = getSampleSize(sig)
    sig = scrambleWithIndex(sig, sample_size, sampling_rate, channels, num_samples, lower, upper, total)
    filename = "mixes/" + clip_name + ".wav"
    wavfile.write(filename, sampling_rate, np.array(sig))

# if ("-" in sys.argv[3]):
#     try:
#         bounds = sys.argv[3].split("-")
#         upper = float(bounds[1])
#         lower = float(bounds[0])
#         indexRange = True
#     except ValueError:
#         print "Error: Shard time must be a valid positive number"
#         sys.exit()
# else:
#     try:
#         upper = float(sys.argv[3])
#     except ValueError:
#         print "Error: Total time must be a valid positive number"
#         sys.exit()

# try:
#     total_len = float(sys.argv[4])
# except ValueError:
#     print "Error: Total length must be a valid positive number"
#     sys.exit()

# if (total_len < upper):
#     print "Error: Total time must be greater than the shard time"
#     sys.exit()

# try:
#     sampling_rate, sig = wavfile.read(SRC_FILE)
# except IOError:
#     print "Error: Could not read source wav file"
#     sys.exit()

# print "Processing {}...".format(SRC_FILE)
# channels = sig.shape[1]
# num_samples = sig.shape[0]
# sample_size = getSampleSize(sig)
# if indexRange:
#     sig = scrambleWithIndex(sig, sample_size, sampling_rate, channels, num_samples, lower, upper, total_len)
# else:
#     sig = scramble(sig, sample_size, sampling_rate, channels, num_samples, upper, total_len)
# wavfile.write(DST_FILE, sampling_rate, np.array(sig))
