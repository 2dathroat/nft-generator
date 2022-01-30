# nft-generator
Intuitive multi-platform NFT art generator

# Installation
1. Make sure you have python3 (https://www.python.org/downloads/)
2. Clone the repository `git clone https://github.com/2dathroat/nft-generator.git`
3. Install the dependencies `pip3 install -r requirements.txt`

# Quick Start
1. Generate JSON input using https://2dathroat.github.io/rarity-calculator/
2. Make sure your directories are lined up accordingly, see below example. The script assumes path construct of `character/trait/variant.png` and `character/character.png`
3. Run `./nft.py --config <json_config>`

# Example
Resulting tokens (compiled to gif):

![Webp net-gifmaker](https://user-images.githubusercontent.com/98057345/151698651-e311df3d-de4f-4734-88ac-46807dc189b4.gif)

1. Example directory tree is as follow:

![image](https://user-images.githubusercontent.com/98057345/151698564-e3b0d76a-265b-47d5-a6dc-dad000c80acb.png)

2. Example config file can be found under `example/config.json` 
I have 2 characters: `blueEmoji` and `yellowEmoji`. Each one has the same number of traits and variants, they differ by the underlying `.png` files.

3. Running `./nft.py --base_path example --config config.json`
```
5 tokens generated for character: blueEmoji
5 tokens generated for character: yellowEmoji
2 variants generated for trait: eyes
variant: smile occurrences: 5 rarity: 50.00%
variant: sad occurrences: 5 rarity: 50.00%
2 variants generated for trait: mouth
variant: black occurrences: 4 rarity: 40.00%
variant: white occurrences: 6 rarity: 60.00%
```
4. Tokens are generated to `character/output` directory. See output of tokens in the new tree structure

![image](https://user-images.githubusercontent.com/98057345/151698620-a1def258-b3b2-49d5-bccb-46e9cf433241.png)

