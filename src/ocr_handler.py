"""
OCR Receipt Handler Module

Handles receipt image processing and text extraction.
Placeholder for vision model integration (Azure AI Vision / OpenAI).
Supports parsing of OCR text output into structured expense data.

Author: RodZilla (CTO, GrowBiz)
"""

import re
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class ParsedReceipt:
    """Structured data extracted from a receipt.
    
    Attributes:
        amount: Total transaction amount
        merchant: Store or vendor name
        date: Transaction date (YYYY-MM-DD)
        items: List of purchased items with prices
        subtotal: Subtotal before tax
        tax: Tax amount
        category: Auto-detected category
        confidence: Extraction confidence score (0-1)
        raw_text: Original OCR text
    """
    amount: Optional[float] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    items: Optional[list] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    category: Optional[str] = None
    confidence: float = 0.0
    raw_text: Optional[str] = None


class OCRHandler:
    """Receipt OCR processing handler.
    
    Provides both placeholder vision model integration
    and manual text parsing capabilities.
    """
    
    # Common merchant name patterns
    MERCHANT_PATTERNS = [
        r"^([A-Z][A-Z\s&]+)\s*(?:INC|LLC|LTD|CO|STORE|MARKET)?\.?$",
        r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Store|Market|Restaurant|Cafe|Pharmacy)$",
        r"MERCHANT:\s*(.+?)(?:\n|$)",
        r"STORE\s*#?\d*\s*(.+?)(?:\n|$)",
    ]
    
    # Amount patterns (handles various formats)
    AMOUNT_PATTERNS = [
        r"TOTAL[\s:]*\$?([\d,]+\.\d{2})",
        r"AMOUNT[\s:]*\$?([\d,]+\.\d{2})",
        r"\$?([\d,]+\.\d{2})\s*(?:USD|\$)?\s*$",
        r"BALANCE\s+DUE[\s:]*\$?([\d,]+\.\d{2})",
        r"PAY[\s:]*\$?([\d,]+\.\d{2})",
    ]
    
    # Date patterns
    DATE_PATTERNS = [
        r"(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{2,4})",  # MM/DD/YYYY or DD/MM/YYYY
        r"(\d{4})[/\-\.](\d{1,2})[/\-\.](\d{1,2})",      # YYYY/MM/DD
        r"(\d{1,2})\s+([A-Za-z]{3,9})\s+(\d{2,4})",      # 25 Dec 2024
        r"([A-Za-z]{3,9})\s+(\d{1,2}),?\s+(\d{2,4})",     # Dec 25, 2024
    ]
    
    # Item line patterns
    ITEM_PATTERN = r"([\w\s\-\(\)\.]+?)\s+\$?([\d,]+\.\d{2})"
    
    # Category detection keywords
    CATEGORY_KEYWORDS = {
        "groceries": ["grocery", "supermarket", "market", "food", "produce", "meat", "dairy"],
        "dining": ["restaurant", "cafe", "coffee", "pizza", "sushi", "burger", "kitchen"],
        "transportation": ["gas", "fuel", "uber", "lyft", "taxi", "parking", "toll"],
        "utilities": ["electric", "water", "gas", "internet", "phone", "cable"],
        "entertainment": ["movie", "theater", "netflix", "spotify", "game", "concert"],
        "shopping": ["clothing", "apparel", "shoes", "electronics", "amazon", "walmart"],
        "healthcare": ["pharmacy", "drug", "medical", "dental", "hospital", "clinic"],
        "home": ["hardware", "furniture", "home", "garden", "improvement"],
    }
    
    def __init__(self, vision_api_key: Optional[str] = None) -> None:
        """Initialize OCR handler.
        
        Args:
            vision_api_key: Optional API key for vision service
        """
        self.vision_api_key = vision_api_key
        logger.info("OCRHandler initialized")
    
    # ═══════════════════════════════════════════════════════════
    # PLACEHOLDER: Vision Model Integration
    # ═══════════════════════════════════════════════════════════
    
    def process_image_azure(self, image_path: str) -> ParsedReceipt:
        """Process receipt image using Azure AI Vision.
        
        PLACEHOLDER: Implement when Azure credentials are configured.
        
        Args:
            image_path: Path to receipt image file
            
        Returns:
            ParsedReceipt with extracted data
            
        Raises:
            NotImplementedError: Until Azure integration is complete
        """
        logger.info(f"Azure Vision processing placeholder: {image_path}")
        # TODO: Implement Azure AI Vision OCR
        # from azure.ai.vision.imageanalysis import ImageAnalysisClient
        # from azure.ai.vision.imageanalysis.models import VisualFeatures
        # from azure.core.credentials import AzureKeyCredential
        #
        # client = ImageAnalysisClient(
        #     endpoint="https://your-resource.cognitiveservices.azure.com",
        #     credential=AzureKeyCredential(self.vision_api_key)
        # )
        # result = client.analyze(
        #     image_data=open(image_path, "rb"),
        #     visual_features=[VisualFeatures.READ]
        # )
        # return self.parse_text(result.read.blocks[0].lines)
        
        raise NotImplementedError(
            "Azure Vision integration requires configured credentials. "
            "Use process_image_local() for manual text input or "
            "set vision_api_key for cloud processing."
        )
    
    def process_image_openai(self, image_path: str) -> ParsedReceipt:
        """Process receipt image using OpenAI Vision API.
        
        PLACEHOLDER: Implement when OpenAI API key is configured.
        
        Args:
            image_path: Path to receipt image file
            
        Returns:
            ParsedReceipt with extracted data
        """
        logger.info(f"OpenAI Vision processing placeholder: {image_path}")
        # TODO: Implement OpenAI GPT-4 Vision
        # import base64
        # from openai import OpenAI
        #
        # client = OpenAI(api_key=self.vision_api_key)
        # with open(image_path, "rb") as f:
        #     base64_image = base64.b64encode(f.read()).decode()
        #
        # response = client.chat.completions.create(
        #     model="gpt-4-vision-preview",
        #     messages=[{
        #         "role": "user",
        #         "content": [
        #             {"type": "text", "text": "Extract receipt data: merchant, total, date, items"},
        #             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        #         ]
        #     }]
        # )
        # return self.parse_text(response.choices[0].message.content)
        
        raise NotImplementedError(
            "OpenAI Vision integration requires configured API key. "
            "Use process_image_local() for manual text input."
        )
    
    # ═══════════════════════════════════════════════════════════
    # TEXT PARSING (Production Ready)
    # ═══════════════════════════════════════════════════════════
    
    def parse_text(self, text: str) -> ParsedReceipt:
        """Parse OCR text output into structured receipt data.
        
        Args:
            text: Raw OCR text from receipt
            
        Returns:
            ParsedReceipt with extracted fields
        """
        logger.info("Parsing receipt text")
        
        receipt = ParsedReceipt(raw_text=text)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # Extract merchant
        receipt.merchant = self._extract_merchant(lines)
        
        # Extract total amount
        receipt.amount = self._extract_amount(text)
        
        # Extract date
        receipt.date = self._extract_date(text)
        
        # Extract items
        receipt.items = self._extract_items(lines)
        
        # Calculate subtotal and tax if available
        receipt.subtotal = self._extract_subtotal(text)
        receipt.tax = self._extract_tax(text)
        
        # Detect category
        receipt.category = self._detect_category(
            receipt.merchant,
            text,
            receipt.items
        )
        
        # Calculate confidence
        receipt.confidence = self._calculate_confidence(receipt)
        
        logger.info(
            f"Parsed receipt: {receipt.merchant} | "
            f"${receipt.amount:.2f} | {receipt.date} | "
            f"confidence={receipt.confidence:.2f}"
        )
        
        return receipt
    
    def _extract_merchant(self, lines: list[str]) -> Optional[str]:
        """Extract merchant name from receipt lines."""
        # Try first few lines (merchant usually at top)
        for line in lines[:5]:
            for pattern in self.MERCHANT_PATTERNS:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    merchant = match.group(1).strip()
                    if len(merchant) > 2:  # Avoid single letters
                        return merchant.title()
        
        # Fallback: use first non-empty, non-numeric line
        for line in lines[:3]:
            if not re.match(r"^[\d\s\.\$]+$", line) and len(line) > 2:
                return line.title()
        
        return "Unknown Merchant"
    
    def _extract_amount(self, text: str) -> Optional[float]:
        """Extract total amount from receipt text."""
        amounts = []
        
        for pattern in self.AMOUNT_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                try:
                    amount_str = match.group(1).replace(",", "")
                    amount = float(amount_str)
                    if 0 < amount < 100000:  # Sanity check
                        amounts.append(amount)
                except (ValueError, IndexError):
                    continue
        
        # Return largest amount (usually the total)
        return max(amounts) if amounts else None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract transaction date from receipt text."""
        for pattern in self.DATE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                try:
                    groups = match.groups()
                    
                    # Try to determine format and parse
                    if len(groups[2]) == 4:  # MM/DD/YYYY or DD/MM/YYYY
                        month, day, year = int(groups[0]), int(groups[1]), groups[2]
                        # Assume MM/DD/YYYY for US receipts
                        return f"{year}-{month:02d}-{day:02d}"
                    
                    elif len(groups[0]) == 4:  # YYYY/MM/DD
                        year, month, day = groups[0], int(groups[1]), int(groups[2])
                        return f"{year}-{month:02d}-{day:02d}"
                    
                    else:  # Text format
                        # Parse "25 Dec 2024" or "Dec 25, 2024"
                        date_str = match.group(0)
                        for fmt in ["%d %b %Y", "%b %d, %Y", "%b %d %Y"]:
                            try:
                                dt = datetime.strptime(date_str, fmt)
                                return dt.strftime("%Y-%m-%d")
                            except ValueError:
                                continue
                                
                except (ValueError, IndexError):
                    continue
        
        # Default to today if no date found
        return datetime.now().strftime("%Y-%m-%d")
    
    def _extract_items(self, lines: list[str]) -> list[Dict[str, Any]]:
        """Extract purchased items from receipt lines."""
        items = []
        
        for line in lines:
            # Skip header/footer lines
            if any(skip in line.upper() for skip in [
                "TOTAL", "SUBTOTAL", "TAX", "CHANGE", "CASH", "CREDIT",
                "THANK", "WELCOME", "MERCHANT", "DATE", "TIME"
            ]):
                continue
            
            match = re.search(self.ITEM_PATTERN, line)
            if match:
                item_name = match.group(1).strip()
                item_price = float(match.group(2).replace(",", ""))
                
                # Skip if it looks like a total line
                if item_name.upper() in ["TOTAL", "AMOUNT", "BALANCE"]:
                    continue
                
                items.append({
                    "name": item_name,
                    "price": item_price
                })
        
        return items
    
    def _extract_subtotal(self, text: str) -> Optional[float]:
        """Extract subtotal amount."""
        patterns = [
            r"SUB[-\s]?TOTAL[\s:]*\$?([\d,]+\.\d{2})",
            r"SUBTOTAL[\s:]*\$?([\d,]+\.\d{2})",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1).replace(",", ""))
                except ValueError:
                    continue
        return None
    
    def _extract_tax(self, text: str) -> Optional[float]:
        """Extract tax amount."""
        patterns = [
            r"TAX[\s:]*\$?([\d,]+\.\d{2})",
            r"SALES\s+TAX[\s:]*\$?([\d,]+\.\d{2})",
            r"TAX\([\d\.]+%\)[\s:]*\$?([\d,]+\.\d{2})",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1).replace(",", ""))
                except ValueError:
                    continue
        return None
    
    def _detect_category(
        self,
        merchant: Optional[str],
        text: str,
        items: Optional[list]
    ) -> Optional[str]:
        """Auto-detect expense category from receipt content."""
        combined_text = f"{merchant or ''} {text}".lower()
        
        # Check items first (more specific)
        if items:
            item_names = " ".join(item.get("name", "").lower() for item in items)
        else:
            item_names = ""
        
        scores = {}
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in combined_text:
                    score += 2
                if keyword in item_names:
                    score += 3
            if score > 0:
                scores[category] = score
        
        # Return highest scoring category
        if scores:
            return max(scores, key=scores.get)
        
        return "other"
    
    def _calculate_confidence(self, receipt: ParsedReceipt) -> float:
        """Calculate confidence score for parsed receipt."""
        score = 0.0
        checks = 0
        
        if receipt.amount is not None and receipt.amount > 0:
            score += 1.0
        checks += 1
        
        if receipt.merchant and receipt.merchant != "Unknown Merchant":
            score += 1.0
        checks += 1
        
        if receipt.date and receipt.date != datetime.now().strftime("%Y-%m-%d"):
            score += 1.0
        checks += 1
        
        if receipt.items and len(receipt.items) > 0:
            score += 0.5
        checks += 1
        
        return score / checks if checks > 0 else 0.0
    
    def process_image_local(self, image_path: str) -> ParsedReceipt:
        """Process receipt image using local OCR (Tesseract).
        
        Args:
            image_path: Path to receipt image
            
        Returns:
            ParsedReceipt with extracted data
            
        Raises:
            ImportError: If pytesseract is not installed
        """
        try:
            import pytesseract
            from PIL import Image
            
            logger.info(f"Processing image with Tesseract: {image_path}")
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            return self.parse_text(text)
            
        except ImportError:
            logger.error("pytesseract or Pillow not installed. Run: pip install pytesseract Pillow")
            raise
        except Exception as e:
            logger.error(f"Local OCR failed: {e}")
            raise
    
    def validate_receipt(self, receipt: ParsedReceipt) -> Dict[str, Any]:
        """Validate parsed receipt data and return status.
        
        Args:
            receipt: ParsedReceipt to validate
            
        Returns:
            Dictionary with validation results
        """
        issues = []
        
        if receipt.amount is None or receipt.amount <= 0:
            issues.append("Missing or invalid amount")
        
        if not receipt.merchant or receipt.merchant == "Unknown Merchant":
            issues.append("Could not identify merchant")
        
        if not receipt.date:
            issues.append("Missing date (defaulted to today)")
        
        if receipt.confidence < 0.5:
            issues.append("Low confidence extraction - review recommended")
        
        return {
            "valid": len(issues) == 0,
            "confidence": receipt.confidence,
            "issues": issues,
            "needs_review": len(issues) > 0 or receipt.confidence < 0.7
        }
