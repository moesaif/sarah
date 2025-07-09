#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Core Module for Sarah - Natural Language Understanding

This module provides the core AI capabilities for understanding natural language
and mapping it to appropriate actions and plugins.
"""

import re
import json
import os
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

# NLP libraries
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configuration
from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Intent:
    """Represents a recognized intent with confidence score"""
    plugin_name: str
    confidence: float
    entities: Dict[str, Any]
    raw_text: str


@dataclass
class PluginInfo:
    """Information about a Sarah plugin"""
    name: str
    description: str
    examples: List[str]
    keywords: List[str]
    parameters: List[str]


class SarahAICore:
    """
    Core AI system for Sarah that handles natural language understanding
    """
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.nlp = None
        self.sentence_model = None
        self.plugin_embeddings = {}
        self.plugins_info = {}
        
        # Initialize NLP models
        self._initialize_models()
        
        # Load plugin information
        self._load_plugin_definitions()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load AI configuration"""
        default_config = {
            "spacy_model": "en_core_web_sm",
            "sentence_model": "all-MiniLM-L6-v2",
            "confidence_threshold": 0.6,
            "max_suggestions": 3,
            "enable_conversation": True,
            "conversation_context_length": 5
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _initialize_models(self):
        """Initialize NLP models"""
        try:
            # Load spaCy model for NER and linguistic analysis
            self.nlp = spacy.load(self.config["spacy_model"])
            logger.info(f"Loaded spaCy model: {self.config['spacy_model']}")
        except OSError:
            logger.warning(f"spaCy model {self.config['spacy_model']} not found. Using basic tokenization.")
            self.nlp = None
        
        try:
            # Load sentence transformer for semantic similarity
            self.sentence_model = SentenceTransformer(self.config["sentence_model"])
            logger.info(f"Loaded sentence model: {self.config['sentence_model']}")
        except Exception as e:
            logger.error(f"Failed to load sentence model: {e}")
            self.sentence_model = None
    
    def _load_plugin_definitions(self):
        """Load plugin definitions and create embeddings"""
        # Define Sarah's built-in plugins with natural language descriptions
        self.plugins_info = {
            "weather": PluginInfo(
                name="weather",
                description="Get weather information and forecasts for any location",
                examples=[
                    "what's the weather like?",
                    "show me the weather in New York",
                    "is it going to rain today?",
                    "weather forecast for London"
                ],
                keywords=["weather", "temperature", "rain", "snow", "forecast", "climate"],
                parameters=["location"]
            ),
            "time": PluginInfo(
                name="time",
                description="Show current time and date information",
                examples=[
                    "what time is it?",
                    "show me the current time",
                    "what's today's date?",
                    "current time and date"
                ],
                keywords=["time", "date", "clock", "current", "now"],
                parameters=[]
            ),
            "wiki": PluginInfo(
                name="wiki",
                description="Search Wikipedia for information about topics",
                examples=[
                    "tell me about Albert Einstein",
                    "search Wikipedia for Python programming",
                    "what is machine learning?",
                    "wiki information about Paris"
                ],
                keywords=["wiki", "wikipedia", "information", "about", "tell me", "search"],
                parameters=["topic", "query"]
            ),
            "google": PluginInfo(
                name="google",
                description="Search Google for information and websites",
                examples=[
                    "google search for best restaurants",
                    "search the web for Python tutorials",
                    "find information about cars",
                    "web search for news"
                ],
                keywords=["google", "search", "web", "find", "look up"],
                parameters=["query", "search_term"]
            ),
            "youtube": PluginInfo(
                name="youtube",
                description="Search YouTube for videos",
                examples=[
                    "find videos about cooking",
                    "search YouTube for music",
                    "show me tutorials on programming",
                    "youtube search for funny cats"
                ],
                keywords=["youtube", "video", "videos", "watch", "music", "tutorial"],
                parameters=["query", "search_term"]
            ),
            "github": PluginInfo(
                name="github",
                description="Search GitHub for repositories and code",
                examples=[
                    "find Python projects on GitHub",
                    "search GitHub for machine learning repos",
                    "show me JavaScript libraries",
                    "github search for web frameworks"
                ],
                keywords=["github", "repository", "code", "project", "library", "framework"],
                parameters=["query", "search_term"]
            ),
            "whois": PluginInfo(
                name="whois",
                description="Get information about people, domains, or entities",
                examples=[
                    "who is Elon Musk?",
                    "tell me about Steve Jobs",
                    "information about Albert Einstein",
                    "whois domain.com"
                ],
                keywords=["who", "whois", "about", "information", "person", "biography"],
                parameters=["person", "domain", "entity"]
            ),
            "watch": PluginInfo(
                name="watch",
                description="Get movie and TV show information from IMDB",
                examples=[
                    "tell me about Titanic movie",
                    "movie information for Inception",
                    "show details for Breaking Bad",
                    "IMDB info for The Matrix"
                ],
                keywords=["movie", "film", "tv show", "series", "imdb", "watch", "cinema"],
                parameters=["title", "movie_name", "show_name"]
            ),
            "speedtest": PluginInfo(
                name="speedtest",
                description="Test internet connection speed",
                examples=[
                    "test my internet speed",
                    "check connection speed",
                    "how fast is my internet?",
                    "run speed test"
                ],
                keywords=["speed", "internet", "connection", "bandwidth", "test"],
                parameters=[]
            ),
            "adhan": PluginInfo(
                name="adhan",
                description="Get Islamic prayer times for locations",
                examples=[
                    "prayer times for Mecca",
                    "adhan times in Cairo Egypt",
                    "when is Fajr prayer in London?",
                    "Islamic prayer schedule"
                ],
                keywords=["prayer", "adhan", "islamic", "fajr", "dhuhr", "asr", "maghrib", "isha"],
                parameters=["city", "country"]
            ),
            "hi": PluginInfo(
                name="hi",
                description="Greeting and general conversation",
                examples=[
                    "hello",
                    "hi there",
                    "good morning",
                    "how are you?"
                ],
                keywords=["hello", "hi", "hey", "greetings", "good morning", "good evening"],
                parameters=[]
            ),
            "marketwatch": PluginInfo(
                name="marketwatch",
                description="Get stock market and financial information",
                examples=[
                    "stock price for Apple",
                    "market info for GOOGL",
                    "check Tesla stock",
                    "financial data for Microsoft"
                ],
                keywords=["stock", "market", "price", "shares", "financial", "investment"],
                parameters=["symbol", "stock_name", "country", "security_type"]
            )
        }
        
        # Create embeddings for plugin matching
        self._create_plugin_embeddings()
    
    def _create_plugin_embeddings(self):
        """Create embeddings for all plugins to enable semantic matching"""
        if not self.sentence_model:
            logger.warning("No sentence model available for embeddings")
            return
        
        for plugin_name, plugin_info in self.plugins_info.items():
            # Combine description, examples, and keywords for embedding
            text_content = []
            text_content.append(plugin_info.description)
            text_content.extend(plugin_info.examples)
            text_content.extend(plugin_info.keywords)
            
            # Create embedding for this plugin
            combined_text = " ".join(text_content)
            embedding = self.sentence_model.encode([combined_text])[0]
            self.plugin_embeddings[plugin_name] = embedding
        
        logger.info(f"Created embeddings for {len(self.plugin_embeddings)} plugins")
    
    def understand_input(self, user_input: str) -> Intent:
        """
        Main method to understand user input and return intent
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Intent object with plugin name, confidence, and extracted entities
        """
        # Clean and normalize input
        cleaned_input = self._clean_input(user_input)
        
        # Extract entities using spaCy if available
        entities = self._extract_entities(cleaned_input)
        
        # Find best matching plugin using semantic similarity
        plugin_match = self._find_best_plugin_match(cleaned_input)
        
        # Create intent object
        intent = Intent(
            plugin_name=plugin_match['plugin'],
            confidence=plugin_match['confidence'],
            entities=entities,
            raw_text=user_input
        )
        
        return intent
    
    def _clean_input(self, text: str) -> str:
        """Clean and normalize user input"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Convert to lowercase for processing (but keep original case in entities)
        return text.lower()
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities and important information from text"""
        entities = {}
        
        if self.nlp:
            doc = self.nlp(text)
            
            # Extract named entities
            for ent in doc.ents:
                entity_type = ent.label_.lower()
                if entity_type in ['person', 'org', 'gpe', 'loc']:  # Focus on relevant entities
                    entities[entity_type] = ent.text
            
            # Extract potential search terms (remaining content after removing stop words)
            search_terms = []
            for token in doc:
                if not token.is_stop and not token.is_punct and len(token.text) > 2:
                    search_terms.append(token.text)
            
            if search_terms:
                entities['search_terms'] = search_terms
        else:
            # Fallback: simple keyword extraction
            words = text.split()
            # Remove common stop words
            stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by'}
            search_terms = [word for word in words if word not in stop_words and len(word) > 2]
            if search_terms:
                entities['search_terms'] = search_terms
        
        return entities
    
    def _find_best_plugin_match(self, text: str) -> Dict[str, Any]:
        """Find the best matching plugin using semantic similarity"""
        
        if not self.sentence_model:
            # Fallback to keyword matching
            return self._keyword_based_matching(text)
        
        # Create embedding for user input
        input_embedding = self.sentence_model.encode([text])[0]
        
        best_match = {
            'plugin': 'hi',  # Default fallback
            'confidence': 0.0
        }
        
        # Calculate similarity with all plugin embeddings
        for plugin_name, plugin_embedding in self.plugin_embeddings.items():
            similarity = cosine_similarity(
                [input_embedding], 
                [plugin_embedding]
            )[0][0]
            
            if similarity > best_match['confidence']:
                best_match = {
                    'plugin': plugin_name,
                    'confidence': float(similarity)
                }
        
        return best_match
    
    def _keyword_based_matching(self, text: str) -> Dict[str, Any]:
        """Fallback keyword-based matching when no ML models available"""
        best_match = {
            'plugin': 'hi',
            'confidence': 0.0
        }
        
        words = set(text.lower().split())
        
        for plugin_name, plugin_info in self.plugins_info.items():
            # Check for keyword matches
            keyword_matches = sum(1 for keyword in plugin_info.keywords if keyword in text)
            
            # Simple scoring based on keyword matches
            score = keyword_matches / len(plugin_info.keywords) if plugin_info.keywords else 0
            
            if score > best_match['confidence']:
                best_match = {
                    'plugin': plugin_name,
                    'confidence': score
                }
        
        return best_match
    
    def get_suggestions(self, user_input: str, max_suggestions: int = None) -> List[Dict]:
        """Get multiple plugin suggestions for ambiguous input"""
        if max_suggestions is None:
            max_suggestions = self.config['max_suggestions']
        
        if not self.sentence_model:
            return [self._keyword_based_matching(user_input)]
        
        cleaned_input = self._clean_input(user_input)
        input_embedding = self.sentence_model.encode([cleaned_input])[0]
        
        suggestions = []
        
        for plugin_name, plugin_embedding in self.plugin_embeddings.items():
            similarity = cosine_similarity(
                [input_embedding], 
                [plugin_embedding]
            )[0][0]
            
            suggestions.append({
                'plugin': plugin_name,
                'confidence': float(similarity),
                'description': self.plugins_info[plugin_name].description
            })
        
        # Sort by confidence and return top suggestions
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        return suggestions[:max_suggestions]
    
    def format_response(self, intent: Intent, result: str = None) -> str:
        """Format AI response with context"""
        if intent.confidence < self.config['confidence_threshold']:
            suggestions = self.get_suggestions(intent.raw_text, 3)
            response = f"I'm not quite sure what you mean by '{intent.raw_text}'. "
            response += "Did you mean:\n"
            for i, suggestion in enumerate(suggestions, 1):
                response += f"{i}. {suggestion['description']} (confidence: {suggestion['confidence']:.2f})\n"
            return response
        
        # If we have a result, format it nicely
        if result:
            return f"Here's what I found:\n{result}"
        
        return f"I understood you want to use {intent.plugin_name} with confidence {intent.confidence:.2f}"


def create_ai_core(config_path: str = None) -> SarahAICore:
    """Factory function to create AI core instance"""
    return SarahAICore(config_path)


if __name__ == "__main__":
    # Test the AI core
    ai = create_ai_core()
    
    test_inputs = [
        "what's the weather like in New York?",
        "search for Python tutorials",
        "tell me about Einstein",
        "what time is it?",
        "test my internet speed"
    ]
    
    for test_input in test_inputs:
        intent = ai.understand_input(test_input)
        print(f"Input: {test_input}")
        print(f"Intent: {intent.plugin_name} (confidence: {intent.confidence:.2f})")
        print(f"Entities: {intent.entities}")
        print("-" * 50) 