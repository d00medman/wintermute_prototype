from kafka import KafkaConsumer
import pandas as pd
import numpy as np

import pixel_to_grid_translation_algorithm as pixel_grid_translator

consumer = KafkaConsumer('emulator_to_environment')
for message in consumer:
    '''
    Almost certainly going to want greater encapsulation after this. Regardless, am able to send state from actuation and format
    it in this file. Huge win.
    '''
    print (f'message of size {len(message.value)} written to emulator_to_environment')
    decoded_message = message.value.decode('utf-8')
    print (f'message of size {len(decoded_message)} decoded. type {type(decoded_message)} first 100 {decoded_message[0:256]}')
    decoded_sans_brackets = decoded_message.replace(']','').replace('[','')
    formatted_decoded_ints = [int(i) for i in decoded_sans_brackets.split(",")]
    print (f'formatted_decoded_message of size {len(formatted_decoded_ints)} decoded. type {type(formatted_decoded_ints)} first 100 {formatted_decoded_ints[0:256]}')
    pixel_grid = pixel_grid_translator.create_pixel_grid(formatted_decoded_ints)
    dominant_color_grid = pixel_grid_translator.reduce_grid(pixel_grid)
    print('possible character tile: ', pixel_grid[9][8])
    print('Dominant color grid: ', pd.DataFrame(dominant_color_grid))
