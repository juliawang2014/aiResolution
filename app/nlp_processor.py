import re
import spacy
from typing import Dict, List, Any
from datetime import datetime
import random

class NLPProcessor:
    def __init__(self):
        # For now, we'll use simple rule-based processing
        # In production, you'd load spaCy models: nlp = spacy.load("en_core_web_sm")
        self.progress_keywords = {
            "high": ["completed", "finished", "done", "achieved", "accomplished", "success"],
            "medium": ["progress", "working", "started", "began", "improving", "advancing"],
            "low": ["struggling", "difficult", "challenging", "stuck", "slow", "behind"]
        }
        
        self.sentiment_keywords = {
            "positive": ["great", "excellent", "amazing", "fantastic", "good", "happy", "excited"],
            "negative": ["bad", "terrible", "awful", "frustrated", "disappointed", "difficult"],
            "neutral": ["okay", "fine", "normal", "regular", "standard"]
        }

    def analyze_progress_update(self, text: str, goal_title: str) -> Dict[str, Any]:
        """Analyze a natural language progress update"""
        text_lower = text.lower()
        
        # Extract progress percentage
        progress_percentage = self._extract_progress_percentage(text_lower)
        
        # Determine sentiment
        sentiment = self._analyze_sentiment(text_lower)
        
        # Extract key insights
        insights = self._extract_insights(text, goal_title)
        
        return {
            "progress_percentage": progress_percentage,
            "sentiment": sentiment,
            "insights": insights,
            "processed_at": datetime.utcnow().isoformat()
        }

    def _extract_progress_percentage(self, text: str) -> float:
        """Extract progress percentage from text"""
        # Look for explicit percentages
        percentage_match = re.search(r'(\d+)%', text)
        if percentage_match:
            return float(percentage_match.group(1))
        
        # Look for fractions
        fraction_match = re.search(r'(\d+)/(\d+)', text)
        if fraction_match:
            numerator = float(fraction_match.group(1))
            denominator = float(fraction_match.group(2))
            return (numerator / denominator) * 100
        
        # Use keyword-based estimation
        for level, keywords in self.progress_keywords.items():
            if any(keyword in text for keyword in keywords):
                if level == "high":
                    return random.uniform(80, 100)
                elif level == "medium":
                    return random.uniform(40, 79)
                else:  # low
                    return random.uniform(0, 39)
        
        # Default to small progress if update is provided
        return random.uniform(5, 15)

    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of the text"""
        positive_score = sum(1 for word in self.sentiment_keywords["positive"] if word in text)
        negative_score = sum(1 for word in self.sentiment_keywords["negative"] if word in text)
        
        if positive_score > negative_score:
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        else:
            return "neutral"

    def _extract_insights(self, text: str, goal_title: str) -> List[str]:
        """Extract key insights from the update"""
        insights = []
        
        # Simple keyword-based insights
        if any(word in text.lower() for word in ["challenge", "difficult", "problem"]):
            insights.append("Facing challenges that may need attention")
        
        if any(word in text.lower() for word in ["milestone", "achievement", "completed"]):
            insights.append("Reached an important milestone")
        
        if any(word in text.lower() for word in ["plan", "strategy", "approach"]):
            insights.append("Developing new strategies or approaches")
        
        if any(word in text.lower() for word in ["time", "schedule", "deadline"]):
            insights.append("Time management considerations mentioned")
        
        return insights

    def generate_feedback(self, goal, analysis: Dict[str, Any]) -> str:
        """Generate AI feedback based on progress analysis"""
        progress = analysis.get("progress_percentage", 0)
        sentiment = analysis.get("sentiment", "neutral")
        insights = analysis.get("insights", [])
        
        feedback_parts = []
        
        # Progress-based feedback
        if progress >= 80:
            feedback_parts.append("Excellent progress! You're doing great.")
        elif progress >= 50:
            feedback_parts.append("Good momentum! Keep up the steady progress.")
        elif progress >= 20:
            feedback_parts.append("You're making progress. Consider what's working well.")
        else:
            feedback_parts.append("Every step counts. What small action can you take today?")
        
        # Sentiment-based feedback
        if sentiment == "positive":
            feedback_parts.append("Your positive attitude is a great asset for achieving this goal.")
        elif sentiment == "negative":
            feedback_parts.append("Challenges are part of the journey. Consider breaking this into smaller steps.")
        
        # Insight-based feedback
        if "Facing challenges" in str(insights):
            feedback_parts.append("When facing obstacles, try the 5-minute rule: commit to just 5 minutes of work.")
        
        if "Reached an important milestone" in str(insights):
            feedback_parts.append("Celebrate this achievement! Momentum builds on success.")
        
        return " ".join(feedback_parts)