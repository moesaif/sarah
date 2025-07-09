# Sarah AI Agent - Natural Language Interface

Transform Sarah from a command-line tool into an intelligent AI assistant that understands natural language! 🤖

## Overview

The Sarah AI Agent adds powerful natural language processing capabilities to the existing Sarah terminal assistant. Instead of remembering specific commands, you can now talk to Sarah naturally, and she'll understand what you want to do.

## Features

### 🧠 Natural Language Understanding

- **Intent Recognition**: Understands what you want to do from natural language
- **Entity Extraction**: Automatically extracts relevant information (names, locations, etc.)
- **Semantic Similarity**: Uses advanced ML models for accurate intent matching
- **Fallback Support**: Works even without ML models using keyword matching

### 💬 Conversational AI

- **Context Awareness**: Remembers previous conversations
- **Follow-up Handling**: Understands follow-up questions
- **User Preferences**: Learns from your usage patterns
- **Session Management**: Maintains conversation state

### 🎯 Smart Plugin Execution

- **Automatic Mapping**: Maps natural language to existing Sarah plugins
- **Parameter Extraction**: Automatically prepares plugin arguments
- **Error Handling**: Graceful degradation when things go wrong
- **Suggestion System**: Helps when intent is unclear

### 🔧 Advanced Features

- **Multiple AI Models**: Supports various NLP backends
- **Configuration**: Highly customizable behavior
- **Voice Support**: Optional speech recognition and synthesis
- **Learning**: Adapts to user patterns over time

## Installation

### 1. Install Sarah with AI Dependencies

The AI agent is included in the Sarah Docker image. Build with AI support:

```bash
# Build Sarah with AI capabilities
docker build -t sarah:ai .

# Or use docker-compose
docker-compose up --build
```

### 2. Install Language Models (Optional)

For enhanced understanding, install spaCy language models:

```bash
# Inside container or on host
python -m spacy download en_core_web_sm
```

### 3. Configuration

Create your AI configuration:

```bash
# Copy default config
cp plugins/ai_agent/config.json ~/.sarah/ai_config.json

# Edit settings as needed
nano ~/.sarah/ai_config.json
```

## Usage

### Basic Natural Language Commands

Instead of memorizing specific syntax, just talk naturally:

```bash
# Traditional Sarah command:
sarah weather New York

# AI Agent - Natural Language:
sarah ai_agent "What's the weather like in New York?"
sarah ai_agent "Is it going to rain today?"
sarah ai_agent "Show me the forecast for London"
```

### Example Conversations

```bash
# Web Search
sarah ai_agent "Search for Python tutorials"
sarah ai_agent "Find information about machine learning"
sarah ai_agent "Look up best restaurants in Paris"

# Information Queries
sarah ai_agent "Tell me about Albert Einstein"
sarah ai_agent "Who is Elon Musk?"
sarah ai_agent "What is quantum computing?"

# Utilities
sarah ai_agent "What time is it?"
sarah ai_agent "Test my internet speed"
sarah ai_agent "Check Apple stock price"

# Entertainment
sarah ai_agent "Find funny cat videos"
sarah ai_agent "Tell me about the movie Inception"
sarah ai_agent "Search for jazz music on YouTube"
```

### Interactive Mode

Run in interactive mode for ongoing conversations:

```bash
# Start interactive session
python plugins/ai_agent/ai_agent.py

# Or through Docker
docker run -it sarah:ai python plugins/ai_agent/ai_agent.py
```

### Help and Status

```bash
# Get help
sarah ai_agent help

# Check AI system status
sarah ai_agent status

# View configuration
sarah ai_agent config show
```

## Architecture

### Core Components

```
Sarah AI Agent
├── ai_core.py              # NLP and intent recognition
├── conversation_manager.py # Context and conversation flow
├── ai_agent.py            # Main plugin integration
└── config.json           # Configuration settings
```

### How It Works

1. **Input Processing**: User speaks naturally to Sarah
2. **Intent Recognition**: AI analyzes input to determine what the user wants
3. **Entity Extraction**: Extracts relevant parameters (locations, names, etc.)
4. **Plugin Mapping**: Maps intent to appropriate Sarah plugin
5. **Execution**: Runs the plugin with extracted parameters
6. **Response**: Provides contextual, conversational response
7. **Learning**: Updates conversation context and user preferences

### AI Models Used

- **spaCy**: Named entity recognition and linguistic analysis
- **Sentence Transformers**: Semantic similarity for intent matching
- **Scikit-learn**: Machine learning utilities
- **Optional OpenAI**: Enhanced language understanding (configurable)

## Configuration

### AI Core Settings

```json
{
  "ai_core": {
    "spacy_model": "en_core_web_sm",
    "sentence_model": "all-MiniLM-L6-v2",
    "confidence_threshold": 0.6,
    "max_suggestions": 3
  }
}
```

### Conversation Settings

```json
{
  "conversation": {
    "enable_conversation": true,
    "max_context_turns": 10,
    "session_timeout_minutes": 30,
    "save_history": true
  }
}
```

### Advanced Features

```json
{
  "advanced": {
    "cache_embeddings": true,
    "enable_voice": false,
    "model_cache_dir": "~/.sarah/models"
  }
}
```

## Supported Natural Language Patterns

### Weather Queries

- "What's the weather like?"
- "Is it going to rain in London?"
- "Weather forecast for Tokyo"
- "How's the weather today?"

### Search Requests

- "Search for Python programming"
- "Find videos about cooking"
- "Look up information about cars"
- "Google search for news"

### Information Queries

- "Tell me about Einstein"
- "Who is Steve Jobs?"
- "What is machine learning?"
- "Information about Paris"

### Time and Utilities

- "What time is it?"
- "Current date and time"
- "Test internet speed"
- "Check connection speed"

### Entertainment

- "Find funny videos"
- "Movie information for Titanic"
- "Search for jazz music"
- "Show me cooking tutorials"

## Extending the AI Agent

### Adding New Intent Patterns

Edit `ai_core.py` to add new plugin definitions:

```python
"new_plugin": PluginInfo(
    name="new_plugin",
    description="Description of what this plugin does",
    examples=[
        "example user input 1",
        "example user input 2"
    ],
    keywords=["keyword1", "keyword2"],
    parameters=["param1", "param2"]
)
```

### Custom Conversation Patterns

Modify `conversation_manager.py` to add new response patterns:

```python
self.custom_responses = [
    "Your custom response pattern",
    "Another response option"
]
```

### Integration with External APIs

The AI agent can be extended to work with external APIs:

```python
# In ai_agent.py
def _call_external_api(self, intent):
    # Custom API integration
    pass
```

## Troubleshooting

### Common Issues

1. **AI Models Not Loading**

   ```bash
   # Install missing models
   python -m spacy download en_core_web_sm
   pip install sentence-transformers
   ```

2. **Low Confidence Responses**

   - Adjust `confidence_threshold` in config
   - Add more training examples
   - Use more specific language

3. **Memory Issues**
   - Reduce `max_context_turns`
   - Disable `cache_embeddings`
   - Use smaller models

### Debug Mode

Enable debug logging:

```json
{
  "advanced": {
    "log_level": "DEBUG"
  }
}
```

### Performance Optimization

- Use GPU acceleration for transformers
- Cache embeddings for faster startup
- Limit conversation context length
- Use smaller/faster models for resource-constrained environments

## Examples

### Simple Weather Query

```
User: "What's the weather like in New York?"
Sarah: 🧠 I understand you want: weather (confidence: 0.89)
       🔧 Executing: sarah weather New York
       📋 Result: [Weather information for New York]
```

### Follow-up Conversation

```
User: "What's the weather like?"
Sarah: [Weather for current location]

User: "How about in London?"
Sarah: 💬 Got it! Here's more information:
       🔧 Executing: sarah weather London
       📋 Result: [Weather information for London]
```

### Unclear Intent

```
User: "I want to know stuff"
Sarah: ❓ I'm not quite sure what you mean by 'I want to know stuff'.
       💡 Did you mean:
         1. Search Wikipedia for information 🟡
         2. Search Google for information 🟡
         3. Get current time and date 🔴
```

## Contributing

Want to improve Sarah's AI capabilities? Here are ways to contribute:

1. **Add Training Data**: Expand the examples in plugin definitions
2. **Improve NLP**: Enhance entity extraction and intent recognition
3. **New Features**: Add voice support, sentiment analysis, etc.
4. **Bug Fixes**: Report and fix issues
5. **Documentation**: Improve guides and examples

## Future Enhancements

### Planned Features

- 🎤 **Voice Interface**: Speech-to-text and text-to-speech
- 🧠 **Advanced Learning**: User-specific model fine-tuning
- 🌐 **Multi-language**: Support for multiple languages
- 🔗 **API Integration**: Direct integration with popular APIs
- 📱 **GUI Interface**: Graphical conversation interface
- 🤝 **Multi-agent**: Coordination between multiple AI agents

### Experimental Features

- **GPT Integration**: Use OpenAI GPT models for enhanced understanding
- **Memory Networks**: Long-term memory across sessions
- **Emotional Intelligence**: Sentiment-aware responses
- **Proactive Assistance**: Sarah suggests actions before being asked

## License

This AI agent extension follows the same license as the main Sarah project.

---

_Sarah AI Agent - Making terminal assistance more human! 🤖💙_
