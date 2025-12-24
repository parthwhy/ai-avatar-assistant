# 🚀 SAGE Quick Start Guide

Get SAGE up and running in 5 minutes!

## ⚡ Prerequisites

- **Windows 10/11** (primary support)
- **Python 3.10+** ([Download here](https://python.org/downloads/))
- **Microphone** (for voice commands)
- **Internet connection** (for AI APIs)

## 🎯 Quick Installation

### Option 1: Automated Setup (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/sage.git
cd sage

# 2. Run setup script
python setup.py

# 3. Follow the prompts to complete setup
```

### Option 2: Manual Setup
```bash
# 1. Clone and navigate
git clone https://github.com/yourusername/sage.git
cd sage

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy configuration
copy .env.example .env
```

## 🔑 Get API Keys (Required)

### 1. Groq API Key (Free)
1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up/login
3. Create API key
4. Copy key to `.env` file: `GROQ_API_KEY=your_key_here`

### 2. Picovoice Access Key (Free)
1. Visit [console.picovoice.ai](https://console.picovoice.ai/)
2. Sign up/login
3. Create access key
4. Copy key to `.env` file: `PICOVOICE_ACCESS_KEY=your_key_here`

### 3. OpenRouter API Key (Optional)
1. Visit [openrouter.ai](https://openrouter.ai/)
2. Sign up and add credits ($5 minimum)
3. Create API key
4. Copy key to `.env` file: `OPENROUTER_API_KEY=your_key_here`

## 🎮 First Run

```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Start SAGE
python main.py
```

## 🎤 Try These Commands

Once SAGE is running, try these voice commands:

### Basic Commands
- **"Hey SAGE"** - Wake up the assistant
- **"What time is it?"** - Get current time
- **"Open Chrome"** - Launch Chrome browser
- **"Set volume to 50"** - Adjust system volume

### Productivity
- **"What's the weather in Mumbai?"** - Get weather info
- **"Calculate 25 times 30"** - Math calculations
- **"Set a timer for 5 minutes"** - Set countdown timer

### Communication
- **"Send email to manager"** - Compose email (will ask for details)
- **"Send WhatsApp message to John saying hello"** - Send message

### Media
- **"Play Shape of You on Spotify"** - Play specific song
- **"Next song"** - Skip to next track
- **"Pause music"** - Pause playback

### Advanced
- **"What's on my screen?"** - Analyze current screen (requires OpenRouter)
- **"Take a screenshot"** - Capture screen
- **"Schedule meeting with John tomorrow at 3 PM"** - Create meeting

## 📋 Setup Checklist

- [ ] Python 3.10+ installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured with API keys
- [ ] Microphone working
- [ ] SAGE starts without errors
- [ ] Wake word "Hey SAGE" detected
- [ ] Basic commands working

## 🔧 Troubleshooting

### SAGE won't start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check for errors
python main.py
```

### Wake word not working
- Check microphone permissions in Windows Settings
- Ensure microphone is not muted
- Verify `PICOVOICE_ACCESS_KEY` in `.env` file
- Try speaking louder and clearer

### Voice commands not recognized
- Check internet connection
- Speak clearly after "Hey SAGE"
- Wait for "Yes, I'm listening" response
- Commands timeout after 8 seconds

### TTS not working
- Check Windows Speech settings
- Ensure speakers/headphones are working
- Try: `python -c "from voice.tts import speak; speak('test')"`

### API errors
- Verify API keys in `.env` file
- Check API key quotas/limits
- Ensure internet connection is stable

## 📚 Next Steps

### Customize SAGE
1. **Add Contacts**: Edit `data/contacts.json` with your contacts
2. **Record Tasks**: Use the GUI to record repetitive tasks
3. **Create Routines**: Set up morning/evening routines

### Explore Features
- **Screen Analysis**: "What options are available?"
- **Content Generation**: "Write a birthday invitation"
- **Task Recording**: Click "Record" button in GUI
- **Meeting Scheduling**: "Schedule meeting with team"

### Advanced Setup
- **Gmail Integration**: Add `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` to `.env`
- **WhatsApp**: Install WhatsApp Desktop for messaging features
- **Spotify**: Install Spotify Desktop for music control

## 🆘 Getting Help

- **Documentation**: Read `README.md` for full details
- **Issues**: Create GitHub issue for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Contributing**: See `CONTRIBUTING.md` to help improve SAGE

## 🎉 You're Ready!

SAGE is now set up and ready to boost your productivity! Start with simple commands and gradually explore more advanced features.

**Happy automating!** 🤖✨