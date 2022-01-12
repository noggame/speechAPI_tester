from pydub import AudioSegment
import os
import logging
import time

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