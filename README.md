# Sarah [![Build Status](https://travis-ci.org/semicode-ltd/sarah.svg?branch=master)](https://travis-ci.org/semicode-ltd/sarah)

Sarah is an English-like assistant that helps you with doing almost everything in SemiCode OS.

Sarah is your new girl friend &hearts;

She will take care of you and help you with your work. Just open a terminal anywhere you want, call her and she will be there for you.
Sarah supports a large amount of commands. They can be listed with the following command:

```bash
$ sarah list
```

## 🤖 NEW: AI-Powered Natural Language Interface

Sarah now includes an advanced AI agent that understands natural language! Instead of memorizing specific commands, you can now talk to Sarah naturally:

```bash
# Traditional command:
$ sarah weather New York

# AI-powered natural language:
$ sarah ai_agent "What's the weather like in New York?"
$ sarah ai_agent "Is it going to rain today?"
$ sarah ai_agent "Search for Python tutorials on YouTube"
$ sarah ai_agent "Tell me about Albert Einstein"
```

**Key AI Features:**

- 🧠 **Natural Language Understanding** - Talk to Sarah naturally
- 💬 **Conversational Context** - Remembers previous interactions
- 🎯 **Smart Intent Recognition** - Understands what you want to do
- 🔧 **Automatic Plugin Execution** - Maps language to Sarah commands
- 📊 **Learning** - Adapts to your usage patterns

See [AI Agent Documentation](plugins/ai_agent/README.md) for complete details.

Sarah uses only your username. She won't collect any personal information or send them to our servers. So we care about your privacy.

Sarah will respond to your greetings, your love or even your personal questions about her.
Just don't be rude ;)

## Some useful Sarah commands

Get movie or TV-Show information:

```bash
$ sarah watch titanic
Name : Titanic
Year of Releasing : 1997
Movie or Series : movie
Genre : Drama, Romance
Cast : Leonardo DiCaprio, Kate Winslet, Billy Zane, Kathy Bates
Ok I will watch it because it got 7.7 on imdb
```

Get the lyrics of a song:

```bash
$ sarah lyrics majerlazor leanon
<<it will output the lyrics of Major Lazors song "Lean on">>
```

Download file with resume-ability. Even if the link doesn't support resuming:

```bash
$ sarah download http://anylink.com/anyfile.tar.gz
```

Grabbing the entire content of a website for offline use:

```bash
$ sarah grab http://www.w3schools.com
```

Downloading Youtube video:

```bash
$ sarah nzli https://www.youtube.com/watch?v=7XTHdcmjenI
```

Translate any English word to Arabic word:

```bash
$ sarah translate pencil
قلم رصاص
```

Get small bio of anyone you want:

```bash
$ sarah whois Adam Levine
Adam Noah Levine (born March 18, 1979) is an American singer-songwriter, multi-instrumentalist, and actor.
He is the lead vocalist for pop rock band Maroon 5.
```

Generate "Hello World"-program in any programming language:

```bash
$ sarah first python

.py File Created Successfully , Check your Current Path
```

Get the weather of a specific city:

```bash
$ sarah weather khartoum
```

Test your internet connection speed:

```bash
$ sarah speedtest
```

Get the number of characters in any file:

```bash
$ sarah how many characters are in file.txt
34
```

Get Muslim prayer time **الأذان** (Muslim World League method)

```bash
$ sarah adhan oran Algeria
Prayer time for Algeria, Oran :
 Fajr 06:39
 Dhuhr 13:03
 Asr 15:38
 Maghrib 17:56
 Isha 19:22
```

Check the stock market :

```bash
$ sarah marketwatch yamaha jp all
```

# Roadmap

- add autotools support

# Installation

## 🐳 Docker Installation (Recommended)

The easiest way to run Sarah with full AI capabilities:

```bash
# Build Sarah with AI support
$ docker build -t sarah:latest .

# Run Sarah
$ docker run -it --rm sarah:latest sarah list

# Use AI agent
$ docker run -it --rm sarah:latest sarah ai_agent "what's the weather like?"

# Or use docker-compose
$ docker-compose up --build
```

## 📦 Manual Installation

Get all dependencies to run `Sarah` by executing:

```bash
$ sudo add-apt-repository ppa:vala-team/ppa/
$ sudo apt-get install software-properties-common
$ sudo apt-get install valac
$ sudo apt-get install libpeas-*
$ sudo apt-get install python-pip
$ sudo pip install -r requirements.txt

# For AI capabilities, also install:
$ python -m spacy download en_core_web_sm
```

## Getting started

### Docker (Easy)

```bash
$ docker run -it --rm sarah:latest sarah ai_agent "help"
```

### Manual Build

Switch to your project directory and run the following commands:

```bash
$ make
$ make install
$ export LD_LIBRARY_PATH=.
$ export GI_TYPELIB_PATH=.
$ ./sarah <some command to run>

# Try the AI agent
$ ./sarah ai_agent "what time is it?"
```

Enjoy your friendship with Sarah.

Made with &hearts; in Sudan.

SemiCode OS Core Team
