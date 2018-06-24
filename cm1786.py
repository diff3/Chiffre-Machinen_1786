# -*- coding: utf-8 -*-

import argparse
import configparser
import module

config_file = configparser.ConfigParser()
config_file.read("config.ini")

config = {}
config['alphabet'] = config_file.get('default', 'alphabet')
config['alter'] = int(config_file.get('default', 'alter'))
config['file'] = config_file.get('default', 'file')
config['num'] = int(config_file.get('default', 'number_of_alphabets'))
config['outfile'] = config_file.get('default', 'outfile')

def main():
    global config

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generate', default=False, required=False,
                        help='Generate crypto table', action='store_true')
    args, unknown = parser.parse_known_args()

    if args.generate == True:
        print("Generate new chiper alphabet")
        data = module.crypto_table_dictionary_generate(config['num'], config['alphabet'])
        module.save_json_to_file(config['file'], data)

        if len(unknown) < 1:
            exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--alter', help='Alter start position.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', help='Encrypt', action='store_true')
    group.add_argument('-d', '--decrypt', help='Decrypt', action='store_true')
    group_input = parser.add_mutually_exclusive_group(required=True)
    group_input.add_argument('-s', '--string', help='input string')
    group_input.add_argument('-i', '--input', help='Open file to encrypt.')
    parser.add_argument('-o', '--output', help='Save encrypted text to file.')
    args, unknown = parser.parse_known_args()

    print("Chiffre-Machinen 1786")
    print("---------------------\n")

    if args.alter:
        config['alter'] = args.alter

    if args.input:
        msg = module.load_message_file(args.input)

    if args.output:
        config['outfile'] = args.output

    if args.string:
        msg = args.string


    chiper_alphabet = module.load_crypto_tabel_file(config['file'])

    if args.encrypt == True:
        text = module.encrypt_message(msg, chiper_alphabet, config['alter'])

        print ("Message: \n%s\n") % (msg)
        print ("Encoded: \n%s\n") % (text)

    if args.decrypt == True:
        chiper_alphabet_inverted = module.crypto_table_dictionary_inverted(chiper_alphabet, config['num'] )

        text = module.decrypt_message(msg, chiper_alphabet_inverted)
        print ("Encoded: \n%s\n") % (msg)
        print ("Decoded: \n%s\n") % (text)

    if config['outfile']:
        module.save_output_to_file(config['outfile'], text)


if __name__ == '__main__':
    main()
