# LLM Foundations

A collection of Python projects demonstrating foundational concepts and patterns for building LLM-powered applications using the OpenAI API.

## 📁 Projects

### 1. Basic LLM Agent
An intelligent agent that can make tool calls to execute functions and answer user queries.

**Features:**
- Multi-turn conversation support
- Dynamic tool calling with function execution
- Integration with Open-Meteo weather API
- Built-in tools:
  - `get_time`: Get current time for a city
  - `calculate`: Evaluate mathematical expressions
  - `check_weather`: Check current weather for coordinates (latitude/longitude)

**Usage:**
```bash
cd basic-llm-agent
python main.py
```

**Example Interaction:**
```
You: Hey, what's the weather in Delhi today?
[INFO] Tool call: check_weather with args {'latitude': 28.6139, 'longitude': 77.209}
AI: The weather in Delhi today is around 28.2°C with a wind speed of 3.7 m/s.
```

### 2. CLI Streaming Assistant
A real-time streaming chatbot that streams responses token-by-token for a more interactive experience.

**Features:**
- Real-time token streaming
- Multi-turn conversation history
- Immediate token output as response is generated

**Usage:**
```bash
cd cli-streaming-assistant
python main.py
```

**Example:**
```
You: Tell me a short poem about programming
AI: [Response streams in real-time, one token at a time]
```

### 3. Structured JSON Generator
Converts unstructured text into structured JSON data using LLMs with predefined schemas.

**Features:**
- Schema-based extraction from text
- Automatic retry logic for parsing failures
- Temperature-controlled deterministic output

**Usage:**
```bash
cd structured-json-generator
python main.py
```

**Example:**
```
Enter text: John Doe is a software engineer with 5 years of experience in Python and JavaScript

✅ Parsed JSON:
{
  "name": "John Doe",
  "skills": ["Python", "JavaScript"],
  "experience": "5 years"
}
```

## 🚀 Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- Python virtual environment (recommended)

### Installation

1. **Clone/Navigate to the repository:**
```bash
cd "LLM Foundations"
```

2. **Create and activate virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4
```

## 📦 Dependencies

- `openai==2.32.0` - OpenAI API client
- `python-dotenv==1.2.2` - Environment variable management
- `requests==2.33.1` - HTTP library for API calls
- `openmeteo_requests==1.7.5` - Weather API requests

## 🏗️ Architecture

### Common Patterns

1. **Agent Loop**: Continuous message exchange with tool calling capability
2. **Streaming**: Token-by-token response generation for better UX
3. **Structured Extraction**: LLM-powered data parsing with error handling

### Message Flow

```
User Input
   ↓
LLM Processing
   ↓
Tool Call Detection?
   ├─ YES → Execute Tool → Get Result → Add to Context → Re-prompt LLM
   └─ NO  → Return Final Response
   ↓
Output to User
```

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `MODEL` | Model to use for API calls | `gpt-4` or `gpt-4-turbo` |

## 📚 Learning Concepts

This repository demonstrates:

- **Agent Design Pattern**: Building autonomous systems that can use tools
- **API Integration**: Working with OpenAI's latest response API
- **Streaming**: Real-time response generation
- **Structured Output**: Using LLMs for data extraction and formatting
- **Tool Calling**: Dynamic function invocation based on LLM decisions
- **Error Handling**: Robust parsing and retry logic

## 🤝 Common Issues & Solutions

### Issue: `OPENAI_API_KEY` not found
**Solution:** Ensure `.env` file exists in the root directory with your API key

### Issue: Tool call not recognized
**Solution:** Check that the model supports function calling (GPT-4 or newer)

### Issue: Weather API errors
**Solution:** Check internet connection and Open-Meteo API availability

## 📖 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Open-Meteo Weather API](https://open-meteo.com/)
- [Python-dotenv Guide](https://pypi.org/project/python-dotenv/)

## 🎯 Future Enhancements

- [ ] Add more tool categories (web search, database queries, etc.)
- [ ] Implement memory/context management for longer conversations
- [ ] Add cost tracking for API calls
- [ ] Create web UI for the streaming assistant
- [ ] Add support for different LLM providers
- [ ] Implement caching for repeated queries

## 📝 License

This project is provided as-is for educational purposes.

---

**Last Updated:** April 2026
