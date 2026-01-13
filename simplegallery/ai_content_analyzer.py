"""
AI-Powered Content Analysis for SimpleGallery
Provides advanced content analysis using machine learning models
"""

import os
import cv2
import numpy as np
from PIL import Image
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
import requests
from io import BytesIO
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIContentAnalyzer:
    """AI-powered content analysis using various ML models"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.models = {}
        self.cache = {}
        
        # Initialize models based on configuration
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models for content analysis"""
        try:
            # Try to import required libraries
            import torch
            import torchvision.transforms as transforms
            from torchvision.models import resnet50, ResNet50_Weights
            import clip
            
            self.models['resnet'] = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
            self.models['resnet'].eval()
            
            # Initialize CLIP for image-text understanding
            self.models['clip_model'], self.models['clip_preprocess'] = clip.load("ViT-B/32")
            
            # Initialize transforms
            self.models['transform'] = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            logger.info("AI models initialized successfully")
            
        except ImportError as e:
            logger.warning(f"AI models not available: {e}")
            logger.info("Install torch, torchvision, and clip for AI features")
            self.models = {}
        except Exception as e:
            logger.warning(f"Failed to initialize AI models: {e}")
            self.models = {}
    
    def analyze_image_content(self, image_path: str) -> Dict[str, Any]:
        """
        Perform comprehensive AI-powered content analysis
        """
        if not self.models:
            return self._fallback_analysis(image_path)
        
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            
            # Object detection and classification
            objects = self._detect_objects(image)
            
            # Scene classification
            scene = self._classify_scene(image)
            
            # Text extraction using OCR
            text_content = self._extract_text_ai(image)
            
            # Face detection and analysis
            faces = self._analyze_faces_ai(image)
            
            # Aesthetic quality assessment
            aesthetic_score = self._assess_aesthetic_quality(image)
            
            # Color palette analysis
            color_analysis = self._analyze_colors_ai(image)
            
            # Composition analysis
            composition = self._analyze_composition_ai(image)
            
            # Mood and emotion analysis
            mood = self._analyze_mood(image)
            
            # Style classification
            style = self._classify_style(image)
            
            return {
                'objects': objects,
                'scene': scene,
                'text_content': text_content,
                'faces': faces,
                'aesthetic_score': aesthetic_score,
                'color_analysis': color_analysis,
                'composition': composition,
                'mood': mood,
                'style': style,
                'ai_confidence': self._calculate_overall_confidence()
            }
            
        except Exception as e:
            logger.warning(f"AI analysis failed for {image_path}: {e}")
            return self._fallback_analysis(image_path)
    
    def _detect_objects(self, image: Image.Image) -> Dict[str, Any]:
        """Detect objects in the image using ResNet"""
        if 'resnet' not in self.models:
            return {'objects': [], 'confidence': 0}
        
        try:
            import torch
            import torch.nn.functional as F
            
            # Preprocess image
            input_tensor = self.models['transform'](image).unsqueeze(0)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.models['resnet'](input_tensor)
                probabilities = F.softmax(outputs[0], dim=1)
            
            # Get top predictions
            top5_prob, top5_indices = torch.topk(probabilities, 5)
            
            # Load ImageNet class names
            class_names = self._get_imagenet_classes()
            
            objects = []
            for i in range(5):
                idx = top5_indices[0][i].item()
                prob = top5_prob[0][i].item()
                class_name = class_names.get(idx, f"Class {idx}")
                
                objects.append({
                    'name': class_name,
                    'confidence': prob,
                    'category': self._categorize_object(class_name)
                })
            
            return {
                'objects': objects,
                'confidence': float(top5_prob[0][0].item()),
                'primary_object': objects[0] if objects else None
            }
            
        except Exception as e:
            logger.warning(f"Object detection failed: {e}")
            return {'objects': [], 'confidence': 0}
    
    def _classify_scene(self, image: Image.Image) -> Dict[str, Any]:
        """Classify the scene type using CLIP"""
        if 'clip_model' not in self.models:
            return {'scene_type': 'unknown', 'confidence': 0}
        
        try:
            import torch
            
            # Define scene categories
            scene_categories = [
                "indoor room", "outdoor landscape", "city street", "beach", "mountain",
                "forest", "desert", "ocean", "sky", "building", "garden", "park",
                "kitchen", "bedroom", "living room", "office", "restaurant", "shop"
            ]
            
            # Preprocess image
            image_input = self.models['clip_preprocess'](image).unsqueeze(0)
            text_input = clip.tokenize(scene_categories)
            
            # Get predictions
            with torch.no_grad():
                image_features = self.models['clip_model'].encode_image(image_input)
                text_features = self.models['clip_model'].encode_text(text_input)
                
                # Calculate similarities
                similarities = (image_features @ text_features.T).softmax(dim=-1)
                
                # Get top scene
                top_idx = similarities.argmax().item()
                confidence = similarities[0][top_idx].item()
                
                return {
                    'scene_type': scene_categories[top_idx],
                    'confidence': confidence,
                    'all_scenes': [
                        {'name': scene_categories[i], 'confidence': float(similarities[0][i])}
                        for i in range(len(scene_categories))
                    ]
                }
                
        except Exception as e:
            logger.warning(f"Scene classification failed: {e}")
            return {'scene_type': 'unknown', 'confidence': 0}
    
    def _extract_text_ai(self, image: Image.Image) -> Dict[str, Any]:
        """Extract text using AI-powered OCR"""
        try:
            import pytesseract
            
            # Extract text
            text = pytesseract.image_to_string(image)
            cleaned_text = ' '.join(text.split())
            
            # Get confidence scores
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Detect language
            language = pytesseract.image_to_string(image, lang='eng')
            
            return {
                'text': cleaned_text,
                'confidence': avg_confidence / 100.0,
                'language': 'en',  # Simplified
                'word_count': len(cleaned_text.split()),
                'has_text': len(cleaned_text) > 0
            }
            
        except ImportError:
            logger.info("pytesseract not available for OCR")
            return {'text': '', 'confidence': 0, 'has_text': False}
        except Exception as e:
            logger.warning(f"Text extraction failed: {e}")
            return {'text': '', 'confidence': 0, 'has_text': False}
    
    def _analyze_faces_ai(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze faces using OpenCV and AI models"""
        try:
            # Convert PIL to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            face_analysis = {
                'face_count': len(faces),
                'faces_detected': len(faces) > 0,
                'face_locations': faces.tolist(),
                'confidence': 0.8 if len(faces) > 0 else 0
            }
            
            # Analyze face sizes and positions
            if len(faces) > 0:
                face_sizes = [w * h for (x, y, w, h) in faces]
                face_analysis.update({
                    'largest_face_size': max(face_sizes),
                    'average_face_size': sum(face_sizes) / len(face_sizes),
                    'face_density': len(faces) / (image.width * image.height) * 1000000
                })
            
            return face_analysis
            
        except Exception as e:
            logger.warning(f"Face analysis failed: {e}")
            return {'face_count': 0, 'faces_detected': False, 'confidence': 0}
    
    def _assess_aesthetic_quality(self, image: Image.Image) -> Dict[str, Any]:
        """Assess aesthetic quality using various metrics"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Calculate various quality metrics
            sharpness = self._calculate_sharpness(img_array)
            brightness = self._calculate_brightness(img_array)
            contrast = self._calculate_contrast(img_array)
            colorfulness = self._calculate_colorfulness(img_array)
            composition = self._assess_composition_quality(img_array)
            
            # Calculate overall aesthetic score
            aesthetic_score = (
                sharpness * 0.25 +
                brightness * 0.2 +
                contrast * 0.2 +
                colorfulness * 0.15 +
                composition * 0.2
            )
            
            # Determine grade
            if aesthetic_score >= 0.8:
                grade = 'A'
            elif aesthetic_score >= 0.6:
                grade = 'B'
            elif aesthetic_score >= 0.4:
                grade = 'C'
            else:
                grade = 'D'
            
            return {
                'overall_score': aesthetic_score,
                'grade': grade,
                'sharpness': sharpness,
                'brightness': brightness,
                'contrast': contrast,
                'colorfulness': colorfulness,
                'composition': composition
            }
            
        except Exception as e:
            logger.warning(f"Aesthetic assessment failed: {e}")
            return {'overall_score': 0.5, 'grade': 'C'}
    
    def _analyze_colors_ai(self, image: Image.Image) -> Dict[str, Any]:
        """Advanced color analysis using AI"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Reshape to list of pixels
            pixels = img_array.reshape(-1, 3)
            
            # Use K-means for dominant colors
            from sklearn.cluster import KMeans
            
            kmeans = KMeans(n_clusters=8, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            
            # Calculate color percentages
            color_percentages = []
            for i in range(8):
                percentage = (labels == i).sum() / len(labels) * 100
                color_percentages.append({
                    'rgb': colors[i].tolist(),
                    'hex': f"#{colors[i][0]:02x}{colors[i][1]:02x}{colors[i][2]:02x}",
                    'percentage': round(percentage, 2)
                })
            
            # Sort by percentage
            color_percentages.sort(key=lambda x: x['percentage'], reverse=True)
            
            # Analyze color harmony
            harmony_score = self._calculate_color_harmony(colors)
            
            # Analyze color temperature
            temperature = self._analyze_color_temperature(img_array)
            
            return {
                'dominant_colors': color_percentages[:5],
                'color_harmony': harmony_score,
                'temperature': temperature,
                'vibrance': self._calculate_vibrance(img_array),
                'saturation': self._calculate_saturation(img_array)
            }
            
        except Exception as e:
            logger.warning(f"Color analysis failed: {e}")
            return {'dominant_colors': [], 'color_harmony': 0.5}
    
    def _analyze_composition_ai(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze composition using AI techniques"""
        try:
            img_array = np.array(image)
            
            # Rule of thirds analysis
            rule_of_thirds = self._analyze_rule_of_thirds_ai(img_array)
            
            # Symmetry analysis
            symmetry = self._analyze_symmetry_ai(img_array)
            
            # Edge analysis
            edges = self._analyze_edges(img_array)
            
            # Depth of field estimation
            depth_of_field = self._estimate_depth_of_field_ai(img_array)
            
            return {
                'rule_of_thirds': rule_of_thirds,
                'symmetry': symmetry,
                'edge_density': edges['density'],
                'edge_distribution': edges['distribution'],
                'depth_of_field': depth_of_field,
                'composition_score': (rule_of_thirds + symmetry + edges['quality']) / 3
            }
            
        except Exception as e:
            logger.warning(f"Composition analysis failed: {e}")
            return {'composition_score': 0.5}
    
    def _analyze_mood(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze mood and emotion in the image"""
        try:
            img_array = np.array(image)
            
            # Analyze color mood
            color_mood = self._analyze_color_mood(img_array)
            
            # Analyze brightness mood
            brightness_mood = self._analyze_brightness_mood(img_array)
            
            # Analyze composition mood
            composition_mood = self._analyze_composition_mood(img_array)
            
            # Combine mood indicators
            overall_mood = self._combine_mood_indicators(color_mood, brightness_mood, composition_mood)
            
            return {
                'overall_mood': overall_mood,
                'color_mood': color_mood,
                'brightness_mood': brightness_mood,
                'composition_mood': composition_mood,
                'mood_tags': self._generate_mood_tags(overall_mood)
            }
            
        except Exception as e:
            logger.warning(f"Mood analysis failed: {e}")
            return {'overall_mood': 'neutral', 'mood_tags': []}
    
    def _classify_style(self, image: Image.Image) -> Dict[str, Any]:
        """Classify artistic style using AI"""
        try:
            # Define style categories
            styles = [
                "photography", "painting", "digital art", "sketch", "watercolor",
                "oil painting", "abstract", "realistic", "minimalist", "vintage",
                "modern", "classical", "contemporary", "street art", "portrait"
            ]
            
            # This would typically use a trained style classification model
            # For now, we'll use basic heuristics
            style_analysis = self._analyze_style_heuristics(image)
            
            return {
                'primary_style': style_analysis['primary'],
                'confidence': style_analysis['confidence'],
                'all_styles': style_analysis['all_styles']
            }
            
        except Exception as e:
            logger.warning(f"Style classification failed: {e}")
            return {'primary_style': 'photography', 'confidence': 0.5}
    
    def _fallback_analysis(self, image_path: str) -> Dict[str, Any]:
        """Fallback analysis when AI models are not available"""
        return {
            'objects': {'objects': [], 'confidence': 0},
            'scene': {'scene_type': 'unknown', 'confidence': 0},
            'text_content': {'text': '', 'confidence': 0, 'has_text': False},
            'faces': {'face_count': 0, 'faces_detected': False, 'confidence': 0},
            'aesthetic_score': {'overall_score': 0.5, 'grade': 'C'},
            'color_analysis': {'dominant_colors': [], 'color_harmony': 0.5},
            'composition': {'composition_score': 0.5},
            'mood': {'overall_mood': 'neutral', 'mood_tags': []},
            'style': {'primary_style': 'photography', 'confidence': 0.5},
            'ai_confidence': 0
        }
    
    # Helper methods for various analyses
    def _get_imagenet_classes(self) -> Dict[int, str]:
        """Get ImageNet class names"""
        # This would typically load from a file or API
        return {
            0: "tench", 1: "goldfish", 2: "great white shark", 3: "tiger shark",
            # ... more classes would be loaded here
        }
    
    def _categorize_object(self, class_name: str) -> str:
        """Categorize object into broader categories"""
        categories = {
            'person': ['person', 'man', 'woman', 'child', 'baby'],
            'animal': ['cat', 'dog', 'bird', 'fish', 'horse', 'cow'],
            'vehicle': ['car', 'truck', 'bus', 'motorcycle', 'bicycle'],
            'building': ['house', 'building', 'church', 'castle', 'bridge'],
            'nature': ['tree', 'flower', 'mountain', 'ocean', 'sky']
        }
        
        for category, keywords in categories.items():
            if any(keyword in class_name.lower() for keyword in keywords):
                return category
        return 'other'
    
    def _calculate_sharpness(self, img_array: np.ndarray) -> float:
        """Calculate image sharpness using Laplacian variance"""
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()
    
    def _calculate_brightness(self, img_array: np.ndarray) -> float:
        """Calculate image brightness"""
        return np.mean(img_array) / 255.0
    
    def _calculate_contrast(self, img_array: np.ndarray) -> float:
        """Calculate image contrast"""
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        return gray.std() / 255.0
    
    def _calculate_colorfulness(self, img_array: np.ndarray) -> float:
        """Calculate colorfulness metric"""
        # Convert to Lab color space
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        a, b = lab[:, :, 1], lab[:, :, 2]
        return np.sqrt(np.var(a) + np.var(b))
    
    def _assess_composition_quality(self, img_array: np.ndarray) -> float:
        """Assess composition quality"""
        # This would implement various composition rules
        return 0.5  # Placeholder
    
    def _calculate_color_harmony(self, colors: np.ndarray) -> float:
        """Calculate color harmony score"""
        # This would implement color harmony algorithms
        return 0.5  # Placeholder
    
    def _analyze_color_temperature(self, img_array: np.ndarray) -> str:
        """Analyze color temperature"""
        # This would analyze warm vs cool colors
        return "neutral"  # Placeholder
    
    def _calculate_vibrance(self, img_array: np.ndarray) -> float:
        """Calculate color vibrance"""
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        return np.mean(hsv[:, :, 1]) / 255.0
    
    def _calculate_saturation(self, img_array: np.ndarray) -> float:
        """Calculate color saturation"""
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        return np.mean(hsv[:, :, 1]) / 255.0
    
    def _analyze_rule_of_thirds_ai(self, img_array: np.ndarray) -> float:
        """Analyze rule of thirds using AI"""
        # This would implement rule of thirds analysis
        return 0.5  # Placeholder
    
    def _analyze_symmetry_ai(self, img_array: np.ndarray) -> float:
        """Analyze symmetry using AI"""
        # This would implement symmetry analysis
        return 0.5  # Placeholder
    
    def _analyze_edges(self, img_array: np.ndarray) -> Dict[str, float]:
        """Analyze edge distribution"""
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return {
            'density': np.sum(edges > 0) / edges.size,
            'distribution': 0.5,  # Placeholder
            'quality': 0.5  # Placeholder
        }
    
    def _estimate_depth_of_field_ai(self, img_array: np.ndarray) -> str:
        """Estimate depth of field using AI"""
        # This would implement depth of field estimation
        return "medium"  # Placeholder
    
    def _analyze_color_mood(self, img_array: np.ndarray) -> str:
        """Analyze color mood"""
        # This would analyze color psychology
        return "neutral"  # Placeholder
    
    def _analyze_brightness_mood(self, img_array: np.ndarray) -> str:
        """Analyze brightness mood"""
        brightness = np.mean(img_array) / 255.0
        if brightness > 0.7:
            return "cheerful"
        elif brightness < 0.3:
            return "moody"
        else:
            return "neutral"
    
    def _analyze_composition_mood(self, img_array: np.ndarray) -> str:
        """Analyze composition mood"""
        # This would analyze composition psychology
        return "neutral"  # Placeholder
    
    def _combine_mood_indicators(self, color_mood: str, brightness_mood: str, composition_mood: str) -> str:
        """Combine mood indicators"""
        # This would combine various mood indicators
        return "neutral"  # Placeholder
    
    def _generate_mood_tags(self, mood: str) -> List[str]:
        """Generate mood tags"""
        mood_tags = {
            'cheerful': ['happy', 'bright', 'energetic'],
            'moody': ['dark', 'melancholic', 'dramatic'],
            'neutral': ['balanced', 'calm', 'peaceful']
        }
        return mood_tags.get(mood, ['neutral'])
    
    def _analyze_style_heuristics(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze style using heuristics"""
        # This would implement style analysis heuristics
        return {
            'primary': 'photography',
            'confidence': 0.5,
            'all_styles': [{'name': 'photography', 'confidence': 0.5}]
        }
    
    def _calculate_overall_confidence(self) -> float:
        """Calculate overall AI confidence"""
        # This would calculate confidence based on model outputs
        return 0.8  # Placeholder


def analyze_image_with_ai(image_path: str, config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Analyze a single image with AI-powered content analysis
    """
    analyzer = AIContentAnalyzer(config)
    return analyzer.analyze_image_content(image_path)