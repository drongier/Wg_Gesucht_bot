# 🏠 WG-Gesucht Bot

A Python bot that monitors apartment listings on Kleinanzeigen and sends real-time notifications via Telegram when new suitable listings are found.

## ✨ Features

- 🔍 **Real-time monitoring** of Kleinanzeigen apartment listings
- 📱 **Telegram notifications** for new listings
- 🚫 **Smart filtering** to exclude unwanted listings (office spaces, swaps, etc.)
- 💾 **Duplicate prevention** - tracks already seen listings
- 📝 **Comprehensive logging** for monitoring and debugging
- ⚙️ **Configurable** via JSON configuration file

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- A Telegram bot token
- Your Telegram chat ID

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/wg-gesucht-bot.git
cd wg-gesucht-bot
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4 python-telegram-bot
```

### 3. Configure the bot

```bash
cp config.example.json config.json
nano config.json  # Edit with your actual values
```

## 🔧 Configuration

Create a config.json file with the following structure:

```json
{
    "BOT_TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
    "CHAT_ID": "YOUR_TELEGRAM_CHAT_ID",
    "URL": "https://www.kleinanzeigen.de/s-immobilien/berlin/preis:300:1200/c195l3331",
    "SEEN_IDS_FILE": "/path/to/seen_ids.json",
    "LOG_FILE": "/path/to/wgbot.log"
}
```

### Getting Telegram Credentials

1. **Create a bot**: Message `@BotFather` on Telegram
   - Send `/newbot`
   - Choose a name and username for your bot
   - Copy the token provided

2. **Get your Chat ID**: 
   - Start a conversation with your bot
   - Send any message
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Find your chat ID in the response

## 🚀 Usage

### Run the bot

```bash
python3 wg_gesucht_bot.py
```

### Run as a service (Raspberry Pi)

Create a systemd service for continuous monitoring:

```bash
sudo nano /etc/systemd/system/wgbot.service
```

```ini
[Unit]
Description=WG Gesucht Bot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/wg-gesucht-bot
ExecStart=/usr/bin/python3 /home/pi/wg-gesucht-bot/wg_gesucht_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable wgbot.service
sudo systemctl start wgbot.service
```

## 🎯 How It Works

1. **Monitoring**: The bot continuously scrapes the configured Kleinanzeigen URL
2. **Filtering**: Excludes listings containing unwanted keywords (offices, swaps, etc.)
3. **Duplicate Check**: Maintains a record of seen listings to avoid spam
4. **Notification**: Sends formatted Telegram messages for new suitable listings
5. **Logging**: Records all activities for monitoring and debugging

### Excluded Keywords

The bot automatically filters out listings containing:
- `tausch` (swaps)
- `nur frauen` (women only)
- `coworking`
- `büro` / `büroräum` / `büroraum` (office spaces)
- `praxis` (practice/clinic spaces)

## 📁 Project Structure

```
wg-gesucht-bot/
├── wg_gesucht_bot.py      # Main bot script
├── config.json            # Configuration (not tracked)
├── config.example.json    # Configuration template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── seen_ids.json         # Tracked listings (auto-generated)
└── wgbot.log            # Log file (auto-generated)
```

## 🔒 Security

- ⚠️ **Never commit config.json** - it contains sensitive tokens
- ✅ Use `config.example.json` as a template
- 🔐 Keep your bot token secure and private

## 📊 Monitoring

The bot provides comprehensive logging:

- 🚀 Startup notifications
- 🔍 Scan progress updates  
- 📊 Statistics (articles found, new listings, excluded items)
- ❌ Error handling and reporting

Check logs:
```bash
tail -f wgbot.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**401 Unauthorized Error**
- Check your bot token is correct
- Ensure you've started a conversation with your bot

**File Permission Errors**
- Verify the bot has write permissions for log and data files
- Check file paths in configuration

**No notifications received**
- Confirm your chat ID is correct
- Test the bot token with a simple API call
- Check if the search URL returns results

---

<div align="center">
  <strong>Happy apartment hunting! 🏠✨</strong>
</div>
