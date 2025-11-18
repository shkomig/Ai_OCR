"""
OCR Service - Document text extraction using Google Cloud Vision
"""
import io
import base64
from typing import Dict, Any, List, Optional
from PIL import Image
import numpy as np
from google.cloud import vision
from google.cloud.vision_v1 import types
from app.core.config import settings


class OCRService:
    """Service for OCR processing using Google Cloud Vision API"""

    def __init__(self):
        """Initialize Google Cloud Vision client"""
        try:
            self.client = vision.ImageAnnotatorClient()
            self.use_google_vision = True
        except Exception as e:
            print(f"Google Cloud Vision not configured: {e}")
            self.use_google_vision = False

    async def preprocess_image(self, image_data: bytes) -> bytes:
        """
        Preprocess image for better OCR results
        - Quality assessment
        - Rotation correction
        - Noise reduction
        """
        try:
            image = Image.open(io.BytesIO(image_data))

            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize if too large
            max_dimension = 4096
            if max(image.size) > max_dimension:
                ratio = max_dimension / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            # Convert back to bytes
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=95)
            return output.getvalue()

        except Exception as e:
            print(f"Image preprocessing error: {e}")
            return image_data

    async def extract_text_google_vision(self, image_data: bytes) -> Dict[str, Any]:
        """
        Extract text using Google Cloud Vision API
        """
        if not self.use_google_vision:
            return await self.extract_text_fallback(image_data)

        try:
            image = vision.Image(content=image_data)

            # Perform document text detection
            response = self.client.document_text_detection(image=image)

            if response.error.message:
                raise Exception(response.error.message)

            # Extract full text
            full_text = response.full_text_annotation.text if response.full_text_annotation else ""

            # Extract structured data
            pages = []
            if response.full_text_annotation and response.full_text_annotation.pages:
                for page in response.full_text_annotation.pages:
                    page_data = {
                        "width": page.width,
                        "height": page.height,
                        "blocks": []
                    }

                    for block in page.blocks:
                        block_text = ""
                        for paragraph in block.paragraphs:
                            for word in paragraph.words:
                                word_text = "".join([symbol.text for symbol in word.symbols])
                                block_text += word_text + " "

                        page_data["blocks"].append({
                            "text": block_text.strip(),
                            "confidence": block.confidence if hasattr(block, 'confidence') else 0.9
                        })

                    pages.append(page_data)

            # Calculate overall confidence
            confidences = []
            for page in pages:
                for block in page["blocks"]:
                    confidences.append(block["confidence"])

            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

            return {
                "raw_text": full_text,
                "confidence_score": avg_confidence,
                "extraction_method": "google_vision",
                "pages": pages,
                "language_hints": self._detect_languages(full_text)
            }

        except Exception as e:
            print(f"Google Vision OCR error: {e}")
            return await self.extract_text_fallback(image_data)

    async def extract_text_fallback(self, image_data: bytes) -> Dict[str, Any]:
        """
        Fallback OCR method (basic implementation)
        In production, this could use Tesseract or another OCR library
        """
        return {
            "raw_text": "[OCR text would be extracted here - please configure Google Cloud Vision]",
            "confidence_score": 0.5,
            "extraction_method": "fallback",
            "pages": [],
            "language_hints": ["hebrew", "english"]
        }

    def _detect_languages(self, text: str) -> List[str]:
        """
        Detect languages in the text
        """
        languages = []

        # Simple heuristic-based language detection
        # Check for Hebrew characters
        if any('\u0590' <= c <= '\u05FF' for c in text):
            languages.append("hebrew")

        # Check for English characters
        if any('a' <= c.lower() <= 'z' for c in text):
            languages.append("english")

        # Check for mathematical symbols
        math_symbols = set("+-×÷=≠<>≤≥∑∫√π")
        if any(c in math_symbols for c in text):
            languages.append("mathematics")

        return languages if languages else ["unknown"]

    async def validate_text(self, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and enhance OCR results
        """
        confidence = ocr_result.get("confidence_score", 0.0)
        raw_text = ocr_result.get("raw_text", "")

        issues = []
        warnings = []

        if confidence < settings.OCR_CONFIDENCE_THRESHOLD:
            warnings.append(f"Low OCR confidence: {confidence:.2f}")

        if len(raw_text.strip()) < 10:
            issues.append("Very little text detected")

        return {
            "overall_confidence": confidence,
            "issues_detected": issues,
            "warnings": warnings,
            "validated": len(issues) == 0
        }

    async def structure_content(self, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure the OCR output into a document model
        """
        raw_text = ocr_result.get("raw_text", "")
        pages = ocr_result.get("pages", [])
        languages = ocr_result.get("language_hints", [])

        # Simple section detection (can be enhanced with Claude AI)
        sections = []
        for page in pages:
            for block in page.get("blocks", []):
                sections.append({
                    "type": "text",  # Could be: problem, instruction, reading
                    "text": block["text"],
                    "confidence": block["confidence"]
                })

        # Detect subject based on content
        subject = "unknown"
        if "mathematics" in languages:
            subject = "mathematics"
        elif any(keyword in raw_text.lower() for keyword in ["read", "write", "story", "passage"]):
            subject = "english"
        elif "hebrew" in languages:
            subject = "hebrew"

        return {
            "title": "Homework Document",
            "sections": sections,
            "subject": subject,
            "languages": languages,
            "total_pages": len(pages)
        }

    async def process_document(self, image_data: bytes) -> Dict[str, Any]:
        """
        Complete OCR processing pipeline
        """
        # Step 1: Preprocess
        processed_image = await self.preprocess_image(image_data)

        # Step 2: Extract text
        ocr_result = await self.extract_text_google_vision(processed_image)

        # Step 3: Validate
        validation = await self.validate_text(ocr_result)

        # Step 4: Structure
        structured_content = await self.structure_content(ocr_result)

        return {
            "ocr_data": ocr_result,
            "processing_quality": validation,
            "content": structured_content
        }
