# -*- coding: utf-8 -*-

import argparse
import configparser
import module

config_file = configparser.ConfigParser()
config_file.read("config.ini")
config = dict(config_file.items('default'))


class generate_chiper_alphabet_action(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("Generate new chiper alphabet")
        data = module.crypto_table_dictionary_generate(int(config['num']), config['alphabet'])
        module.save_json_to_file(config['file'], data)
        exit()

if __name__ == '__main__':
    # add num option
    # add function to update config file
    # change how A works, need to change whole msg or eath line

    parser = argparse.ArgumentParser()
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-e', '--encrypt', help='Encrypt', action='store_true')
    group1.add_argument('-d', '--decrypt', help='Decrypt', action='store_true')

    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('-s', '--string', help='input string')
    group2.add_argument('-i', '--input', help='Open file to encrypt.')

    parser.add_argument('-a', '--alter', help='Alter start position.')
    parser.add_argument('-g', '--generate', help="Generates a new chiper alphabet, can't be used with other flags", action=generate_chiper_alphabet_action, nargs=0)
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
