# 📦 Bin Packing Telegram Bot

An intelligent Telegram bot that solves the **Bin Packing Problem** using AI-powered combinatorial optimization. The bot leverages cloud-based LLMs with few-shot learning to find optimal packing solutions.

## 🌟 Overview

The Bin Packing Problem is a classic combinatorial optimization challenge where items of different sizes must be packed into bins with a fixed capacity, minimizing the number of bins used. This bot uses a Large Language Model trained with examples to solve this problem efficiently.

**🤖 Try it now**: [@lavashapatnisashBot](https://t.me/lavashapatnisashBot)

## ✨ Features

- **AI-Powered Optimization**: Uses GPT-based cloud LLM (gpt-oss:20b-cloud) to find optimal bin packing solutions
- **Few-Shot Learning**: Leverages 100+ pre-computed examples to guide the model
- **Visual Results**: Generates a PNG table showing the bin packing solution
- **Telegram Integration**: Easy-to-use conversational interface via Telegram
- **Combinatorial Efficiency**: Finds solutions with minimum number of bins and lowest load in the last bin

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│  (Telegram) │
└──────┬──────┘
       │
       │ Send items & capacity
       ▼
┌─────────────────┐
│    bot.py       │ ◄─── Main entry point
└────────┬────────┘
         │
         │ Parse input
         ▼
┌──────────────────────┐
│  ollama_client.py    │ ◄─── LLM communication
└────────┬─────────────┘
         │
         │ Build few-shot prompt
         ▼
┌──────────────────────┐
│   examples.json      │ ◄─── 100+ training examples
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│  Ollama API/LLM      │ ◄─── Cloud-based GPT model
└────────┬─────────────┘
         │
         │ JSON response
         ▼
┌──────────────────────┐
│  table_image.py      │ ◄─── Visualization
└────────┬─────────────┘
         │
         │ PNG image
         ▼
┌──────────────────────┐
│   User (Telegram)    │
└──────────────────────┘
```

## 📁 Project Structure

```
ollama/
├── bot.py                 # Main Telegram bot logic & message handlers
├── ollama_client.py       # LLM API client with few-shot prompting
├── build_examples.py      # Converts dataset to few-shot examples
├── table_image.py         # Generates PNG visualization of bins
├── dataset.txt            # Raw training data (100+ solved problems)
├── examples.json          # Processed few-shot examples in JSON format
├── requirements.txt       # Python dependencies
└── .venv/                 # Virtual environment (not tracked)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Ollama API Key (for cloud LLM access)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Davlatbek0710/AI-projecct.git>
   cd ollama
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   
   Edit `bot.py` and set your Telegram Bot Token:
   ```python
   BOT_TOKEN = "your-telegram-bot-token"
   ```
   
   Edit `ollama_client.py` and set your API key:
   ```python
   API_KEY = "your-ollama-api-key"
   ```

5. **Generate examples (optional)**
   
   If you want to regenerate the examples from the dataset:
   ```bash
   python build_examples.py
   ```
   This will create/update `examples.json` from `dataset.txt`.

6. **Run the bot**
   ```bash
   python bot.py
   ```

## 💬 Usage

1. Start a conversation with your bot on Telegram
2. Send a message with numbers separated by spaces:
   - First number: bin capacity
   - Remaining numbers: item sizes

**Example Input:**
```
400 200 150 85 75 74 68 60 50 32
```

**Expected Output:**
- The bot will respond with "Asking the model for optimal solution..."
- Then send a PNG image showing:
  - Bin numbers
  - Items in each bin
  - Total load per bin

**Example Solution:**
```
┌──────┬────────────────────┬──────┐
│ Bin #│ Items (desc.)      │ Load │
├──────┼────────────────────┼──────┤
│  1   │ 200, 150, 50       │ 400  │
│  2   │ 85, 75, 74, 68, 60 │ 362  │
│  3   │ 32                 │  32  │
└──────┴────────────────────┴──────┘
```

## 🔧 Configuration

### LLM Model Selection

In `ollama_client.py`, you can change the model:

```python
# Current model
MODEL_NAME = "gpt-oss:20b-cloud"

# Alternative (commented out)
# MODEL_NAME = "deepseek-v3.1:671b-cloud"
```

### Few-Shot Examples Count

Adjust the number of examples used per request in `ollama_client.py`:

```python
def ask_model_with_examples(user_input: str, n_examples: int = 4):
    # Default: 4 random examples per request
    # Increase for better accuracy, decrease for faster responses
```

## 📊 Dataset Information

The `dataset.txt` file contains 100+ pre-solved bin packing problems with the following format:

```
Capacity [TAB] Item1 Item2 ... Item10 [TAB] NumBins [TAB] OptimalOrder
```

Each line represents:
- **Capacity**: Maximum bin capacity (always 400 in current dataset)
- **Items**: 7-10 item sizes to be packed
- **NumBins**: Optimal number of bins needed
- **OptimalOrder**: The optimal ordering of items for packing

## 🧠 How It Works

1. **Input Parsing**: User sends space-separated numbers via Telegram
2. **Prompt Building**: System creates a few-shot prompt with 4 random examples from `examples.json`
3. **LLM Request**: Sends prompt to cloud-based GPT model via Ollama API
4. **Response Parsing**: Extracts JSON response containing bin assignments
5. **Visualization**: Generates PNG table using matplotlib
6. **Delivery**: Sends image back to user via Telegram

### System Prompt

The bot instructs the LLM to:
- Solve the bin packing problem
- Sort items in the most combinatorially efficient way
- Minimize the number of bins
- Minimize the load in the last bin (if multiple solutions exist)
- Output results in strict JSON format

## 📦 Dependencies

Key dependencies (see `requirements.txt` for full list):

- **aiogram** (3.23.0) - Telegram Bot framework
- **requests** (2.32.5) - HTTP client for API calls
- **matplotlib** (3.10.7) - Table visualization
- **Pillow** (12.0.0) - Image processing
- **aiofiles** (25.1.0) - Async file operations

## 🛠️ Development

### Building New Examples

To add more training examples:

1. Add new lines to `dataset.txt` following the tab-separated format
2. Run the builder script:
   ```bash
   python build_examples.py
   ```
3. Restart the bot to use the updated examples

### Testing

Send test inputs to your bot:

```
# Simple case
400 200 150 50

# Complex case  
400 300 95 90 82 69 48 42 28 11

# Edge case (items larger than capacity will fail)
100 200 50 30
```

## ⚠️ Important Notes

- **API Costs**: Each request to the LLM API may incur costs depending on your plan
- **Rate Limiting**: Be aware of API rate limits
- **Validation**: The bot does basic input validation but doesn't check if items exceed bin capacity
- **Concurrency**: The bot processes one request at a time per user
- **Response Time**: Typical response time is 2-10 seconds depending on LLM load

## 🔐 Security Considerations

- ✅ Keep your `BOT_TOKEN` and `API_KEY` secret
- ✅ Don't commit credentials to version control
- ✅ Use environment variables for production deployment
- ✅ Implement rate limiting for production use
- ✅ Add user authentication if needed

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if `BOT_TOKEN` is correct
- Verify the bot is running (`python bot.py`)
- Check internet connection

### "Error in model request"
- Verify `API_KEY` is valid
- Check API quota/credits
- Ensure LLM service is available

### Incorrect solutions
- Try increasing `n_examples` in few-shot prompt
- Verify `examples.json` is properly formatted
- Consider using a different model

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment before running

## 🚀 Future Enhancements

- [ ] Support for multiple bin capacities
- [ ] Add visualization showing actual bins with items
- [ ] Implement caching for common problem instances
- [ ] Add comparison with classical algorithms (First Fit, Best Fit)
- [ ] Support for weight + volume constraints
- [ ] Export solutions to PDF/CSV
- [ ] Multi-language support
- [ ] Web interface

## 📝 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Made with ❤️ using AI and combinatorial optimization**

