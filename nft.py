#!/usr/bin/python3

import random
import click
import json
import logging
import os
import itertools
from collections import defaultdict
from PIL import Image


def _generate_single_token(token, characters, traits):
    token.append(random.choices(characters, [i['weight'] for i in characters])[0]['name'])
    for t in traits:
        logging.info(f'generating trait {t["type"]}')
        token.append(random.choices(t['variants'], [i['weight'] for i in t['variants']])[0]['type'])

def generate_single_token(characters, traits, generated_set):
    """ Generates a single unique token """
    
    token = []
    _generate_single_token(token, characters, traits)
    logging.info(f'candidate token {token}')
    # regenerate existing or invalid token
    while all(i is None for i in token) or tuple(token) in generated_set:
        logging.info(f'existing token: {token}, regenerating')
        token = []
        _generate_single_token(token, characters, traits)
    logging.info(f'generated token: {token}')
    generated_set.add(tuple(token))

def validate(config):
    """ Validates config """
    
    assert 'size' in config
    assert 'traits' in config
    assert config['size'] >= 1
    assert len(config['traits']) >= 1
    assert len(config['traits'][0]['variants']) >= 1

    # validate 'size' tokens can be uniquly generated
    n = len(config['characters']) 
    for i in config['traits']:
        n *= len(i['variants'])

    assert config['size'] <= n, f'Not enough variants to generate {config["size"]} unique tokens \
        (can generate up to {n} with current config)' 

def analyze(config, character_tokens):
    """ Analyzes generated tokens for interesting metrics """

    all_tokens = []
    for k, v in character_tokens.items():
        logging.warn(f"{len(v)} tokens generated for character: {k}")
        all_tokens.extend(v)

    # group by variants per trait and analyze rarity
    transposed = list(zip(*all_tokens))[1:]
    for n, i in enumerate(transposed):
        variants = defaultdict(int)
        for j in i:
            variants[j] += 1

        logging.warn(f"{len(variants)} variants generated for trait: {config['traits'][n]['type']}")
        for k in variants:
            logging.warn(f"variant: {k} occurrences: {variants[k]} rarity: {variants[k]*100/config['size']:.2f}%")


@click.command()
@click.option('-c', '--config', required=True, type=str, help='Location of NFT config file')
@click.option('-p', '--base_path', default='.', type=str, help='Base path of character directories')
@click.option('-d', '--debug', default=False, type=bool, help='Verbose run')
@click.option('-i', '--skip_images', default=False, type=bool, help='Skip image generation. Useful to analyze expected output')
@click.option('-s', '--skip_analysis', default=False, type=bool, help='Skip token analysis')
def main(config, base_path, debug, skip_images, skip_analysis):
    """ Generate random tokens with different traits given a config file. """

    with open(config) as config_file:
        config_json = json.load(config_file)

    if debug:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s', level=logging.WARNING)

    validate(config_json)

    logging.info('generating tokens')

    # generate the unique tokens first
    generated_set = set()
    for i in range(config_json['size']):
        generate_single_token(config_json['characters'], config_json['traits'], generated_set)

    # convert to dict character->list of tokens for easier manipulation 
    character_tokens = defaultdict(list)
    for i in generated_set:
        character_tokens[i[0]].append(i[1:])

    logging.warn(f'tokens and characters: {character_tokens}')

    if not skip_analysis:
        analyze(config_json, character_tokens)
    #
    # per token create the images by overlaying each trait.
    #

    if skip_images:
        return

    # first, create the output directories
    for i in config_json['characters']:
        if not os.path.exists(f'{base_path}/{i["name"]}/output'):
            os.mkdir(f'{base_path}/{i["name"]}/output')

    # next, iterate over generated tokens per character to generate the images
    for char, char_tokens in character_tokens.items():
        base_img = None
        char_config = next(filter(lambda c:c['name'] == char, config_json['characters']))

        # map out z index to trait order
        z_order = sorted(config_json['traits'], key=lambda i:i['z-index'])
        # put the character in its position as well
        for char_pos, i in enumerate(z_order):
            if char_config['z-index'] <= i['z-index']:
                break

        traverse_order = list(map(lambda j:[i['type'] for i in config_json['traits']].index(j['type']), z_order))
        # arbitrary lets have -1 represent the character
        traverse_order.insert(char_pos, -1)
        for n, i in enumerate(char_tokens):
            # overlay the traits according to z index order
            for j in traverse_order:
                # this is the character (he must exist)
                if j == -1:
                    im = Image.open(f'{base_path}/{char}/{char}.png').convert('RGBA')
                # nothing to overlay
                elif i[j] is None:
                    continue
                else:
                    im = Image.open(f'{base_path}/{char}/{config_json["traits"][j]["type"]}/{i[j]}.png').convert('RGBA')
                if base_img is None:
                    base_img = Image.new(mode='RGBA', size=im.size)
                base_img.paste(im, (0, 0), mask=im)
                #im1 = com

            base_img.save(f'{base_path}/{char}/output/{n}.png')
            base_img = None


if __name__ == '__main__':
    main()
