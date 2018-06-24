# -*- coding: utf-8 -*-

import random
import os.path
import json


def crypto_table_dictionary_generate(num, alphabet):
    chiper_alphabet = {}

    for index in range(num):
        chiper_alphabet[index] = {}

        for char in alphabet:
            rand_formated = get_uniqe_random(chiper_alphabet, index, char)
            chiper_alphabet[index][char] = rand_formated

    return chiper_alphabet


def crypto_table_dictionary_inverted(chiper_alphabet, num = 57):
    chiper_alphabet_inverted = {}

    for index in range(num):
        chiper_alphabet_inverted[index] = {}
        chiper_alphabet_inverted[index] = dict((value, key) for (key, value) in chiper_alphabet[str(index)].items())

    return chiper_alphabet_inverted


def decrypt_message(msg, chiper_alphabet_inverted):
    decoded, string = [], []

    msg_list = msg.split('\n')
    msg_list_filtered = filter(None, msg_list)

    alter = int(msg_list_filtered[0][msg_list_filtered[0].index('K')+1:])
    msg_list_filtered[0] = msg_list_filtered[0][:msg_list_filtered[0].index('K')-1]

    index = 0 + alter

    for text in msg_list_filtered:
        text = text.split(' ')
        text_filtered = filter(None, text)

        text_filtered.reverse()

        for number in text_filtered:
            try:
                string.append(chiper_alphabet_inverted[index][str(number)])
                index = 0 if index > 55 else index + 1
            except:
                print("Key error, you are trying to decrypt with wrong chiper_alphabet")
                exit()

        decoded.append(''.join(string) + '\n')
        string = []

    return ''.join(decoded).replace('-',' ')


def encrypt_message(msg, chiper_alphabet, alter):
    encoded, string,  = [], []

    msg_list = msg.upper().replace(' ','-').split('\n')
    msg_list_filtered = filter(None, msg_list)

    index = 0 + int(alter)

    string.append("K%s" %(alter))

    for text in msg_list_filtered:
        for char in text:
            try:
                string.append(chiper_alphabet[str(index)][char])
                index = 0 if index > 55 else index + 1
            except:
                print("You are trying to encrypt a unsuported character (%s). exit") %(char)
                exit()

        encoded.append(' '.join(reversed(string)).lstrip() + "\n")
        string = []

    return ''.join(encoded)


def get_uniqe_random(chiper_alphabet, index, char):
    rand = random.randint(0,99)
    rand_formated = '{num:02d}'.format(num=rand)

    if (rand_formated in chiper_alphabet[index].values()) == True:
        return get_uniqe_random(chiper_alphabet, index, char)

    return rand_formated


def load_crypto_tabel_file(file):
    if not os.path.exists(file):
        print("No valid crypto table file.")
        print("You need to generate one with cm1786 -g")
        exit()

    with open(file, 'r') as f:
        chiper_alphabet = json.load(f)

    return chiper_alphabet


def load_message_file(file):
    with open(file, 'r') as f:
        message_file = f.read()

    return message_file


def save_json_to_file(filename, chiper_alphabet):
    print ("Saved to file: %s") %(filename)
    with open( filename, 'w' ) as outfile:
        json.dump(chiper_alphabet, outfile, indent=4, sort_keys=False)


def save_output_to_file(outfile, msg):
    print ("Saved message to file: %s") %(outfile)
    with open(outfile, 'w') as file:
        file.write(msg)
