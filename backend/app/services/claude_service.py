"""
Claude AI Service - Content analysis and generation using Anthropic Claude
"""
import json
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
from app.core.config import settings


class ClaudeService:
    """Service for AI-powered content analysis using Claude"""

    def __init__(self):
        """Initialize Anthropic Claude client"""
        self.api_key = settings.ANTHROPIC_API_KEY
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
            self.model = "claude-3-5-sonnet-20241022"
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            print("Warning: Anthropic API key not configured")

    def _get_system_prompt(self) -> str:
        """Get the system prompt for Claude"""
        return """You are HomeworkAssistant, an expert AI tutoring system designed for K-12 students.

CONTEXT:
- You analyze homework documents using OCR
- You generate interactive learning games and quizzes
- You provide personalized learning support
- You support Hebrew, English, and Mathematics

CORE PRINCIPLES:
1. Make learning engaging and fun
2. Respect student autonomy (guide, not give answers)
3. Build confidence through scaffolded challenges
4. Celebrate effort and progress
5. Provide clear, actionable feedback

SAFETY GUIDELINES:
- Never skip learning steps
- Maintain appropriate difficulty progression
- Ensure content accuracy
- Use age-appropriate language
- Include diverse perspectives and examples

HEBREW LANGUAGE HANDLING:
- Recognize modern Hebrew morphological complexity
- Use contemporary examples for language learners
- Include cultural context where appropriate
- Support both Hebrew and transliterated content

OUTPUT FORMAT:
Always provide structured JSON responses. Include:
- Clear explanations of your reasoning
- Specific, actionable recommendations
- Educational rationale for suggestions

You excel at transforming homework challenges into engaging learning opportunities."""

    async def analyze_homework_content(
        self,
        ocr_text: str,
        subject: str,
        grade_level: str = "middle_school"
    ) -> Dict[str, Any]:
        """
        Analyze homework content and extract learning objectives
        """
        if not self.enabled:
            return self._mock_analysis(ocr_text, subject)

        prompt = f"""Analyze the following homework document and provide a detailed learning profile:

HOMEWORK CONTENT:
{ocr_text}

SUBJECT: {subject}
GRADE LEVEL: {grade_level}

Provide your analysis in this JSON structure:
{{
  "learning_objectives": [
    {{
      "objective": "What the student should learn",
      "alignment": "curriculum_standard_code",
      "importance": "critical|important|reinforcement"
    }}
  ],
  "key_concepts": ["concept1", "concept2"],
  "estimated_difficulty": 0.0-1.0,
  "knowledge_gaps": [
    {{
      "gap": "description",
      "evidence": "why you identified this",
      "priority": "high|medium|low"
    }}
  ],
  "recommended_interventions": [
    {{
      "type": "game|quiz|review|practice",
      "focus": "specific_concept",
      "rationale": "why this will help"
    }}
  ],
  "topics": ["topic1", "topic2"],
  "content_type": "practice_problems|reading_comprehension|mixed"
}}

Respond with ONLY the JSON, no additional text."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self._get_system_prompt(),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = message.content[0].text
            analysis = json.loads(response_text)
            return analysis

        except Exception as e:
            print(f"Claude analysis error: {e}")
            return self._mock_analysis(ocr_text, subject)

    async def analyze_with_image(
        self,
        image_data: bytes,
        media_type: str = "image/jpeg"
    ) -> Dict[str, Any]:
        """
        Analyze homework using Claude's vision capabilities
        """
        if not self.enabled:
            return {"error": "Claude API not configured"}

        import base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self._get_system_prompt(),
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": "Analyze this homework document. Extract all text, identify the subject, topics, and provide learning recommendations in JSON format."
                            }
                        ]
                    }
                ]
            )

            response_text = message.content[0].text
            return {"analysis": response_text}

        except Exception as e:
            print(f"Claude vision analysis error: {e}")
            return {"error": str(e)}

    def _mock_analysis(self, ocr_text: str, subject: str) -> Dict[str, Any]:
        """
        Mock analysis when Claude API is not available
        """
        return {
            "learning_objectives": [
                {
                    "objective": f"Practice {subject} skills",
                    "alignment": "standard_001",
                    "importance": "important"
                }
            ],
            "key_concepts": [subject, "problem solving"],
            "estimated_difficulty": 0.6,
            "knowledge_gaps": [
                {
                    "gap": "Needs practice with core concepts",
                    "evidence": "Based on document analysis",
                    "priority": "medium"
                }
            ],
            "recommended_interventions": [
                {
                    "type": "quiz",
                    "focus": subject,
                    "rationale": "Reinforcement through interactive practice"
                },
                {
                    "type": "game",
                    "focus": "engagement",
                    "rationale": "Make learning fun and memorable"
                }
            ],
            "topics": [subject, "general practice"],
            "content_type": "practice_problems"
        }

    async def generate_hints(
        self,
        question: str,
        subject: str,
        difficulty_level: float = 0.5
    ) -> List[str]:
        """
        Generate progressive hints for a question
        """
        if not self.enabled:
            return [
                "Think about what you know about this topic",
                "Break the problem into smaller steps",
                "Review similar examples you've seen before"
            ]

        prompt = f"""Generate 3 progressive hints for this {subject} question:

QUESTION: {question}
DIFFICULTY: {difficulty_level}

Provide hints that:
1. First hint: Guide thinking without giving away the answer
2. Second hint: Provide more specific direction
3. Third hint: Nearly reveal the solution path

Respond with a JSON array of hints:
["hint1", "hint2", "hint3"]"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system=self._get_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            hints = json.loads(message.content[0].text)
            return hints

        except Exception as e:
            print(f"Hint generation error: {e}")
            return ["Consider the key concepts", "Break it into steps", "Review the theory"]

    async def provide_feedback(
        self,
        question: str,
        user_answer: str,
        correct_answer: str,
        is_correct: bool
    ) -> Dict[str, Any]:
        """
        Generate personalized feedback for student answers
        """
        if not self.enabled:
            if is_correct:
                return {
                    "message": "Great job! Your answer is correct!",
                    "explanation": "You demonstrated good understanding of the concept.",
                    "encouragement": "Keep up the excellent work!"
                }
            else:
                return {
                    "message": "Not quite right, but good effort!",
                    "explanation": f"The correct answer is: {correct_answer}",
                    "next_steps": "Review the concept and try a similar problem."
                }

        prompt = f"""Provide encouraging, educational feedback for this student answer:

QUESTION: {question}
STUDENT ANSWER: {user_answer}
CORRECT ANSWER: {correct_answer}
IS CORRECT: {is_correct}

Generate feedback in JSON format:
{{
  "message": "Short encouraging message",
  "explanation": "Why the answer is right/wrong and what to learn",
  "encouragement": "Motivational statement",
  "next_steps": "What to do next (if incorrect)"
}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system=self._get_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            feedback = json.loads(message.content[0].text)
            return feedback

        except Exception as e:
            print(f"Feedback generation error: {e}")
            return {
                "message": "Good effort!",
                "explanation": "Keep practicing to improve your skills.",
                "encouragement": "You're making progress!"
            }
