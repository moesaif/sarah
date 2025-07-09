#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversation Manager for Sarah AI Agent

This module manages conversation context, remembers previous interactions,
and provides contextual responses.
"""

import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """Represents a single turn in conversation"""
    timestamp: datetime
    user_input: str
    intent_plugin: str
    intent_confidence: float
    entities: Dict[str, Any]
    sarah_response: str
    execution_successful: bool


@dataclass
class ConversationContext:
    """Maintains conversation context and state"""
    session_id: str
    started_at: datetime
    last_interaction: datetime
    turns: List[ConversationTurn]
    active_topic: Optional[str] = None
    user_preferences: Dict[str, Any] = None
    location_context: Optional[str] = None
    

class ConversationManager:
    """
    Manages conversation flow, context, and provides intelligent responses
    """
    
    def __init__(self, max_context_turns: int = 10, session_timeout_minutes: int = 30):
        self.max_context_turns = max_context_turns
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self.current_context: Optional[ConversationContext] = None
        self.conversation_history: Dict[str, ConversationContext] = {}
        
        # Conversation patterns for more natural responses
        self.greeting_responses = [
            "Hello! I'm Sarah, your AI assistant. How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! Ready to help you with anything you need.",
            "Good to see you! What would you like me to help with?"
        ]
        
        self.farewell_responses = [
            "Goodbye! Feel free to ask me anything anytime.",
            "See you later! I'm always here when you need help.",
            "Take care! Don't hesitate to come back if you need anything.",
            "Bye! Looking forward to helping you again soon."
        ]
        
        self.confusion_responses = [
            "I'm not quite sure what you mean. Could you rephrase that?",
            "Could you be more specific? I want to make sure I help you correctly.",
            "I didn't quite catch that. Can you try asking in a different way?",
            "Let me try to understand better. What exactly are you looking for?"
        ]
        
        self.acknowledgment_responses = [
            "Got it!",
            "Understood!",
            "Perfect!",
            "Sure thing!",
            "Absolutely!",
            "No problem!"
        ]
    
    def start_conversation(self, session_id: str = None) -> str:
        """Start a new conversation session"""
        if session_id is None:
            session_id = f"session_{int(time.time())}"
        
        now = datetime.now()
        self.current_context = ConversationContext(
            session_id=session_id,
            started_at=now,
            last_interaction=now,
            turns=[],
            user_preferences={}
        )
        
        # Store in history
        self.conversation_history[session_id] = self.current_context
        
        # Clean up old sessions
        self._cleanup_old_sessions()
        
        return self._get_greeting_response()
    
    def add_turn(self, user_input: str, intent_plugin: str, intent_confidence: float, 
                 entities: Dict[str, Any], sarah_response: str, 
                 execution_successful: bool = True) -> None:
        """Add a conversation turn to the current context"""
        
        if not self.current_context:
            self.start_conversation()
        
        turn = ConversationTurn(
            timestamp=datetime.now(),
            user_input=user_input,
            intent_plugin=intent_plugin,
            intent_confidence=intent_confidence,
            entities=entities,
            sarah_response=sarah_response,
            execution_successful=execution_successful
        )
        
        self.current_context.turns.append(turn)
        self.current_context.last_interaction = turn.timestamp
        
        # Update active topic based on intent
        self._update_active_topic(intent_plugin, entities)
        
        # Keep only recent turns to manage memory
        if len(self.current_context.turns) > self.max_context_turns:
            self.current_context.turns = self.current_context.turns[-self.max_context_turns:]
        
        # Extract and update user preferences
        self._update_user_preferences(entities, intent_plugin)
    
    def get_contextual_response(self, user_input: str, intent_plugin: str, 
                              entities: Dict[str, Any], base_response: str) -> str:
        """Generate a contextual response based on conversation history"""
        
        if not self.current_context:
            return base_response
        
        # Check for conversation patterns
        if self._is_greeting(user_input):
            return self._get_contextual_greeting()
        
        if self._is_farewell(user_input):
            return self._get_farewell_response()
        
        if self._is_follow_up_question(user_input, intent_plugin):
            return self._handle_follow_up(base_response)
        
        # Add contextual information
        contextual_response = self._add_context_to_response(base_response, intent_plugin, entities)
        
        return contextual_response
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation"""
        if not self.current_context:
            return {"status": "no_active_conversation"}
        
        recent_plugins = []
        recent_topics = []
        
        for turn in self.current_context.turns[-5:]:  # Last 5 turns
            if turn.intent_plugin not in recent_plugins:
                recent_plugins.append(turn.intent_plugin)
            
            if 'search_terms' in turn.entities:
                recent_topics.extend(turn.entities['search_terms'])
        
        return {
            "session_id": self.current_context.session_id,
            "duration": str(datetime.now() - self.current_context.started_at),
            "total_turns": len(self.current_context.turns),
            "active_topic": self.current_context.active_topic,
            "recent_plugins": recent_plugins,
            "recent_topics": list(set(recent_topics)),
            "user_preferences": self.current_context.user_preferences
        }
    
    def _update_active_topic(self, intent_plugin: str, entities: Dict[str, Any]) -> None:
        """Update the active conversation topic"""
        if 'search_terms' in entities and entities['search_terms']:
            # Use the most recent search terms as active topic
            self.current_context.active_topic = ' '.join(entities['search_terms'][:3])
        elif intent_plugin in ['weather', 'time', 'speedtest']:
            self.current_context.active_topic = intent_plugin
    
    def _update_user_preferences(self, entities: Dict[str, Any], intent_plugin: str) -> None:
        """Learn and update user preferences from conversation"""
        if not self.current_context.user_preferences:
            self.current_context.user_preferences = {}
        
        # Track preferred plugins
        if 'preferred_plugins' not in self.current_context.user_preferences:
            self.current_context.user_preferences['preferred_plugins'] = {}
        
        plugin_prefs = self.current_context.user_preferences['preferred_plugins']
        plugin_prefs[intent_plugin] = plugin_prefs.get(intent_plugin, 0) + 1
        
        # Track location preferences
        if 'gpe' in entities or 'loc' in entities:
            location = entities.get('gpe') or entities.get('loc')
            self.current_context.location_context = location
            self.current_context.user_preferences['preferred_location'] = location
    
    def _is_greeting(self, user_input: str) -> bool:
        """Check if user input is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 
                    'good evening', 'greetings', 'howdy']
        return any(greeting in user_input.lower() for greeting in greetings)
    
    def _is_farewell(self, user_input: str) -> bool:
        """Check if user input is a farewell"""
        farewells = ['goodbye', 'bye', 'see you', 'farewell', 'exit', 'quit', 
                    'thanks', 'thank you', 'that\'s all']
        return any(farewell in user_input.lower() for farewell in farewells)
    
    def _is_follow_up_question(self, user_input: str, intent_plugin: str) -> bool:
        """Check if this is a follow-up question"""
        if not self.current_context or not self.current_context.turns:
            return False
        
        last_turn = self.current_context.turns[-1]
        
        # Check if it's the same plugin as last turn (within 2 minutes)
        time_diff = datetime.now() - last_turn.timestamp
        if time_diff < timedelta(minutes=2) and intent_plugin == last_turn.intent_plugin:
            return True
        
        # Check for follow-up indicators
        follow_up_words = ['also', 'and', 'what about', 'how about', 'more', 'another']
        return any(word in user_input.lower() for word in follow_up_words)
    
    def _get_greeting_response(self) -> str:
        """Get an appropriate greeting response"""
        import random
        return random.choice(self.greeting_responses)
    
    def _get_contextual_greeting(self) -> str:
        """Get a contextual greeting based on conversation history"""
        if self.current_context and self.current_context.turns:
            return "Welcome back! What else can I help you with?"
        return self._get_greeting_response()
    
    def _get_farewell_response(self) -> str:
        """Get an appropriate farewell response"""
        import random
        base_farewell = random.choice(self.farewell_responses)
        
        if self.current_context and len(self.current_context.turns) > 0:
            base_farewell += " It was great helping you today!"
        
        return base_farewell
    
    def _handle_follow_up(self, base_response: str) -> str:
        """Handle follow-up questions with context"""
        import random
        acknowledgment = random.choice(self.acknowledgment_responses)
        return f"{acknowledgment} Here's more information:\n{base_response}"
    
    def _add_context_to_response(self, base_response: str, intent_plugin: str, 
                                entities: Dict[str, Any]) -> str:
        """Add contextual information to the response"""
        
        # Add location context for weather and location-based queries
        if intent_plugin == 'weather' and self.current_context.location_context:
            if not any(loc in base_response.lower() for loc in [
                self.current_context.location_context.lower()
            ]):
                location_hint = f"\n(I remember you usually ask about {self.current_context.location_context})"
                base_response += location_hint
        
        # Add topic continuity
        if (self.current_context.active_topic and 
            intent_plugin in ['wiki', 'google', 'youtube', 'github']):
            if self.current_context.active_topic.lower() not in base_response.lower():
                topic_hint = f"\n(Related to our discussion about {self.current_context.active_topic})"
                base_response += topic_hint
        
        return base_response
    
    def _cleanup_old_sessions(self) -> None:
        """Remove old conversation sessions to manage memory"""
        cutoff_time = datetime.now() - self.session_timeout
        
        sessions_to_remove = []
        for session_id, context in self.conversation_history.items():
            if context.last_interaction < cutoff_time:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.conversation_history[session_id]
        
        if sessions_to_remove:
            logger.info(f"Cleaned up {len(sessions_to_remove)} old conversation sessions")
    
    def save_conversation_history(self, filepath: str) -> None:
        """Save conversation history to file"""
        try:
            # Convert conversation history to serializable format
            history_data = {}
            for session_id, context in self.conversation_history.items():
                turns_data = []
                for turn in context.turns:
                    turn_dict = asdict(turn)
                    turn_dict['timestamp'] = turn.timestamp.isoformat()
                    turns_data.append(turn_dict)
                
                context_dict = asdict(context)
                context_dict['started_at'] = context.started_at.isoformat()
                context_dict['last_interaction'] = context.last_interaction.isoformat()
                context_dict['turns'] = turns_data
                
                history_data[session_id] = context_dict
            
            with open(filepath, 'w') as f:
                json.dump(history_data, f, indent=2)
            
            logger.info(f"Saved conversation history to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save conversation history: {e}")
    
    def load_conversation_history(self, filepath: str) -> None:
        """Load conversation history from file"""
        try:
            with open(filepath, 'r') as f:
                history_data = json.load(f)
            
            self.conversation_history = {}
            for session_id, context_dict in history_data.items():
                # Reconstruct turns
                turns = []
                for turn_dict in context_dict['turns']:
                    turn_dict['timestamp'] = datetime.fromisoformat(turn_dict['timestamp'])
                    turns.append(ConversationTurn(**turn_dict))
                
                # Reconstruct context
                context_dict['started_at'] = datetime.fromisoformat(context_dict['started_at'])
                context_dict['last_interaction'] = datetime.fromisoformat(context_dict['last_interaction'])
                context_dict['turns'] = turns
                
                self.conversation_history[session_id] = ConversationContext(**context_dict)
            
            logger.info(f"Loaded conversation history from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load conversation history: {e}")


def create_conversation_manager(max_context_turns: int = 10, 
                              session_timeout_minutes: int = 30) -> ConversationManager:
    """Factory function to create conversation manager"""
    return ConversationManager(max_context_turns, session_timeout_minutes)


if __name__ == "__main__":
    # Test the conversation manager
    conv_mgr = create_conversation_manager()
    
    # Start conversation
    greeting = conv_mgr.start_conversation()
    print(f"Sarah: {greeting}")
    
    # Simulate conversation turns
    test_conversations = [
        ("Hello Sarah", "hi", 0.95, {"search_terms": ["hello"]}, "Hello! How can I help you?"),
        ("What's the weather like?", "weather", 0.88, {"search_terms": ["weather"]}, "Here's the weather..."),
        ("How about in New York?", "weather", 0.85, {"gpe": "New York"}, "Weather in New York..."),
        ("Thanks, that's all", "hi", 0.70, {"search_terms": ["thanks"]}, "You're welcome!")
    ]
    
    for user_input, plugin, confidence, entities, response in test_conversations:
        conv_mgr.add_turn(user_input, plugin, confidence, entities, response)
        contextual_response = conv_mgr.get_contextual_response(
            user_input, plugin, entities, response
        )
        print(f"User: {user_input}")
        print(f"Sarah: {contextual_response}")
        print("-" * 40)
    
    # Show conversation summary
    summary = conv_mgr.get_conversation_summary()
    print("Conversation Summary:", json.dumps(summary, indent=2)) 