"""
Image optimization utilities for avatar uploads
"""
from PIL import Image
from pathlib import Path
from typing import Tuple
import io


class ImageOptimizer:
    """Optimize and resize images"""
    
    MAX_SIZE = (800, 800)  # Maximum dimensions
    THUMBNAIL_SIZE = (200, 200)  # Thumbnail dimensions
    QUALITY = 85  # JPEG quality
    ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}
    
    @staticmethod
    def optimize_image(
        image_bytes: bytes,
        max_size: Tuple[int, int] = MAX_SIZE,
        quality: int = QUALITY,
        convert_to_webp: bool = True
    ) -> Tuple[bytes, str]:
        """
        Optimize image by resizing and converting to WebP
        
        Args:
            image_bytes: Original image bytes
            max_size: Maximum dimensions (width, height)
            quality: Image quality (1-100)
            convert_to_webp: Convert to WebP format
            
        Returns:
            Tuple of (optimized_bytes, format)
        """
        # Open image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB if saving as JPEG
        if img.mode == 'RGBA' and not convert_to_webp:
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        # Resize if larger than max_size
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = io.BytesIO()
        
        if convert_to_webp:
            img.save(output, format='WEBP', quality=quality)
            format_str = 'webp'
        else:
            format_str = 'jpeg' if img.format == 'JPEG' else 'png'
            img.save(output, format=format_str.upper(), quality=quality)
        
        output.seek(0)
        return output.read(), format_str
    
    @staticmethod
    def create_thumbnail(
        image_bytes: bytes,
        size: Tuple[int, int] = THUMBNAIL_SIZE
    ) -> bytes:
        """
        Create thumbnail from image
        
        Args:
            image_bytes: Original image bytes
            size: Thumbnail dimensions
            
        Returns:
            Thumbnail image bytes
        """
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        # Create thumbnail
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = io.BytesIO()
        img.save(output, format='WEBP', quality=85)
        output.seek(0)
        
        return output.read()
    
    @staticmethod
    def validate_image(image_bytes: bytes) -> bool:
        """
        Validate if bytes represent a valid image
        
        Args:
            image_bytes: Image bytes to validate
            
        Returns:
            True if valid image, False otherwise
        """
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()
            return img.format in ImageOptimizer.ALLOWED_FORMATS
        except Exception:
            return False
    
    @staticmethod
    def get_image_info(image_bytes: bytes) -> dict:
        """
        Get image information
        
        Args:
            image_bytes: Image bytes
            
        Returns:
            Dictionary with image info
        """
        img = Image.open(io.BytesIO(image_bytes))
        return {
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height
        }
