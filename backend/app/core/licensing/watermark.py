"""
Digital Watermarking System
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

import hashlib
import json
import base64
from typing import Any, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DigitalWatermark:
    def __init__(self, license_info: Dict[str, Any]):
        self.license_info = license_info

    def generate_watermark(self, data: Any) -> str:
        """Generate digital watermark for data"""
        try:
            # Cria metadados do watermark
            watermark_data = {
                "timestamp": datetime.now().isoformat(),
                "license_id": self.license_info.get("license_id"),
                "company": self.license_info.get("company"),
                "user": self.license_info.get("user"),
                "data_hash": self._generate_hash(data)
            }
            
            # Codifica watermark
            encoded = base64.b85encode(
                json.dumps(watermark_data).encode()
            ).decode()
            
            return encoded
            
        except Exception as e:
            logger.error(f"Error generating watermark: {str(e)}")
            return ""

    def verify_watermark(self, data: Any, watermark: str) -> bool:
        """Verify if watermark matches data"""
        try:
            # Decodifica watermark
            decoded = json.loads(
                base64.b85decode(watermark.encode()).decode()
            )
            
            # Verifica hash dos dados
            current_hash = self._generate_hash(data)
            if current_hash != decoded["data_hash"]:
                logger.warning("Data hash mismatch in watermark")
                return False
                
            # Verifica licença
            if decoded["license_id"] != self.license_info.get("license_id"):
                logger.warning("License mismatch in watermark")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error verifying watermark: {str(e)}")
            return False

    def _generate_hash(self, data: Any) -> str:
        """Generate secure hash of data"""
        try:
            if isinstance(data, (dict, list)):
                data = json.dumps(data, sort_keys=True)
            return hashlib.sha256(str(data).encode()).hexdigest()
        except Exception as e:
            logger.error(f"Error generating hash: {str(e)}")
            return ""

class DocumentWatermark:
    def __init__(self, license_info: Dict[str, Any]):
        self.watermarker = DigitalWatermark(license_info)

    def add_watermark_to_pdf(self, pdf_content: bytes, visible: bool = True) -> bytes:
        """Add watermark to PDF document"""
        try:
            from PyPDF2 import PdfReader, PdfWriter
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from io import BytesIO
            import os
            
            # Cria marca d'água visível
            if visible:
                watermark = BytesIO()
                c = canvas.Canvas(watermark, pagesize=letter)
                c.setFillColorRGB(0.5, 0.5, 0.5, 0.1)  # Cinza transparente
                c.setFont("Helvetica", 60)
                c.rotate(45)
                text = f"Licensed to: {self.watermarker.license_info.get('company')}"
                c.drawString(100, 100, text)
                c.save()
                
                watermark = PdfReader(BytesIO(watermark.getvalue()))
                
            # Processa PDF
            pdf = PdfReader(BytesIO(pdf_content))
            output = PdfWriter()
            
            # Adiciona marca d'água em cada página
            for page in pdf.pages:
                if visible:
                    page.merge_page(watermark.pages[0])
                    
                # Adiciona watermark digital
                if "/Metadata" not in page:
                    page["/Metadata"] = {}
                page["/Metadata"]["/Watermark"] = self.watermarker.generate_watermark(
                    pdf_content
                )
                output.add_page(page)
                
            # Gera PDF final
            result = BytesIO()
            output.write(result)
            return result.getvalue()
            
        except Exception as e:
            logger.error(f"Error adding watermark to PDF: {str(e)}")
            return pdf_content

    def verify_pdf_watermark(self, pdf_content: bytes) -> bool:
        """Verify PDF document watermark"""
        try:
            from PyPDF2 import PdfReader
            from io import BytesIO
            
            pdf = PdfReader(BytesIO(pdf_content))
            
            # Verifica watermark em cada página
            for page in pdf.pages:
                if "/Metadata" not in page or "/Watermark" not in page["/Metadata"]:
                    logger.warning("No watermark found in PDF")
                    return False
                    
                watermark = page["/Metadata"]["/Watermark"]
                if not self.watermarker.verify_watermark(pdf_content, watermark):
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error verifying PDF watermark: {str(e)}")
            return False
