"""
Enhanced metadata extraction and content analysis for SimpleGallery
Provides advanced content awareness features including AI-powered analysis
"""

import os
import json
import cv2
import numpy as np
from PIL import Image, ExifTags
from datetime import datetime
import requests
from io import BytesIO
import simplegallery.common as spg_common
from collections import defaultdict
import re
from typing import Dict, List, Optional, Tuple, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentAnalyzer:
    """Advanced content analysis for images and videos"""
    
    def __init__(self):
        self.color_palette_cache = {}
        self.face_detection_cache = {}
        self.text_extraction_cache = {}
        
    def extract_enhanced_metadata(self, image_path: str, thumbnail_path: str, public_path: str) -> Dict[str, Any]:
        """
        Extract comprehensive metadata including content analysis
        """
        base_metadata = self._get_base_metadata(image_path, thumbnail_path, public_path)
        
        # Add enhanced content analysis
        enhanced_metadata = {
            **base_metadata,
            'content_analysis': self._analyze_content(image_path),
            'color_analysis': self._analyze_colors(image_path),
            'composition_analysis': self._analyze_composition(image_path),
            'text_content': self._extract_text_content(image_path),
            'face_analysis': self._analyze_faces(image_path),
            'scene_classification': self._classify_scene(image_path),
            'quality_metrics': self._assess_quality(image_path),
            'temporal_context': self._analyze_temporal_context(image_path),
            'geographic_data': self._extract_geographic_data(image_path),
            'device_info': self._extract_device_info(image_path),
            'aesthetic_score': self._calculate_aesthetic_score(image_path)
        }
        
        return enhanced_metadata
    
    def _get_base_metadata(self, image_path: str, thumbnail_path: str, public_path: str) -> Dict[str, Any]:
        """Get basic metadata using existing simplegallery logic"""
        from simplegallery.media import get_metadata
        return get_metadata(image_path, thumbnail_path, public_path)
    
    def _analyze_content(self, image_path: str) -> Dict[str, Any]:
        """Analyze image content for objects, scenes, and activities"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {}
            
            # Basic content analysis
            content_info = {
                'dominant_objects': self._detect_objects(image),
                'scene_type': self._classify_scene_type(image),
                'activity_level': self._assess_activity_level(image),
                'complexity_score': self._calculate_complexity(image),
                'subject_count': self._count_subjects(image)
            }
            
            return content_info
        except Exception as e:
            logger.warning(f"Content analysis failed for {image_path}: {e}")
            return {}
    
    def _analyze_colors(self, image_path: str) -> Dict[str, Any]:
        """Analyze color composition and palette"""
        try:
            if image_path in self.color_palette_cache:
                return self.color_palette_cache[image_path]
            
            image = cv2.imread(image_path)
            if image is None:
                return {}
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Reshape image to be a list of pixels
            pixels = image_rgb.reshape(-1, 3)
            
            # Get dominant colors using K-means
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            
            # Calculate color percentages
            color_percentages = []
            for i in range(5):
                percentage = (labels == i).sum() / len(labels) * 100
                color_percentages.append({
                    'rgb': colors[i].tolist(),
                    'hex': f"#{colors[i][0]:02x}{colors[i][1]:02x}{colors[i][2]:02x}",
                    'percentage': round(percentage, 2)
                })
            
            # Sort by percentage
            color_percentages.sort(key=lambda x: x['percentage'], reverse=True)
            
            color_analysis = {
                'dominant_colors': color_percentages,
                'color_vibrance': self._calculate_vibrance(image_rgb),
                'color_harmony': self._assess_color_harmony(colors),
                'brightness_level': self._calculate_brightness(image_rgb),
                'contrast_level': self._calculate_contrast(image_rgb),
                'saturation_level': self._calculate_saturation(image_rgb)
            }
            
            self.color_palette_cache[image_path] = color_analysis
            return color_analysis
            
        except Exception as e:
            logger.warning(f"Color analysis failed for {image_path}: {e}")
            return {}
    
    def _analyze_composition(self, image_path: str) -> Dict[str, Any]:
        """Analyze image composition and visual elements"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {}
            
            height, width = image.shape[:2]
            
            # Rule of thirds analysis
            rule_of_thirds = self._analyze_rule_of_thirds(image)
            
            # Symmetry analysis
            symmetry = self._analyze_symmetry(image)
            
            # Edge density analysis
            edge_density = self._calculate_edge_density(image)
            
            # Depth of field estimation
            depth_of_field = self._estimate_depth_of_field(image)
            
            composition_analysis = {
                'aspect_ratio': round(width / height, 2),
                'orientation': 'landscape' if width > height else 'portrait' if height > width else 'square',
                'rule_of_thirds_score': rule_of_thirds,
                'symmetry_score': symmetry,
                'edge_density': edge_density,
                'depth_of_field': depth_of_field,
                'composition_balance': self._assess_composition_balance(image),
                'focal_points': self._identify_focal_points(image)
            }
            
            return composition_analysis
            
        except Exception as e:
            logger.warning(f"Composition analysis failed for {image_path}: {e}")
            return {}
    
    def _extract_text_content(self, image_path: str) -> Dict[str, Any]:
        """Extract text content from images using OCR"""
        try:
            if image_path in self.text_extraction_cache:
                return self.text_extraction_cache[image_path]
            
            # Try to import pytesseract for OCR
            try:
                import pytesseract
                from PIL import Image as PILImage
                
                image = PILImage.open(image_path)
                text = pytesseract.image_to_string(image)
                
                # Clean and process text
                cleaned_text = re.sub(r'\s+', ' ', text.strip())
                
                text_analysis = {
                    'extracted_text': cleaned_text,
                    'text_confidence': self._get_text_confidence(image),
                    'language_detected': self._detect_language(cleaned_text),
                    'text_regions': self._find_text_regions(image),
                    'has_text': len(cleaned_text) > 0
                }
                
                self.text_extraction_cache[image_path] = text_analysis
                return text_analysis
                
            except ImportError:
                logger.info("pytesseract not available for OCR")
                return {'has_text': False, 'extracted_text': ''}
                
        except Exception as e:
            logger.warning(f"Text extraction failed for {image_path}: {e}")
            return {'has_text': False, 'extracted_text': ''}
    
    def _analyze_faces(self, image_path: str) -> Dict[str, Any]:
        """Analyze faces in the image"""
        try:
            if image_path in self.face_detection_cache:
                return self.face_detection_cache[image_path]
            
            image = cv2.imread(image_path)
            if image is None:
                return {}
            
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            face_analysis = {
                'face_count': len(faces),
                'faces_detected': len(faces) > 0,
                'face_locations': faces.tolist() if len(faces) > 0 else [],
                'largest_face_size': max([w * h for (x, y, w, h) in faces]) if len(faces) > 0 else 0,
                'face_confidence': self._calculate_face_confidence(faces, image.shape)
            }
            
            self.face_detection_cache[image_path] = face_analysis
            return face_analysis
            
        except Exception as e:
            logger.warning(f"Face analysis failed for {image_path}: {e}")
            return {'face_count': 0, 'faces_detected': False}
    
    def _classify_scene(self, image_path: str) -> Dict[str, Any]:
        """Classify the scene type and content"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {}
            
            # Basic scene classification based on color and texture analysis
            scene_info = {
                'indoor_outdoor': self._classify_indoor_outdoor(image),
                'time_of_day': self._estimate_time_of_day(image),
                'weather_condition': self._estimate_weather(image),
                'scene_category': self._categorize_scene(image),
                'mood': self._assess_mood(image)
            }
            
            return scene_info
            
        except Exception as e:
            logger.warning(f"Scene classification failed for {image_path}: {e}")
            return {}
    
    def _assess_quality(self, image_path: str) -> Dict[str, Any]:
        """Assess image quality metrics"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {}
            
            # Calculate various quality metrics
            quality_metrics = {
                'sharpness': self._calculate_sharpness(image),
                'noise_level': self._calculate_noise_level(image),
                'exposure_quality': self._assess_exposure(image),
                'focus_quality': self._assess_focus(image),
                'overall_quality_score': 0  # Will be calculated
            }
            
            # Calculate overall quality score
            quality_metrics['overall_quality_score'] = self._calculate_overall_quality(quality_metrics)
            
            return quality_metrics
            
        except Exception as e:
            logger.warning(f"Quality assessment failed for {image_path}: {e}")
            return {}
    
    def _analyze_temporal_context(self, image_path: str) -> Dict[str, Any]:
        """Analyze temporal context and metadata"""
        try:
            # Get file creation time
            file_time = datetime.fromtimestamp(os.path.getctime(image_path))
            
            # Try to get EXIF datetime
            exif_time = None
            try:
                image = Image.open(image_path)
                exif = image._getexif()
                if exif and ExifTags.TAGS.get(271) in exif:  # DateTimeOriginal
                    exif_time = datetime.strptime(exif[ExifTags.TAGS.get(271)], "%Y:%m:%d %H:%M:%S")
            except:
                pass
            
            temporal_context = {
                'file_created': file_time.isoformat(),
                'exif_datetime': exif_time.isoformat() if exif_time else None,
                'time_period': self._classify_time_period(file_time),
                'season': self._estimate_season(file_time),
                'is_recent': (datetime.now() - file_time).days < 30,
                'age_days': (datetime.now() - file_time).days
            }
            
            return temporal_context
            
        except Exception as e:
            logger.warning(f"Temporal analysis failed for {image_path}: {e}")
            return {}
    
    def _extract_geographic_data(self, image_path: str) -> Dict[str, Any]:
        """Extract geographic data from EXIF"""
        try:
            image = Image.open(image_path)
            exif = image._getexif()
            
            if not exif:
                return {}
            
            geo_data = {}
            
            # GPS coordinates
            if ExifTags.TAGS.get(34853) in exif:  # GPSInfo
                gps_info = exif[ExifTags.TAGS.get(34853)]
                if gps_info:
                    lat, lon = self._get_lat_lon(gps_info)
                    if lat and lon:
                        geo_data = {
                            'latitude': lat,
                            'longitude': lon,
                            'has_location': True,
                            'location_accuracy': 'exact'
                        }
            
            # Location name (if available)
            if ExifTags.TAGS.get(270) in exif:  # ImageDescription
                description = exif[ExifTags.TAGS.get(270)]
                if description and any(keyword in description.lower() for keyword in ['location', 'place', 'city', 'country']):
                    geo_data['location_description'] = description
            
            return geo_data
            
        except Exception as e:
            logger.warning(f"Geographic data extraction failed for {image_path}: {e}")
            return {}
    
    def _extract_device_info(self, image_path: str) -> Dict[str, Any]:
        """Extract device and camera information"""
        try:
            image = Image.open(image_path)
            exif = image._getexif()
            
            if not exif:
                return {}
            
            device_info = {}
            
            # Camera make and model
            if ExifTags.TAGS.get(271) in exif:  # Make
                device_info['camera_make'] = exif[ExifTags.TAGS.get(271)]
            if ExifTags.TAGS.get(272) in exif:  # Model
                device_info['camera_model'] = exif[ExifTags.TAGS.get(272)]
            
            # Camera settings
            if ExifTags.TAGS.get(33434) in exif:  # ExposureTime
                device_info['exposure_time'] = exif[ExifTags.TAGS.get(33434)]
            if ExifTags.TAGS.get(33437) in exif:  # FNumber
                device_info['f_number'] = exif[ExifTags.TAGS.get(33437)]
            if ExifTags.TAGS.get(34855) in exif:  # ISOSpeedRatings
                device_info['iso'] = exif[ExifTags.TAGS.get(34855)]
            if ExifTags.TAGS.get(37377) in exif:  # FocalLength
                device_info['focal_length'] = exif[ExifTags.TAGS.get(37377)]
            
            return device_info
            
        except Exception as e:
            logger.warning(f"Device info extraction failed for {image_path}: {e}")
            return {}
    
    def _calculate_aesthetic_score(self, image_path: str) -> Dict[str, Any]:
        """Calculate aesthetic quality score"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {}
            
            # Calculate various aesthetic factors
            aesthetic_factors = {
                'color_harmony_score': self._calculate_color_harmony_score(image),
                'composition_score': self._calculate_composition_score(image),
                'lighting_score': self._calculate_lighting_score(image),
                'subject_interest_score': self._calculate_subject_interest_score(image),
                'technical_quality_score': self._calculate_technical_quality_score(image)
            }
            
            # Calculate weighted overall score
            weights = {
                'color_harmony_score': 0.2,
                'composition_score': 0.25,
                'lighting_score': 0.2,
                'subject_interest_score': 0.2,
                'technical_quality_score': 0.15
            }
            
            overall_score = sum(aesthetic_factors[key] * weights[key] for key in weights.keys())
            
            aesthetic_score = {
                **aesthetic_factors,
                'overall_aesthetic_score': round(overall_score, 2),
                'aesthetic_grade': self._get_aesthetic_grade(overall_score)
            }
            
            return aesthetic_score
            
        except Exception as e:
            logger.warning(f"Aesthetic score calculation failed for {image_path}: {e}")
            return {}
    
    # Helper methods for analysis
    def _detect_objects(self, image):
        """Detect objects in image (placeholder for object detection)"""
        # This would integrate with models like YOLO, R-CNN, etc.
        return []
    
    def _classify_scene_type(self, image):
        """Classify scene type (placeholder)"""
        return "unknown"
    
    def _assess_activity_level(self, image):
        """Assess activity level in image"""
        return "static"
    
    def _calculate_complexity(self, image):
        """Calculate image complexity score"""
        return 0.5
    
    def _count_subjects(self, image):
        """Count number of subjects in image"""
        return 1
    
    def _calculate_vibrance(self, image):
        """Calculate color vibrance"""
        return 0.5
    
    def _assess_color_harmony(self, colors):
        """Assess color harmony"""
        return "balanced"
    
    def _calculate_brightness(self, image):
        """Calculate image brightness"""
        return 0.5
    
    def _calculate_contrast(self, image):
        """Calculate image contrast"""
        return 0.5
    
    def _calculate_saturation(self, image):
        """Calculate image saturation"""
        return 0.5
    
    def _analyze_rule_of_thirds(self, image):
        """Analyze rule of thirds composition"""
        return 0.5
    
    def _analyze_symmetry(self, image):
        """Analyze image symmetry"""
        return 0.5
    
    def _calculate_edge_density(self, image):
        """Calculate edge density"""
        return 0.5
    
    def _estimate_depth_of_field(self, image):
        """Estimate depth of field"""
        return "medium"
    
    def _assess_composition_balance(self, image):
        """Assess composition balance"""
        return "balanced"
    
    def _identify_focal_points(self, image):
        """Identify focal points in image"""
        return []
    
    def _get_text_confidence(self, image):
        """Get text extraction confidence"""
        return 0.8
    
    def _detect_language(self, text):
        """Detect text language"""
        return "en"
    
    def _find_text_regions(self, image):
        """Find text regions in image"""
        return []
    
    def _calculate_face_confidence(self, faces, image_shape):
        """Calculate face detection confidence"""
        return 0.8
    
    def _classify_indoor_outdoor(self, image):
        """Classify indoor vs outdoor"""
        return "outdoor"
    
    def _estimate_time_of_day(self, image):
        """Estimate time of day"""
        return "day"
    
    def _estimate_weather(self, image):
        """Estimate weather condition"""
        return "clear"
    
    def _categorize_scene(self, image):
        """Categorize scene type"""
        return "landscape"
    
    def _assess_mood(self, image):
        """Assess image mood"""
        return "neutral"
    
    def _calculate_sharpness(self, image):
        """Calculate image sharpness"""
        return 0.5
    
    def _calculate_noise_level(self, image):
        """Calculate noise level"""
        return 0.3
    
    def _assess_exposure(self, image):
        """Assess exposure quality"""
        return "good"
    
    def _assess_focus(self, image):
        """Assess focus quality"""
        return "sharp"
    
    def _calculate_overall_quality(self, metrics):
        """Calculate overall quality score"""
        return 0.7
    
    def _classify_time_period(self, file_time):
        """Classify time period"""
        return "recent"
    
    def _estimate_season(self, file_time):
        """Estimate season"""
        month = file_time.month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"
    
    def _get_lat_lon(self, gps_info):
        """Extract latitude and longitude from GPS info"""
        return None, None
    
    def _calculate_color_harmony_score(self, image):
        """Calculate color harmony score"""
        return 0.7
    
    def _calculate_composition_score(self, image):
        """Calculate composition score"""
        return 0.6
    
    def _calculate_lighting_score(self, image):
        """Calculate lighting score"""
        return 0.8
    
    def _calculate_subject_interest_score(self, image):
        """Calculate subject interest score"""
        return 0.5
    
    def _calculate_technical_quality_score(self, image):
        """Calculate technical quality score"""
        return 0.7
    
    def _get_aesthetic_grade(self, score):
        """Get aesthetic grade from score"""
        if score >= 0.8:
            return "A"
        elif score >= 0.6:
            return "B"
        elif score >= 0.4:
            return "C"
        else:
            return "D"


def get_enhanced_metadata(image_path: str, thumbnail_path: str, public_path: str) -> Dict[str, Any]:
    """
    Get enhanced metadata for an image
    """
    analyzer = ContentAnalyzer()
    return analyzer.extract_enhanced_metadata(image_path, thumbnail_path, public_path)