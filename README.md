# selfstats.py: A stateless selfbot for Clash Royale Stats
## NOTE:
This project is depracated. Selfbots are against Discord's TOS and DO NOT BLAME ME IF YOU GET FLAGGED OR BANNED (btw the discord server and username below is outdated). Btw why do u even still play cr the game is ded
### Authors:
- [SharpBit](https://github.com/SharpBit)
### Contributors:
If you would like to become a *contributor*, join [the discord server](https://discord.gg/9NjbQCd) and talk to `SharpBit#1510`
*Earn a special role in the server and get acknowledged for your efforts!*

### Join Us:
Join the [official discord server](https://discord.gg/9NjbQCd) to contribute to selfstats.py and be the first to beta test it!

#### Star the repo for a special role in the discord server!

## Hosting:
There are two ways you can host it, on a PC, or on Heroku for **free, 24/7!**

### Installation via Heroku (recommended)
No download is required, everything is done online. Read the installation guide [here](https://github.com/SharpBit/selfstats/wiki/Host-selfstats.py-24-7-For-Free-on-Heroku!) or watch the video tutorial(coming soon). It's possible to install the selfbot using your phone and it has been done before. If you have any questions, join the [support discord server](https://discord.gg/9NjbQCd) and we will be happy to help.

### PC Installation
You need the following to run the bot: (currently)
```
git+https://github.com/Rapptz/discord.py@rewrite
colorthief
psutil
crasync
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
- [x] Fetch your profile, chest cycle, clan info, etc.
- [x] View more detailed info about your clan
- [x] Individually get your trophies (current, best, legend)
- [x] Find out how much longer until you get that super magical chest
- [x] Clan Chest Info
- [x] See your chest cycle
- [x] Find out when your next shop offer is
- [ ] Custom Prefix
- [x] Logout, tinyurl (link shortener), dominant color command, put code into a hastebin, get the source code for a command
If you want to request features, [create an issue](https://github.com/SharpBit/selfstats/issues) on this repo.
This is a `stateless selfbot` (Saves no data). *This means you can [host it on heroku](https://github.com/SharpBit/selfstats/wiki/Host-selfstats.py-24-7-For-Free-on-Heroku!) 24/7 for free*
