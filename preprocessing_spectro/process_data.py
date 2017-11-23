#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 09:41:59 2016

@author: danny
"""
from label_func import label_frames, parse_transcript, label_transcript
from data_functions import list_files, phoneme_dict, check_files
from cepstrum import get_mfcc
from scipy.io.wavfile import read
from glob import glob
import numpy
import tables

def proc_data (pattern,f_ex,params,l_path,d_path,conv_table, CGN):
    # get list of audio and transcript files 
    # audio_files = [d_path+"/"+x for x in list_files(d_path)]
    audio_files =  glob(d_path)
    audio_files.sort()      
    
    # label_files = [l_path+"/"+ x for x in list_files (l_path)]
    label_files =  glob(l_path)
    label_files.sort()
    
    print(audio_files)
    print(label_files)
    
    # create h5 file for the processed data
    data_file = tables.open_file(params[5], mode='a')
    
    # create pytable atoms
    # if we want filterbanks the feature size is #filters+1 for energy x3 for delta and double delta
    if params[4]==True:
        feature_shape=(params[1]+1)
    # features are three times bigger if deltas are used
        if params[6]==True: 
             feature_shape=feature_shape*3
    # if we make MFCCs we take the first 12 cepstral coefficients and energy + delta double delta = 39 features
    else:
        feature_shape=(39)
    # N.B. label size is hard coded. It provides phoneme and 7 articulatory feature
    # labels

    
    # atom for the spectrogram values (fft)
    s_atom = tables.Float64Atom()
    # create a feature and label group branching of the root node
    spectra = data_file.create_group("/", "spectra")
    
    # create a dictionary from the conv table
#    cgndict = phoneme_dict(conv_table)
    
    # check if the audio and transcript files match 
    if check_files(audio_files, label_files, f_ex):
    
    # len(audio_files) 
        for x in range (0,len(audio_files)): #len(audio_files)
            print ('processing file :' + audio_files[x] )
            # create new leaf nodes in the feature and leave nodes for every audio file
            s_table = data_file.create_earray(spectra, audio_files[x][-12:-4], s_atom, (0, 256), expectedrows=100000)
            # read audio samples
            input_data = read(audio_files[x])
            # sampling frequency
            fs=input_data[0]
            # get window and frameshift size in samples
            s_window = int(fs*params[2])
            s_shift=int(fs*params[3])
            
            # create mfccs
            spectrum = get_mfcc (input_data,params[0],params[1],s_window,s_shift,params[4],params[6])    
            s_table.append(spectrum)
    else: 
        print ('audio and transcript files do not match')
    # close the output files
    data_file.close()
    data_file.close()
    
