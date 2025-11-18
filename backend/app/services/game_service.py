"""
Game and Quiz Generation Service
Creates interactive learning content using Claude AI
"""
import json
import random
from typing import Dict, Any, List
from .claude_service import ClaudeService


class GameService:
    """Service for generating interactive games and quizzes"""

    def __init__(self):
        """Initialize with Claude service"""
        self.claude = ClaudeService()

    async def generate_quiz(
        self,
        homework_content: str,
        subject: str,
        analysis_results: Dict[str, Any],
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive quiz based on homework content
        """
        if not self.claude.enabled:
            return self._mock_quiz(subject, difficulty)

        topics = analysis_results.get("topics", [subject])
        key_concepts = analysis_results.get("key_concepts", [])

        prompt = f"""Generate a comprehensive quiz based on this homework content with 5-8 questions
that test different cognitive levels (from remember to analyze).

HOMEWORK CONTENT:
{homework_content}

SUBJECT: {subject}
TOPICS: {', '.join(topics)}
KEY CONCEPTS: {', '.join(key_concepts)}
DIFFICULTY: {difficulty}

Include:
- Variety of question types: multiple choice, true/false, short answer
- Progressive difficulty within the quiz
- Instant feedback with explanations
- Learning hints for incorrect answers

Output JSON with this structure:
{{
  "quiz_type": "comprehensive_review",
  "title": "Creative quiz name",
  "learning_objective": "What student learns",
  "difficulty": "{difficulty}",
  "estimated_duration_minutes": 10,
  "questions": [
    {{
      "id": "q1",
      "type": "multiple_choice|true_false|short_answer",
      "question": "Question text",
      "options": ["option1", "option2", "option3", "option4"],
      "correct_answer": "correct option or answer",
      "hints": ["hint1", "hint2"],
      "explanation": "Why this answer is correct and what it teaches",
      "points": 10
    }}
  ],
  "scoring": {{
    "total_points": 80,
    "passing_score": 60,
    "time_bonus": true
  }},
  "feedback_messages": {{
    "excellent": "Message for 90%+",
    "good": "Message for 70-89%",
    "needs_improvement": "Message for below 70%"
  }}
}}

Respond with ONLY the JSON, no additional text."""

        try:
            message = self.claude.client.messages.create(
                model=self.claude.model,
                max_tokens=3072,
                system=self.claude._get_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            quiz = json.loads(message.content[0].text)
            return quiz

        except Exception as e:
            print(f"Quiz generation error: {e}")
            return self._mock_quiz(subject, difficulty)

    async def generate_game(
        self,
        homework_content: str,
        subject: str,
        analysis_results: Dict[str, Any],
        game_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        Generate an interactive game based on homework content
        """
        if not self.claude.enabled:
            return self._mock_game(subject, game_type)

        topics = analysis_results.get("topics", [subject])

        prompt = f"""You are a creative educational game designer. Based on the homework content below,
generate an interactive game that is:
- Engaging and age-appropriate
- Directly aligned with the learning content
- Completable in 5-10 minutes
- Includes scoring/progress tracking

HOMEWORK CONTENT:
{homework_content}

SUBJECT: {subject}
TOPICS: {', '.join(topics)}
GAME TYPE: {game_type if game_type != 'auto' else 'choose the most appropriate'}

Generate a game specification in this JSON format:
{{
  "game_type": "word_puzzle|matching|fill_blank|sequence|memory",
  "title": "Creative game name",
  "description": "Brief description of how to play",
  "learning_objective": "What player learns",
  "rules": ["rule1", "rule2", "rule3"],
  "difficulty": "easy|medium|hard",
  "questions": [
    {{
      "id": "q1",
      "prompt": "Game challenge/question",
      "answer_type": "text|choice|drag_drop",
      "correct_answers": ["answer"],
      "options": ["option1", "option2", "option3", "option4"],
      "hints": ["hint1", "hint2"],
      "explanation": "Why this answer is correct",
      "points": 10
    }}
  ],
  "scoring": {{
    "points_per_question": 10,
    "bonus_multiplier": 1.5,
    "time_bonus": true,
    "streak_bonus": true
  }},
  "feedback_messages": {{
    "correct": "Motivational message for correct answer",
    "incorrect": "Supportive message with learning point",
    "completion": "Summary of learning achieved"
  }},
  "assets": {{
    "background_color": "#hexcolor",
    "theme": "colorful|minimalist|playful"
  }}
}}

Respond with ONLY the JSON, no additional text."""

        try:
            message = self.claude.client.messages.create(
                model=self.claude.model,
                max_tokens=3072,
                system=self.claude._get_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            game = json.loads(message.content[0].text)
            return game

        except Exception as e:
            print(f"Game generation error: {e}")
            return self._mock_game(subject, game_type)

    async def generate_review_material(
        self,
        homework_content: str,
        subject: str,
        topics: List[str]
    ) -> Dict[str, Any]:
        """
        Create a concise study guide/summary
        """
        if not self.claude.enabled:
            return self._mock_review(subject, topics)

        prompt = f"""Create a concise study guide/summary for the following homework topics:

HOMEWORK CONTENT:
{homework_content}

SUBJECT: {subject}
TOPICS: {', '.join(topics)}

Include:
- Key concept definitions (simple, clear language)
- 1-2 worked examples for each concept
- Common mistakes to avoid
- Memory tricks or mnemonics where applicable
- Quick review questions

Output as structured JSON:
{{
  "title": "Study Guide Title",
  "subject": "{subject}",
  "sections": [
    {{
      "topic": "Topic name",
      "summary": "Brief explanation",
      "key_points": ["point1", "point2"],
      "examples": [
        {{
          "problem": "Example problem",
          "solution": "Step-by-step solution",
          "explanation": "Why this approach works"
        }}
      ],
      "common_mistakes": ["mistake1", "mistake2"],
      "memory_aids": ["mnemonic or trick"]
    }}
  ],
  "quick_review_questions": [
    {{
      "question": "Review question",
      "answer": "Brief answer"
    }}
  ],
  "estimated_study_time_minutes": 15
}}

Respond with ONLY the JSON, no additional text."""

        try:
            message = self.claude.client.messages.create(
                model=self.claude.model,
                max_tokens=2048,
                system=self.claude._get_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            review = json.loads(message.content[0].text)
            return review

        except Exception as e:
            print(f"Review material generation error: {e}")
            return self._mock_review(subject, topics)

    def _mock_quiz(self, subject: str, difficulty: str) -> Dict[str, Any]:
        """Mock quiz when Claude is not available"""
        return {
            "quiz_type": "comprehensive_review",
            "title": f"{subject.title()} Practice Quiz",
            "learning_objective": f"Review and practice {subject} concepts",
            "difficulty": difficulty,
            "estimated_duration_minutes": 10,
            "questions": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "question": f"What is a key concept in {subject}?",
                    "options": ["Concept A", "Concept B", "Concept C", "All of the above"],
                    "correct_answer": "All of the above",
                    "hints": ["Think about what you learned", "All options might be relevant"],
                    "explanation": "These are all important concepts to understand",
                    "points": 20
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "question": f"Practice is important in {subject}.",
                    "options": ["True", "False"],
                    "correct_answer": "True",
                    "hints": ["Consider how skills are developed"],
                    "explanation": "Regular practice is essential for mastery",
                    "points": 20
                }
            ],
            "scoring": {
                "total_points": 40,
                "passing_score": 28,
                "time_bonus": True
            },
            "feedback_messages": {
                "excellent": "Outstanding work! You've mastered these concepts!",
                "good": "Great job! You're on the right track!",
                "needs_improvement": "Keep practicing - you'll get there!"
            }
        }

    def _mock_game(self, subject: str, game_type: str) -> Dict[str, Any]:
        """Mock game when Claude is not available"""
        return {
            "game_type": "matching",
            "title": f"{subject.title()} Matching Challenge",
            "description": "Match concepts with their definitions",
            "learning_objective": f"Reinforce {subject} vocabulary and concepts",
            "rules": [
                "Match each term with its correct definition",
                "You have 3 chances per question",
                "Earn bonus points for quick correct answers"
            ],
            "difficulty": "medium",
            "questions": [
                {
                    "id": "q1",
                    "prompt": "Match: Basic Concept",
                    "answer_type": "choice",
                    "correct_answers": ["Definition of basic concept"],
                    "options": [
                        "Definition of basic concept",
                        "Another definition",
                        "Different concept",
                        "Unrelated term"
                    ],
                    "hints": ["Think about the fundamentals", "Review your notes"],
                    "explanation": "This is the correct definition because...",
                    "points": 15
                }
            ],
            "scoring": {
                "points_per_question": 15,
                "bonus_multiplier": 1.5,
                "time_bonus": True,
                "streak_bonus": True
            },
            "feedback_messages": {
                "correct": "Perfect match! You're doing great!",
                "incorrect": "Not quite, but good try! Let's review this concept.",
                "completion": "Excellent work! You've completed the matching game!"
            },
            "assets": {
                "background_color": "#4A90E2",
                "theme": "playful"
            }
        }

    def _mock_review(self, subject: str, topics: List[str]) -> Dict[str, Any]:
        """Mock review material when Claude is not available"""
        return {
            "title": f"{subject.title()} Study Guide",
            "subject": subject,
            "sections": [
                {
                    "topic": topics[0] if topics else subject,
                    "summary": f"Key concepts and principles in {subject}",
                    "key_points": [
                        "Understanding the fundamentals",
                        "Applying concepts to problems",
                        "Practice makes perfect"
                    ],
                    "examples": [
                        {
                            "problem": "Sample problem",
                            "solution": "Step 1: Identify what you know\\nStep 2: Apply the concept\\nStep 3: Verify your answer",
                            "explanation": "This approach helps you systematically solve problems"
                        }
                    ],
                    "common_mistakes": [
                        "Rushing through problems",
                        "Not showing your work",
                        "Forgetting to check answers"
                    ],
                    "memory_aids": ["Break problems into smaller steps", "Draw diagrams when possible"]
                }
            ],
            "quick_review_questions": [
                {
                    "question": f"What is the most important thing to remember about {subject}?",
                    "answer": "Practice regularly and understand the core concepts"
                }
            ],
            "estimated_study_time_minutes": 15
        }
