from pydub import AudioSegment
import os
import logging
import time
import pathlib

import numpy
import librosa
import soundfile

def convertWAVtoMP3(srcFile):

    if not str(srcFile).endswith('.wav'):
        logging.exception(f'[Exception] {__name__} - source file is not .wav extension')
        return

    ext_mp3 = srcFile[:-4]+'.mp3'
    if not os.path.isfile(ext_mp3):
        try:
            logging.info(f'converting {srcFile} to mp3')
            voice = AudioSegment.from_file(file=srcFile)
            voice.export(ext_mp3, format="mp3")

            # waiting depends on src. size
            waitForCvt = (os.path.getsize(srcFile)/1024000)+1
            time.sleep(waitForCvt)

        except RuntimeError:
            logging.error(f'[ERR] {__name__} - Fail to convert wav to mp3 file')


def convert_PCM_To_WAV(target, dest, org_sr, re_sr):
    ### read file (with pcm, wav)
    f=open(target, 'rb')
    buf = bytearray(f.read())
    pcm_data = numpy.frombuffer(buf, dtype='int16')
    wav_data = librosa.util.buf_to_float(x=pcm_data, n_bytes=2)

    ### convert/write file
    resample = librosa.resample(wav_data, orig_sr=org_sr, target_sr=re_sr)
    soundfile.write(dest, resample, re_sr, format='WAV', endian='LITTLE', subtype='PCM_16')

def makeResamplingData(targetDirPath, org_sr, re_sr):

    for root, dirs, files in os.walk(targetDirPath):
        # Recursion
        for dir in dirs:
            makeResamplingData(f"{root}/{dirs}", org_sr, re_sr)

        # Converting
        for file in files:
            if file.endswith('.wav'):
                target = f"{root}/{file}"
                dest = f"{root}/{file[:-4]}_{re_sr}.wav"

                f=open(target, 'rb')
                buf = bytearray(f.read())
                wav_data = librosa.util.buf_to_float(x=buf, n_bytes=2)
                resample = librosa.resample(wav_data, orig_sr=org_sr, target_sr=re_sr)    # re-sampling
                f.close()
                soundfile.write(dest, resample, re_sr, format='WAV', endian='LITTLE')   # write

            elif file.endswith('.raw'):
                target = f"{root}/{file}"
                dest = f"{root}/{file[:-4]}_{re_sr}.wav"

                f=open(target, 'rb')
                buf = bytearray(f.read())
                pcm_data = numpy.frombuffer(buf, dtype='int16')
                wav_data = librosa.util.buf_to_float(x=pcm_data, n_bytes=2)
                resample = librosa.resample(wav_data, orig_sr=org_sr, target_sr=re_sr)    # re-sampling
                f.close()
                soundfile.write(dest, resample, re_sr, format='WAV', endian='LITTLE')   # write