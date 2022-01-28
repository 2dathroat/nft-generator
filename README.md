# nft-generator
Intuitive multi-platform NFT art generator

# Prerequisites
1. Clone the repository `git clone https://github.com/2dathroat/nft-generator.git`
2. Install the dependencies `pip3 install -r requirements.txt`

# Quick Start
1. Generate JSON input using https://2dathroat.github.io/rarity-calculator/
2. Make sure your directories are lined up accordingly. The script assumes path construct of `character/trait/variant.png`
3. Run `./nft.py --config <json_config>`

# Example
1. Example directory tree is as follow:

![image](https://user-images.githubusercontent.com/98057345/151591475-09cf3fdf-0f3b-4f3d-ad3d-783429318596.png)

2. Example config file can be found under `example/config.json` 
I have 2 characters: `tomer` and `bar`. Each one has the same number of traits and variants, they differ by the underlying `.png` files.

3. Running `./nft.py --base_path example --config config.json`
```
63 tokens generated for character: tomer
37 tokens generated for character: bar
6 variants generated for trait: backgrounds
variant: yellow occurrences: 13 rarity: 13.0
variant: purple occurrences: 23 rarity: 23.0
variant: orange occurrences: 29 rarity: 29.0
variant: None occurrences: 13 rarity: 13.0
variant: blue occurrences: 12 rarity: 12.0
variant: red occurrences: 10 rarity: 10.0
6 variants generated for trait: circles
variant: blue-circle occurrences: 16 rarity: 16.0
variant: red-circle occurrences: 18 rarity: 18.0
variant: None occurrences: 19 rarity: 19.0
variant: orange-circle occurrences: 14 rarity: 14.0
variant: green-circle occurrences: 17 rarity: 17.0
variant: yellow-circle occurrences: 16 rarity: 16.0
5 variants generated for trait: squares
variant: blue-square occurrences: 15 rarity: 15.0
variant: red-square occurrences: 36 rarity: 36.0
variant: green-square occurrences: 16 rarity: 16.0
variant: None occurrences: 16 rarity: 16.0
variant: orange-square occurrences: 17 rarity: 17.0
```
4. Tokens are generated to `character/output` directory. 
