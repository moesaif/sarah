#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Agent Plugin for Sarah - Unicode Safe Version

This plugin provides natural language understanding capabilities to Sarah,
with robust Unicode handling for different environments.
"""

import os
import sys
import logging
import traceback
import subprocess
from typing import Dict, List, Any, Optional

import gi
gi.require_version('Peas', '1.0')
gi.require_version('Sarah', '1.0')
from gi.repository import GObject, Peas, Sarah

# Import our AI modules
try:
    from .ai_core import create_ai_core, Intent
    from .conversation_manager import create_conversation_manager
except ImportError:
    # Fallback for direct execution
    from ai_core import create_ai_core, Intent
    from conversation_manager import create_conversation_manager

logger = logging.getLogger(__name__)


def safe_print(message: str):
    """Safely print messages with Unicode fallback for encoding issues"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version without emojis
        ascii_message = message.encode('ascii', 'ignore').decode('ascii').strip()
        if ascii_message:
            print(ascii_message)
        else:
            print("[Unicode content - display not supported]")


class AIAgentPlugin(GObject.Object, Sarah.IExtension):
    """
    AI Agent plugin that provides natural language understanding for Sarah
    """
    __gtype_name__ = 'AIAgentPlugin'

    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super().__init__()
        self.ai_core = None
        self.conversation_manager = None
        self.initialized = False
        
        # Try to initialize AI components
        self._initialize_ai()

    def _initialize_ai(self):
        """Initialize AI components with error handling"""
        try:
            # Create AI core
            config_path = self._get_config_path()
            self.ai_core = create_ai_core(config_path)
            
            # Create conversation manager
            self.conversation_manager = create_conversation_manager()
            
            # Start conversation session
            if self.conversation_manager:
                greeting = self.conversation_manager.start_conversation()
                safe_print(f"\n[AI] {greeting}")
                safe_print("[INFO] You can now talk to me in natural language!")
                safe_print("[INFO] Try: 'What's the weather like?' or 'Search for Python tutorials'")
                safe_print("[INFO] Type 'sarah ai_agent help' to see available capabilities.\n")
            
            self.initialized = True
            logger.info("AI Agent initialized successfully")
            
        except Exception as e:
            logger.warning(f"AI initialization failed: {e}")
            safe_print(f"[WARNING] AI features limited due to: {e}")
            safe_print("[INFO] Basic keyword matching will be used instead.")
            self.initialized = False

    def _get_config_path(self) -> Optional[str]:
        """Get path to AI configuration file"""
        config_locations = [
            os.path.join(os.path.dirname(__file__), 'config.json'),
            os.path.expanduser('~/.sarah/ai_config.json'),
            '/etc/sarah/ai_config.json'
        ]
        
        for path in config_locations:
            if os.path.exists(path):
                return path
        return None

    def do_activate(self, args, argv):
        """Main activation method called by Sarah's plugin system"""
        try:
            if not args:
                self._show_help()
                return
            
            # Join all arguments as natural language input
            user_input = ' '.join(args)
            
            # Special commands
            if user_input.lower() in ['help', '--help', '-h']:
                self._show_help()
                return
            elif user_input.lower() in ['status', '--status']:
                self._show_status()
                return
            
            # Process natural language input
            self._process_natural_language(user_input)
            
        except Exception as e:
            error_msg = f"AI Agent error: {e}"
            logger.error(error_msg)
            safe_print(f"[ERROR] {error_msg}")
            if logger.isEnabledFor(logging.DEBUG):
                traceback.print_exc()

    def _process_natural_language(self, user_input: str):
        """Process natural language input and execute appropriate action"""
        
        if not self.initialized or not self.ai_core:
            # Fallback to simple keyword matching
            self._fallback_processing(user_input)
            return
        
        try:
            # Understand the intent
            intent = self.ai_core.understand_input(user_input)
            
            safe_print(f"[AI] I understand you want: {intent.plugin_name} (confidence: {intent.confidence:.2f})")
            
            if intent.confidence < 0.3:
                # Very low confidence - ask for clarification
                suggestions = self.ai_core.get_suggestions(user_input, 3)
                self._show_suggestions(user_input, suggestions)
                return
            
            # Execute the intended plugin
            success = self._execute_plugin(intent)
            
            # Add to conversation history
            if self.conversation_manager:
                plugin_response = "Command executed successfully" if success else "Command failed"
                self.conversation_manager.add_turn(
                    user_input, intent.plugin_name, intent.confidence,
                    intent.entities, plugin_response, success
                )
            
        except Exception as e:
            logger.error(f"Error processing natural language: {e}")
            safe_print(f"[ERROR] Sorry, I encountered an error: {e}")

    def _execute_plugin(self, intent: Intent) -> bool:
        """Execute the appropriate Sarah plugin based on intent"""
        try:
            # Prepare arguments for the plugin
            plugin_args = self._prepare_plugin_args(intent)
            
            # Build sarah command
            sarah_cmd = ['sarah', intent.plugin_name] + plugin_args
            
            safe_print(f"[EXEC] Executing: {' '.join(sarah_cmd)}")
            
            # Execute the plugin
            result = subprocess.run(
                sarah_cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            if result.stdout:
                safe_print("[RESULT]")
                safe_print(result.stdout)
            
            if result.stderr and result.returncode != 0:
                safe_print(f"[WARNING] Error: {result.stderr}")
                return False
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            safe_print("[ERROR] Command timed out")
            return False
        except Exception as e:
            safe_print(f"[ERROR] Failed to execute plugin: {e}")
            return False

    def _prepare_plugin_args(self, intent: Intent) -> List[str]:
        """Prepare arguments for the plugin based on extracted entities"""
        args = []
        
        # Extract search terms or relevant entities
        if 'search_terms' in intent.entities:
            args.extend(intent.entities['search_terms'])
        
        # Add location for location-based plugins
        if intent.plugin_name in ['weather', 'adhan']:
            if 'gpe' in intent.entities:
                args.append(intent.entities['gpe'])
            elif 'loc' in intent.entities:
                args.append(intent.entities['loc'])
        
        # Add person name for whois queries
        if intent.plugin_name == 'whois' and 'person' in intent.entities:
            args.append(intent.entities['person'])
        
        # If no specific args found, use search terms from original input
        if not args and 'search_terms' in intent.entities:
            args = intent.entities['search_terms']
        
        return args

    def _fallback_processing(self, user_input: str):
        """Fallback processing when AI is not available"""
        safe_print("[INFO] Using basic keyword matching...")
        
        # Simple keyword to plugin mapping
        keyword_mapping = {
            'weather': ['weather', 'temperature', 'rain', 'snow', 'forecast'],
            'time': ['time', 'date', 'clock'],
            'wiki': ['wiki', 'wikipedia', 'about', 'information'],
            'google': ['google', 'search', 'find'],
            'youtube': ['youtube', 'video', 'music'],
            'github': ['github', 'code', 'repository'],
            'speedtest': ['speed', 'internet', 'connection'],
            'hi': ['hello', 'hi', 'hey', 'greetings']
        }
        
        user_lower = user_input.lower()
        best_match = None
        max_matches = 0
        
        for plugin, keywords in keyword_mapping.items():
            matches = sum(1 for keyword in keywords if keyword in user_lower)
            if matches > max_matches:
                max_matches = matches
                best_match = plugin
        
        if best_match and max_matches > 0:
            # Extract potential arguments
            words = user_input.split()
            args = [word for word in words if len(word) > 2][:5]  # Limit to 5 words
            
            safe_print(f"[MATCH] Best match: {best_match}")
            
            # Execute the plugin
            try:
                sarah_cmd = ['sarah', best_match] + args
                result = subprocess.run(sarah_cmd, capture_output=True, text=True, timeout=30)
                
                if result.stdout:
                    safe_print("[RESULT]")
                    safe_print(result.stdout)
                if result.stderr and result.returncode != 0:
                    safe_print(f"[WARNING] Error: {result.stderr}")
                    
            except Exception as e:
                safe_print(f"[ERROR] Error executing {best_match}: {e}")
        else:
            safe_print("[INFO] I couldn't understand what you want to do.")
            safe_print("[INFO] Try being more specific or use 'sarah ai_agent help' for available commands.")

    def _show_suggestions(self, user_input: str, suggestions: List[Dict]):
        """Show suggestions when intent is unclear"""
        safe_print(f"[INFO] I'm not quite sure what you mean by '{user_input}'.")
        safe_print("[INFO] Did you mean:")
        
        for i, suggestion in enumerate(suggestions, 1):
            confidence_indicator = "HIGH" if suggestion['confidence'] > 0.7 else "MED" if suggestion['confidence'] > 0.4 else "LOW"
            safe_print(f"  {i}. {suggestion['description']} ({confidence_indicator})")
        
        safe_print("\n[INFO] Try rephrasing your request or be more specific.")

    def _show_help(self):
        """Show help information"""
        safe_print("""
[AI AGENT] Sarah AI Agent - Natural Language Interface

USAGE:
  sarah ai_agent <natural language input>

EXAMPLES:
  sarah ai_agent "What's the weather like in New York?"
  sarah ai_agent "Search for Python tutorials on YouTube"
  sarah ai_agent "Tell me about Albert Einstein"
  sarah ai_agent "What time is it?"
  sarah ai_agent "Test my internet speed"
  sarah ai_agent "Show me stock price for Apple"

FEATURES:
  - Natural language understanding
  - Conversational context
  - Smart intent recognition
  - Automatic plugin execution
  - Learning from interactions

COMMANDS:
  help     - Show this help message
  status   - Show AI system status

AVAILABLE PLUGINS:
""")
        
        # Show available plugins
        plugins_info = {
            'weather': 'Get weather information',
            'time': 'Show current time and date',
            'wiki': 'Search Wikipedia',
            'google': 'Search Google',
            'youtube': 'Search YouTube',
            'github': 'Search GitHub',
            'whois': 'Get information about people/domains',
            'watch': 'Get movie/TV show information',
            'speedtest': 'Test internet speed',
            'adhan': 'Get prayer times',
            'marketwatch': 'Get stock market data',
            'hi': 'Greeting and conversation'
        }
        
        for plugin, description in plugins_info.items():
            safe_print(f"  • {plugin:<12} - {description}")
        
        safe_print("\n[INFO] Just talk to me naturally! I'll figure out what you want to do.")

    def _show_status(self):
        """Show AI system status"""
        safe_print("[AI AGENT] Sarah AI Agent Status:")
        safe_print(f"  • AI Core: {'ACTIVE' if self.initialized and self.ai_core else 'INACTIVE'}")
        safe_print(f"  • Conversation: {'ACTIVE' if self.conversation_manager else 'INACTIVE'}")
        
        if self.ai_core:
            try:
                # Test AI components
                safe_print(f"  • NLP Model: {'LOADED' if self.ai_core.nlp else 'BASIC_MODE'}")
                safe_print(f"  • Embeddings: {'READY' if self.ai_core.sentence_model else 'UNAVAILABLE'}")
            except:
                safe_print("  • Models: ERROR_CHECKING_STATUS")
        
        if self.conversation_manager:
            summary = self.conversation_manager.get_conversation_summary()
            if summary.get('status') != 'no_active_conversation':
                safe_print(f"  • Session: {summary.get('session_id', 'Unknown')}")
                safe_print(f"  • Duration: {summary.get('duration', 'Unknown')}")
                safe_print(f"  • Turns: {summary.get('total_turns', 0)}")

    def do_deactivate(self):
        """Cleanup when plugin is deactivated"""
        if self.conversation_manager:
            try:
                # Save conversation history
                history_path = os.path.expanduser('~/.sarah/conversation_history.json')
                os.makedirs(os.path.dirname(history_path), exist_ok=True)
                self.conversation_manager.save_conversation_history(history_path)
                logger.info("Conversation history saved")
            except Exception as e:
                logger.warning(f"Failed to save conversation history: {e}")


def main():
    """Main function for testing the AI agent directly"""
    import sys
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Create AI agent
    agent = AIAgentPlugin()
    
    if len(sys.argv) > 1:
        # Process command line arguments
        args = sys.argv[1:]
        agent.do_activate(args, len(args))
    else:
        # Interactive mode
        safe_print("[AI AGENT] Sarah AI Agent - Interactive Mode")
        safe_print("Type 'quit' to exit, 'help' for help")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    safe_print("Goodbye!")
                    break
                
                if user_input:
                    args = user_input.split()
                    agent.do_activate(args, len(args))
                    
            except KeyboardInterrupt:
                safe_print("\nGoodbye!")
                break
            except Exception as e:
                safe_print(f"[ERROR] Error: {e}")


if __name__ == "__main__":
    main() 