# selfstats.py: A stateless selfbot for Clash Royale Stats
### Authors:
- [SharpBit](https://github.com/SharpBit)
### Contributors:
If you would like to become a *contributor*, join [the discord server](https://discord.gg/9NjbQCd) and talk to Jason#1510
*Earn a special role in the server and get acknowledged for your efforts!*

### Join Us:
Join the [official discord server](https://discord.gg/9NjbQCd) to contribute to selfstats.py and be the first to beta test it!

## Hosting:
There are two ways you can host it, on a PC, or on Heroku for **free, 24/7!*

### Installation via Heroku (recommended)
No download is required, everything is done online. Read the installation guide [here](https://github.com/SharpBit/selfstats/wiki/Host-selfstats.py-24-7-For-Free-on-Heroku!) or watch the video tutorial(coming soon). It's possible to install the selfbot using your phone and it has been done before. If you have any questions, join the [support discord server](https://discord.gg/9NjbQCd) and we will be happy to help.

### PC Installation
You need the following to run the bot: (currently)
```
git+https://github.com/Rapptz/discord.py@rewrite
colorthief
psutil
crasync
cr-py
```
Do `pip install -r path\to\requirements.txt` to install the requirements.
Example: `pip install -r C:\Users\SharpBit\selfstats\requirements.txt`
### Setup
Open a terminal in the directory of the bot's location and type:
```
$ python3 selfstats.py
```
On first start the launcher will run and you will need to input data. After that the bot will launch without setup necessary.
If you need to edit your token, prefix, or Clash Royale tag, navigate into the data folder and open `config.json` and change the values
```
{
    "TOKEN": "your_token_here",
    "PREFIX": "cr.",
    "TAG": "your_tag_here"
}
```

### Features
- Fetch your profile, chest cycle, clan info, etc.
- Logout, tinyurl (link shortener), dominant color command
If you want to request features, [create an issue](https://github.com/SharpBit/selfstats/issues) on this repo.
This is a `stateless selfbot` (Saves no data). `This means you can [host it on heroku](https://github.com/SharpBit/selfstats/wiki/Host-selfstats.py-24-7-For-Free-on-Heroku!) 24/7 for free`

### Acknowledgements
The structure of the selfbot and custom context by [verixx](https://github.com/verixx) from selfbot.py
