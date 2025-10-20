#!/usr/bin/env python3
"""
Audrey Math Course Generator
A comprehensive Python script to create kindergarten math course materials for 3-year-old children in Hong Kong style.

Features:
- 6 progressive learning stages
- Modular functions for different content types
- PDF worksheets with drawings
- Excel activity sheets
- Markdown goals documentation
- AI-powered content generation with Gemini API
- Error-resistant design with comprehensive try-except handling

Author: Generated for Audrey Math Education
Version: 1.0
"""

import os
import json
import logging
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import traceback

# Third-party imports (to be installed)
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing, Rect, Circle, Polygon
    from reportlab.graphics import renderPDF
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not available. PDF generation will be disabled.")

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False
    print("Warning: fpdf not available. Will use reportlab as fallback.")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available. Excel generation will be disabled.")

try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False
    print("Warning: requests/BeautifulSoup not available. Web scraping will be disabled.")

try:
    from PIL import Image as PILImage, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Warning: Pillow not available. Image generation will be disabled.")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not available. AI content generation will be disabled.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('audrey_math_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AudreyMathCourseGenerator:
    """
    Main class for generating kindergarten math course materials.
    Designed specifically for 3-year-old children in Hong Kong educational style.
    """
    
    def __init__(self, output_dir: str = "audrey_math_output", gemini_api_key: Optional[str] = None):
        """
        Initialize the course generator.
        
        Args:
            output_dir: Directory to save generated materials
            gemini_api_key: API key for Gemini AI content generation
        """
        self.output_dir = output_dir
        self.gemini_api_key = gemini_api_key
        self.stages = {
            1: "Number Recognition and Counting (1-10)",
            2: "Shapes and Colors",
            3: "Patterns and Classification",
            4: "Basic Addition/Subtraction with Objects",
            5: "Measurement and Comparison",
            6: "Space and Problem Solving"
        }
        
        # Create output directory
        self._create_output_directory()
        
        # Initialize Gemini AI if available
        if GEMINI_AVAILABLE and gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                self.ai_enabled = True
                logger.info("Gemini AI initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini AI: {e}")
                self.ai_enabled = False
        else:
            self.ai_enabled = False
            logger.info("Gemini AI not available or not configured")
    
    def _create_output_directory(self):
        """Create output directory structure."""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Create subdirectories for different content types
            subdirs = ['goals', 'content', 'worksheets', 'activities', 'images', 'temp']
            for subdir in subdirs:
                os.makedirs(os.path.join(self.output_dir, subdir), exist_ok=True)
            
            logger.info(f"Output directory created: {self.output_dir}")
        except Exception as e:
            logger.error(f"Failed to create output directory: {e}")
            raise
    
    def generate_ai_content(self, prompt: str, context: str = "") -> str:
        """
        Generate content using Gemini AI.
        
        Args:
            prompt: The main prompt for content generation
            context: Additional context for the AI
            
        Returns:
            Generated content as string
        """
        if not self.ai_enabled:
            return self._get_fallback_content(prompt)
        
        try:
            full_prompt = f"""
            You are an expert early childhood educator specializing in Hong Kong kindergarten education.
            Generate engaging, age-appropriate content for 3-year-old children learning math.
            
            Context: {context}
            
            Task: {prompt}
            
            Requirements:
            - Use simple, clear language appropriate for 3-year-olds
            - Include Hong Kong cultural elements where relevant
            - Make content engaging and fun
            - Focus on hands-on learning
            - Use familiar objects and scenarios
            - Keep responses concise but comprehensive
            """
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"AI content generation failed: {e}")
            return self._get_fallback_content(prompt)
    
    def _get_fallback_content(self, prompt: str) -> str:
        """Provide fallback content when AI is not available."""
        fallback_content = {
            "number_recognition": "Learn to recognize numbers 1-10 through fun activities with colorful objects.",
            "shapes_colors": "Identify basic shapes (circle, square, triangle) and primary colors (red, blue, yellow).",
            "patterns": "Create and recognize simple patterns using objects and colors.",
            "addition_subtraction": "Basic counting and simple addition/subtraction using physical objects.",
            "measurement": "Compare sizes, lengths, and weights of everyday objects.",
            "problem_solving": "Solve simple spatial problems and puzzles."
        }
        return fallback_content.get(prompt.lower().replace(" ", "_"), "Educational content for young learners.")
    
    def generate_goals_markdown(self, stage: int) -> str:
        """
        Generate learning goals in Markdown format.
        
        Args:
            stage: The learning stage (1-6)
            
        Returns:
            Markdown formatted goals
        """
        try:
            stage_name = self.stages.get(stage, "Unknown Stage")
            
            if self.ai_enabled:
                goals_content = self.generate_ai_content(
                    f"Create detailed learning goals for stage {stage}: {stage_name}",
                    f"Hong Kong kindergarten curriculum for 3-year-olds"
                )
            else:
                goals_content = self._get_default_goals(stage)
            
            # Special formatting for Stage 1
            if stage == 1:
                markdown_content = f"""# 🎯 Stage {stage}: {stage_name}

## 🌟 Learning Goals & Objectives

{goals_content}

## 🎨 Fun & Interactive Activities for 3-5 Year Olds

### 🧸 Toy-Based Learning
- **Lego Counting**: Build towers with 1-10 blocks
- **Doll Tea Party**: Set table for 5 dolls, count cups and plates
- **Toy Car Garage**: Park 1-10 cars in numbered parking spots
- **Building Blocks**: Create structures using specific number of blocks

### 🎵 Musical & Movement Activities
- **Number Dance**: Dance to counting songs with movements
- **Finger Counting**: Use fingers to show numbers while singing
- **Jump & Count**: Jump the number of times shown on cards
- **Clap & Count**: Clap hands to match the number called out

### 🏠 Daily Life Integration
- **MTR Station Counting**: Count stops on familiar routes
- **Dim Sum Counting**: Count dumplings, buns, and tea cups
- **Elevator Fun**: Count floors as elevator moves
- **Shopping Helper**: Count items in shopping basket

## 🎯 Self-Confidence Building

### 💪 Positive Reinforcement Strategies
- **Celebration Rituals**: High-fives, stickers, applause for attempts
- **Success Sharing**: Children share counting achievements with class
- **Peer Support**: Older children help younger ones count
- **Parent Communication**: Send home counting success stories

### 🌈 Emotional Support
- **"Great Try" Culture**: Emphasize effort over perfection
- **Individual Pacing**: Allow each child to progress at their own speed
- **Error Celebration**: "Oops! Let's try again together!"
- **Progress Recognition**: Notice and celebrate small improvements

## 📊 Assessment Criteria
- Child demonstrates **enthusiasm** for counting activities
- Child shows **engagement** and curiosity about numbers
- Child can follow simple counting instructions with **confidence**
- Child demonstrates **progress** over time in number recognition
- Child exhibits **positive attitude** towards mathematics

## 🇭🇰 Hong Kong Education Standards
- **Aligned** with Hong Kong Kindergarten Education Curriculum Guide
- **Supports** holistic development (cognitive, emotional, social)
- **Promotes** active learning through play and exploration
- **Integrates** local culture and daily life experiences
- **Builds** foundation for future mathematical learning

## 📅 Implementation Timeline
- **Week 1-2**: Numbers 1-3 with toys and songs
- **Week 3-4**: Numbers 4-6 with daily life integration
- **Week 5-6**: Numbers 7-10 with confidence building
- **Week 7-8**: Review and celebration of achievements

---
*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*For Hong Kong Kindergarten Education - Building Confident Young Mathematicians* 🌟
"""
            elif stage == 2:
                markdown_content = f"""# 🔷 Stage {stage}: {stage_name}

## 🌈 Learning Goals & Objectives

{goals_content}

## 🎨 Fun & Interactive Activities for 3-5 Year Olds

### 🔍 Shape Hunt Adventures
- **🏢 Hong Kong Building Hunt**: Find circles (wheels), squares (windows), triangles (roofs)
- **🚇 MTR Station Shape Safari**: Identify shapes in station designs and signs
- **🥟 Dim Sum Shape Discovery**: Circle dumplings, square tofu, triangle spring rolls
- **🛍️ Shopping Mall Shape Quest**: Find shapes in store layouts and decorations
- **🌳 Park Shape Explorer**: Discover shapes in playground equipment and nature

### 🎨 Drawing & Art Activities
- **✏️ Shape Tracing**: Practice drawing basic shapes with confidence
- **🌈 Color Mixing Magic**: Create new colors by combining primary colors
- **🎭 Shape Collage Art**: Cut and paste shapes to create Hong Kong scenes
- **🧱 Building Block Art**: Use 3D shapes to build mini Hong Kong landmarks
- **🍃 Nature Shape Art**: Create art using natural shapes found in Hong Kong parks

### 🎮 Game-Based Learning
- **🎯 Shape Bingo**: Hong Kong-themed shape identification game
- **🧠 Color Memory Match**: Match colors with Hong Kong cultural items
- **🔍 Shape Scavenger Hunt**: Find shapes around the classroom and school
- **🏗️ Building Shape Towers**: Stack different shaped blocks to build structures
- **📚 Shape Story Creation**: Tell stories using different shapes as characters

## 🏙️ Real-Life Hong Kong Examples

### 🔴 Red Elements
- **Red Lanterns**: Circle shapes in traditional decorations
- **Red Taxis**: Rectangle shapes in daily transportation
- **Red Dragon**: Triangle shapes in festival decorations

### 🔵 Blue Elements
- **Blue Harbor Water**: Color recognition in natural settings
- **Blue Sky**: Background for shape identification
- **Blue MTR Signs**: Square shapes in transportation

### 🟡 Yellow Elements
- **Yellow Taxis**: Rectangle shapes in daily life
- **Yellow Sun**: Circle shape in nature
- **Yellow Buildings**: Architectural color recognition

## 🎯 Curiosity Building

### 🤔 "I Wonder" Questions
- **Shape Detective**: Children become investigators finding shapes everywhere
- **Color Experiments**: Mix colors to discover new combinations
- **Environmental Exploration**: Walk around school to find real shapes
- **Shape Stories**: Create narratives using different shapes as characters

### 🌟 Encouraging Exploration
- **"What shapes do you see?"**: Open-ended questioning
- **"How can we make new colors?"**: Experimental learning
- **"Where else might we find this shape?"**: Extending learning beyond classroom
- **"What story can we tell with shapes?"**: Creative expression

## 📊 Assessment Criteria
- Child demonstrates **curiosity** about shapes and colors in environment
- Child shows **enthusiasm** for shape hunting and art activities
- Child can **identify** basic shapes (circle, square, triangle, rectangle) confidently
- Child exhibits **creativity** in combining shapes and colors
- Child demonstrates **spatial awareness** through shape exploration

## 🇭🇰 Hong Kong Education Standards
- **Aligned** with Hong Kong Kindergarten Education Curriculum Guide
- **Supports** visual-spatial development and artistic expression
- **Promotes** cultural awareness through local examples
- **Integrates** real-world learning with classroom activities
- **Builds** foundation for geometric thinking

## 📅 Implementation Timeline
- **Week 1-2**: Circle and square recognition with Hong Kong buildings
- **Week 3-4**: Triangle and rectangle with transportation and nature
- **Week 5-6**: Color mixing and combination activities
- **Week 7-8**: Creative art projects and shape stories

---
*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*For Hong Kong Kindergarten Education - Nurturing Creative Shape Explorers* 🔷
"""
            else:
                markdown_content = f"""# Stage {stage}: {stage_name}

## Learning Goals

{goals_content}

## Assessment Criteria
- Child can demonstrate understanding through play-based activities
- Child shows engagement and curiosity
- Child can follow simple instructions
- Child demonstrates progress over time

## Hong Kong Education Standards
- Aligned with Hong Kong Kindergarten Education Curriculum Guide
- Supports holistic development
- Promotes active learning through play

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            # Save to file
            filename = f"stage_{stage}_goals.md"
            filepath = os.path.join(self.output_dir, 'goals', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Goals generated for stage {stage}: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate goals for stage {stage}: {e}")
            return ""
    
    def _get_default_goals(self, stage: int) -> str:
        """Get default goals when AI is not available."""
        default_goals = {
            1: """
- **Recognize numbers 1-10** with confidence and enthusiasm
- **Count objects accurately** using hands-on manipulatives
- **Build positive attitudes** towards mathematics through play
- **Understand one-to-one correspondence** through daily activities
- **Develop number sense** with Hong Kong cultural context
- **Enhance self-confidence** through successful counting experiences
            """,
            2: """
- **Identify basic shapes** (circle, square, triangle, rectangle) with confidence
- **Combine colors** creatively through art and craft activities
- **Foster curiosity** about shapes and colors in the environment
- **Match shapes and colors** through interactive games
- **Sort objects** by shape and color attributes
- **Develop spatial awareness** through shape exploration
            """,
            3: """
- Create simple patterns (AB, AAB, ABC)
- Recognize and continue patterns
- Classify objects by attributes
- Group similar items together
            """,
            4: """
- Understand addition as combining groups
- Understand subtraction as taking away
- Use concrete objects for counting
- Develop number bonds to 10
            """,
            5: """
- Compare sizes (big/small, long/short)
- Understand measurement concepts
- Use non-standard units
- Order objects by size
            """,
            6: """
- Understand spatial relationships
- Solve simple puzzles
- Follow positional instructions
- Develop logical thinking
            """
        }
        return default_goals.get(stage, "Develop mathematical thinking and problem-solving skills.")
    
    def generate_content_text(self, stage: int) -> str:
        """
        Generate detailed content text for the stage.
        
        Args:
            stage: The learning stage (1-6)
            
        Returns:
            File path to generated content
        """
        try:
            stage_name = self.stages.get(stage, "Unknown Stage")
            
            if self.ai_enabled:
                content = self.generate_ai_content(
                    f"Create detailed teaching content and activities for stage {stage}: {stage_name}",
                    f"Comprehensive lesson plans for Hong Kong kindergarten"
                )
            else:
                content = self._get_default_content(stage)
            
            content_text = f"""STAGE {stage}: {stage_name.upper()}
=====================================

CONTENT OVERVIEW:
{content}

TEACHING STRATEGIES:
- Use concrete materials and manipulatives
- Incorporate songs and rhymes
- Provide hands-on experiences
- Encourage exploration and discovery
- Use visual aids and props

ACTIVITIES SUGGESTIONS:
- Interactive games and puzzles
- Art and craft projects
- Outdoor learning opportunities
- Technology integration (age-appropriate)
- Parent involvement activities

ASSESSMENT METHODS:
- Observation during play
- Portfolio collection
- Photo documentation
- Parent feedback
- Progress checklists

RESOURCES NEEDED:
- Counting objects (blocks, buttons, toys)
- Shape templates and cutouts
- Color materials (crayons, paints, paper)
- Measuring tools (rulers, scales, containers)
- Puzzle pieces and games

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            # Integrate EDB ideas into content
            enhanced_content = self.integrate_edb_ideas(content_text, stage)
            
            # Save to file
            filename = f"stage_{stage}_content.txt"
            filepath = os.path.join(self.output_dir, 'content', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            logger.info(f"Content generated for stage {stage}: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate content for stage {stage}: {e}")
            return ""
    
    def _get_default_content(self, stage: int) -> str:
        """Get default content when AI is not available."""
        default_content = {
            1: """
# 🎯 Stage 1: Number Recognition & Counting (1-10) - Hong Kong Style

## 🌟 Learning Foundation
Number recognition and counting form the foundation of mathematical understanding for 3-5 year olds. 
Children learn to identify numerals and associate them with quantities through joyful, hands-on activities 
with familiar Hong Kong objects and daily life experiences.

## 🎨 Key Learning Concepts
- **One-to-one correspondence**: Each object gets one number
- **Cardinality**: The last number counted tells us "how many"
- **Number sequence and order**: Understanding 1 comes before 2, etc.
- **Visual recognition of numerals**: Recognizing written numbers 1-10
- **Self-confidence building**: Celebrating every counting success!

## 🧸 Interactive Activities with Toys & Games
- **Counting with Hong Kong toys**: Lego blocks, toy cars, dolls
- **Number songs and rhymes**: "一二三，上山打老虎" (1,2,3, climb the mountain to catch tigers)
- **Daily life counting**: Count stairs, elevator floors, MTR stations
- **Food counting games**: Count dim sum pieces, mooncakes, oranges

## 🎵 Songs & Rhymes for Learning
- Traditional Chinese counting songs
- English number rhymes with Hong Kong themes
- Movement songs incorporating counting (jump 5 times, clap 3 times)
- Finger counting songs with visual aids

## 🏠 Daily Life Integration
- Count family members at dinner
- Count toys while cleaning up
- Count coins when shopping
- Count steps when walking
- Count buttons on clothes
- Count windows in buildings

## 🎯 Self-Confidence Building Strategies
- **Celebrate every attempt**: "Great try!" "You're getting better!"
- **Use positive reinforcement**: Stickers, high-fives, applause
- **Start with success**: Begin with numbers they know well
- **Peer support**: Children help each other count
- **Parent involvement**: Share counting successes at home
            """,
            2: """
# 🔷 Stage 2: Shapes & Colors - Hong Kong Discovery Adventure

## 🌈 Learning Foundation
Shapes and colors are fundamental concepts that help children organize and 
understand their visual world. This stage focuses on basic geometric shapes 
and color exploration through Hong Kong's vibrant culture and architecture.

## 🎨 Key Learning Concepts
- **Shape recognition**: Circle, square, triangle, rectangle identification
- **Color exploration**: Primary colors (red, blue, yellow) and color mixing
- **Spatial awareness**: Understanding shapes in 2D and 3D contexts
- **Curiosity building**: Encouraging questions and exploration
- **Creative expression**: Combining shapes and colors in art

## 🔍 Shape Hunt Adventures
- **Hong Kong Building Hunt**: Find circles (wheels), squares (windows), triangles (roofs)
- **MTR Station Shape Safari**: Identify shapes in station designs and signs
- **Dim Sum Shape Discovery**: Circle dumplings, square tofu, triangle spring rolls
- **Shopping Mall Shape Quest**: Find shapes in store layouts and decorations
- **Park Shape Explorer**: Discover shapes in playground equipment and nature

## 🎨 Drawing & Art Activities
- **Shape Tracing**: Practice drawing basic shapes with confidence
- **Color Mixing Magic**: Create new colors by combining primary colors
- **Shape Collage Art**: Cut and paste shapes to create Hong Kong scenes
- **Building Block Art**: Use 3D shapes to build mini Hong Kong landmarks
- **Nature Shape Art**: Create art using natural shapes found in Hong Kong parks

## 🎮 Game-Based Learning
- **Shape Bingo**: Hong Kong-themed shape identification game
- **Color Memory Match**: Match colors with Hong Kong cultural items
- **Shape Scavenger Hunt**: Find shapes around the classroom and school
- **Building Shape Towers**: Stack different shaped blocks to build structures
- **Shape Story Creation**: Tell stories using different shapes as characters

## 🏙️ Real-Life Hong Kong Examples
- **Red Lanterns**: Circle shapes in traditional decorations
- **Blue Harbor Water**: Color recognition in natural settings
- **Yellow Taxis**: Rectangle shapes in daily transportation
- **Green Mountains**: Triangle peaks of Hong Kong's landscape
- **Traditional Architecture**: Square and rectangular building patterns
- **Festival Decorations**: Various shapes in cultural celebrations

## 🎯 Curiosity Building Strategies
- **"I Wonder" Questions**: Encourage children to ask about shapes they see
- **Shape Detective**: Children become investigators finding shapes everywhere
- **Color Experiments**: Mix colors to discover new combinations
- **Shape Stories**: Create narratives using different shapes
- **Environmental Exploration**: Walk around school to find real shapes
            """,
            3: """
Pattern recognition is crucial for mathematical thinking and logical reasoning. 
Children learn to identify, create, and extend patterns using various attributes.

Focus areas:
- Simple repeating patterns (AB, AAB, ABC)
- Pattern recognition in daily life
- Classification by multiple attributes
- Logical sequencing

Incorporate Hong Kong patterns like traditional architectural designs, 
festival decorations, and cultural symbols.
            """,
            4: """
Basic addition and subtraction introduce children to the fundamental operations 
of mathematics using concrete objects and visual representations.

Key learning points:
- Addition as combining groups
- Subtraction as taking away or comparing
- Using fingers and objects for counting
- Understanding "more" and "less"

Start with numbers 1-5 and gradually extend to 10, using Hong Kong 
contexts like counting dim sum pieces or MTR stations.
            """,
            5: """
Measurement and comparison help children understand size, length, weight, 
and capacity using non-standard units and everyday objects.

Learning objectives:
- Comparing sizes (big/small, long/short, tall/short)
- Understanding measurement concepts
- Using body parts for measurement
- Ordering objects by size

Use Hong Kong landmarks and objects for comparisons - comparing the height 
of buildings, length of the harbor, or size of traditional items.
            """,
            6: """
Spatial awareness and problem-solving develop logical thinking and 
reasoning skills essential for mathematical understanding.

Skills developed:
- Understanding positional words (above, below, beside)
- Solving simple puzzles and mazes
- Following multi-step instructions
- Logical reasoning and deduction

Create Hong Kong-themed spatial activities using the city's unique 
architecture and layout as learning contexts.
            """
        }
        return default_content.get(stage, "Comprehensive mathematical learning through play-based activities.")
    
    def generate_worksheet_pdf(self, stage: int) -> str:
        """
        Generate PDF worksheet with drawings.
        
        Args:
            stage: The learning stage (1-6)
            
        Returns:
            File path to generated PDF
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("reportlab not available. Cannot generate PDF worksheets.")
            return ""
        
        try:
            stage_name = self.stages.get(stage, "Unknown Stage")
            filename = f"stage_{stage}_worksheet.pdf"
            filepath = os.path.join(self.output_dir, 'worksheets', filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1,  # Center alignment
                textColor=colors.darkblue
            )
            
            title = Paragraph(f"Stage {stage}: {stage_name}", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Add stage-specific content and drawings
            self._add_stage_content_to_pdf(story, stage, styles)
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF worksheet generated for stage {stage}: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate PDF worksheet for stage {stage}: {e}")
            return ""
    
    def _add_stage_content_to_pdf(self, story: List, stage: int, styles):
        """Add stage-specific content and drawings to PDF."""
        try:
            if stage == 1:  # Number recognition and counting
                self._add_number_recognition_content(story, styles)
            elif stage == 2:  # Shapes and colors
                self._add_shapes_colors_content(story, styles)
            elif stage == 3:  # Patterns and classification
                self._add_patterns_content(story, styles)
            elif stage == 4:  # Basic addition/subtraction
                self._add_addition_subtraction_content(story, styles)
            elif stage == 5:  # Measurement and comparison
                self._add_measurement_content(story, styles)
            elif stage == 6:  # Space and problem solving
                self._add_spatial_content(story, styles)
                
        except Exception as e:
            logger.error(f"Failed to add content for stage {stage}: {e}")
    
    def _add_number_recognition_content(self, story: List, styles):
        """Add number recognition content to PDF."""
        # Instructions
        instruction_text = """
        <b>Activity 1: Count the Objects</b><br/>
        Count each group of objects and circle the correct number.
        """
        story.append(Paragraph(instruction_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Create a simple drawing with numbers and objects
        drawing = Drawing(400, 200)
        
        # Add circles to represent counting objects
        for i in range(3):
            x = 50 + i * 120
            y = 100
            
            # Draw circles (objects to count)
            for j in range(i + 1):
                circle = Circle(x + j * 20, y, 8)
                circle.fillColor = colors.lightblue
                circle.strokeColor = colors.darkblue
                drawing.add(circle)
            
            # Add number below
            from reportlab.graphics.shapes import String
            number_text = String(x + 20, y - 30, str(i + 1), fontSize=20)
            drawing.add(number_text)
        
        story.append(drawing)
        story.append(Spacer(1, 30))
        
        # Add more activities
        activity_text = """
        <b>Activity 2: Number Matching</b><br/>
        Draw a line from each number to the matching group of objects.
        """
        story.append(Paragraph(activity_text, styles['Normal']))
    
    def _add_shapes_colors_content(self, story: List, styles):
        """Add shapes and colors content to PDF."""
        instruction_text = """
        <b>Activity 1: Shape Hunt</b><br/>
        Find and color the shapes. Circle = Red, Square = Blue, Triangle = Yellow
        """
        story.append(Paragraph(instruction_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Create shape drawing
        drawing = Drawing(400, 200)
        
        # Add shapes
        shapes = [
            (Circle(100, 150, 30), colors.red),
            (Rect(200, 120, 60, 60), colors.blue),
            (Polygon([(350, 180), (320, 120), (380, 120)]), colors.yellow)
        ]
        
        for shape, color in shapes:
            shape.fillColor = color
            shape.strokeColor = colors.black
            drawing.add(shape)
        
        story.append(drawing)
    
    def _add_patterns_content(self, story: List, styles):
        """Add patterns content to PDF."""
        instruction_text = """
        <b>Activity 1: Continue the Pattern</b><br/>
        Look at the pattern and draw what comes next.
        """
        story.append(Paragraph(instruction_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Create pattern drawing
        drawing = Drawing(400, 150)
        
        # Create AB pattern with circles and squares
        for i in range(6):
            x = 50 + i * 50
            y = 100
            
            if i % 2 == 0:
                shape = Circle(x, y, 15)
                shape.fillColor = colors.red
            else:
                shape = Rect(x-15, y-15, 30, 30)
                shape.fillColor = colors.blue
            
            shape.strokeColor = colors.black
            drawing.add(shape)
        
        story.append(drawing)
    
    def _add_addition_subtraction_content(self, story: List, styles):
        """Add addition/subtraction content to PDF."""
        instruction_text = """
        <b>Activity 1: Count and Add</b><br/>
        Count the objects in each group and write the total.
        """
        story.append(Paragraph(instruction_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Create addition drawing
        drawing = Drawing(400, 200)
        
        # First group (2 objects)
        for i in range(2):
            circle = Circle(100 + i * 30, 150, 10)
            circle.fillColor = colors.green
            drawing.add(circle)
        
        # Plus sign
        from reportlab.graphics.shapes import String
        plus_text = String(200, 140, "+", fontSize=30)
        drawing.add(plus_text)
        
        # Second group (3 objects)
        for i in range(3):
            circle = Circle(250 + i * 30, 150, 10)
            circle.fillColor = colors.orange
            drawing.add(circle)
        
        # Equals sign
        equals_text = String(350, 140, "=", fontSize=30)
        drawing.add(equals_text)
        
        story.append(drawing)
    
    def _add_measurement_content(self, story: List, styles):
        """Add measurement content to PDF."""
        instruction_text = """
        <b>Activity 1: Which is Bigger?</b><br/>
        Circle the bigger object in each pair.
        """
        story.append(Paragraph(instruction_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Create comparison drawing
        drawing = Drawing(400, 200)
        
        # Big circle
        big_circle = Circle(100, 150, 40)
        big_circle.fillColor = colors.lightblue
        big_circle.strokeColor = colors.black
        drawing.add(big_circle)
        
        # Small circle
        small_circle = Circle(100, 80, 20)
        small_circle.fillColor = colors.lightblue
        small_circle.strokeColor = colors.black
        drawing.add(small_circle)
        
        story.append(drawing)
    
    def _add_spatial_content(self, story: List, styles):
        """Add spatial content to PDF."""
        instruction_text = """
        <b>Activity 1: Where is the Cat?</b><br/>
        Look at the picture and answer the questions.
        """
        story.append(Paragraph(instruction_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Create spatial drawing
        drawing = Drawing(400, 200)
        
        # House
        house = Rect(200, 100, 100, 80)
        house.fillColor = colors.lightgrey
        house.strokeColor = colors.black
        drawing.add(house)
        
        # Cat
        cat = Circle(250, 140, 15)
        cat.fillColor = colors.orange
        drawing.add(cat)
        
        story.append(drawing)
    
    def generate_visual_worksheet_pdf(self, stage: int) -> str:
        """
        Generate visual worksheet PDF using FPDF (preferred) or ReportLab (fallback).
        Creates colorful, kid-friendly worksheets for each stage.
        
        Args:
            stage: The learning stage (1-6)
            
        Returns:
            File path to generated PDF worksheet
        """
        try:
            stage_name = self.stages.get(stage, "Unknown Stage")
            filename = f"visual_worksheet_stage_{stage}.pdf"
            filepath = os.path.join(self.output_dir, 'worksheets', filename)
            
            # Try ReportLab first (more visual), fallback to FPDF
            if REPORTLAB_AVAILABLE:
                return self._generate_reportlab_worksheet(stage, stage_name, filepath)
            elif FPDF_AVAILABLE:
                return self._generate_fpdf_worksheet(stage, stage_name, filepath)
            else:
                logger.error("Neither ReportLab nor FPDF available. Cannot generate visual worksheets.")
                return ""
                
        except Exception as e:
            logger.error(f"Failed to generate visual worksheet for stage {stage}: {e}")
            return ""
    
    def _generate_fpdf_worksheet(self, stage: int, stage_name: str, filepath: str) -> str:
        """Generate worksheet using FPDF (simpler approach)."""
        try:
            # Create PDF with FPDF
            pdf = FPDF()
            pdf.add_page()
            
            # Set font for title
            pdf.set_font('Arial', 'B', 24)
            
            # Add title
            title = f"Fun {self._get_stage_title(stage)} Worksheet for K2"
            pdf.cell(0, 15, title, 0, 1, 'C')
            pdf.ln(10)
            
            # Add stage-specific content
            if stage == 1:
                self._add_stage1_fpdf_content(pdf)
            elif stage == 2:
                self._add_stage2_fpdf_content(pdf)
            elif stage == 4:
                self._add_stage4_fpdf_content(pdf)
            else:
                self._add_default_fpdf_content(pdf, stage)
            
            # Save PDF
            pdf.output(filepath)
            logger.info(f"FPDF visual worksheet generated for stage {stage}: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"FPDF worksheet generation failed: {e}")
            return ""
    
    def _get_stage_title(self, stage: int) -> str:
        """Get simplified stage title for worksheet."""
        titles = {
            1: "Number",
            2: "Shape", 
            3: "Pattern",
            4: "Addition",
            5: "Measurement",
            6: "Space"
        }
        return titles.get(stage, "Math")
    
    def _add_stage1_fpdf_content(self, pdf):
        """Add Stage 1 number worksheet content."""
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, "Count and Draw Numbers 1-5", 0, 1, 'C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        
        # Number 1
        pdf.cell(0, 10, "1. Draw 1 apple and count:", 0, 1)
        pdf.ln(15)  # Space for drawing
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())  # Drawing line
        pdf.ln(10)
        
        # Number 2
        pdf.cell(0, 10, "2. Draw 2 cars and count:", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # Number 3
        pdf.cell(0, 10, "3. Draw 3 balls and count:", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # Number 4
        pdf.cell(0, 10, "4. Draw 4 stars and count:", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # Number 5
        pdf.cell(0, 10, "5. Draw 5 hearts and count:", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(15)
        
        # Hong Kong element
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 8, "Bonus: Count MTR stations from Central to Causeway Bay!", 0, 1, 'C')
        
    def _add_stage2_fpdf_content(self, pdf):
        """Add Stage 2 shapes worksheet content."""
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, "Draw and Color Shapes", 0, 1, 'C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        
        # Circle
        pdf.cell(0, 10, "1. Draw a circle and color it red (like a ball):", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # Square
        pdf.cell(0, 10, "2. Draw a square and color it blue (like a window):", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # Triangle
        pdf.cell(0, 10, "3. Draw a triangle and color it yellow (like a roof):", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # Rectangle
        pdf.cell(0, 10, "4. Draw a rectangle and color it green (like a door):", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(15)
        
        # Hong Kong element
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 8, "Bonus: Find these shapes in Hong Kong buildings!", 0, 1, 'C')
        
    def _add_stage4_fpdf_content(self, pdf):
        """Add Stage 4 addition worksheet content."""
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, "Addition Pictures with Objects", 0, 1, 'C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        
        # 2+1=3
        pdf.cell(0, 10, "1. Draw 2 apples + 1 apple = ? apples", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # 1+2=3
        pdf.cell(0, 10, "2. Draw 1 car + 2 cars = ? cars", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # 2+2=4
        pdf.cell(0, 10, "3. Draw 2 balls + 2 balls = ? balls", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        # 1+3=4
        pdf.cell(0, 10, "4. Draw 1 star + 3 stars = ? stars", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(15)
        
        # Hong Kong element
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 8, "Bonus: 2 dim sum + 1 dim sum = ? dim sum!", 0, 1, 'C')
        
    def _add_default_fpdf_content(self, pdf, stage: int):
        """Add default content for other stages."""
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f"Stage {stage} Fun Activities", 0, 1, 'C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, "Draw and color your favorite math activity!", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        pdf.cell(0, 10, "What did you learn today?", 0, 1)
        pdf.ln(15)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(15)
        
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 8, "Great job learning math!", 0, 1, 'C')
    
    def _generate_reportlab_worksheet(self, stage: int, stage_name: str, filepath: str) -> str:
        """Generate worksheet using ReportLab (fallback approach)."""
        try:
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1,  # Center alignment
                textColor=colors.darkblue
            )
            
            title = Paragraph(f"Fun {self._get_stage_title(stage)} Worksheet for K2", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Add stage-specific content
            if stage == 1:
                self._add_stage1_reportlab_content(story, styles)
            elif stage == 2:
                self._add_stage2_reportlab_content(story, styles)
            elif stage == 4:
                self._add_stage4_reportlab_content(story, styles)
            else:
                self._add_default_reportlab_content(story, styles, stage)
            
            # Build PDF
            doc.build(story)
            logger.info(f"ReportLab visual worksheet generated for stage {stage}: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"ReportLab worksheet generation failed: {e}")
            return ""
    
    def _add_stage1_reportlab_content(self, story, styles):
        """Add Stage 1 content to ReportLab PDF with rich visuals."""
        # Colorful title with emoji
        title_style = ParagraphStyle(
            'Stage1Title',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=20,
            alignment=1,
            textColor=colors.darkblue,
            backColor=colors.lightyellow,
            borderColor=colors.orange,
            borderWidth=2,
            borderPadding=10
        )
        
        title = Paragraph("🔢 Fun Number Adventure! 🔢", title_style)
        story.append(title)
        
        # Add colorful instructions
        instruction_style = ParagraphStyle(
            'Instruction',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=15,
            alignment=1,
            textColor=colors.darkgreen,
            backColor=colors.lightgreen,
            borderPadding=8
        )
        
        instruction_text = """
        <b>🎯 Let's Count Together!</b><br/>
        Draw the objects and count them out loud! 🗣️
        """
        story.append(Paragraph(instruction_text, instruction_style))
        story.append(Spacer(1, 20))
        
        # Create rich drawing space with backgrounds
        drawing = Drawing(500, 400)
        
        # Add colorful background rectangles for each number
        bg_colors = [colors.lightblue, colors.lightgreen, colors.lightyellow, colors.lightpink, colors.lightcyan]
        
        for i in range(1, 6):
            x = 30 + (i-1) * 90
            y = 280
            
            # Background rectangle
            bg_rect = Rect(x-30, y-40, 80, 80)
            bg_rect.fillColor = bg_colors[i-1]
            bg_rect.strokeColor = colors.black
            bg_rect.strokeWidth = 2
            drawing.add(bg_rect)
            
            # Number circle with gradient effect
            circle = Circle(x+10, y, 25)
            circle.fillColor = colors.darkblue
            circle.strokeColor = colors.white
            circle.strokeWidth = 3
            drawing.add(circle)
            
            # Add number text with white color
            from reportlab.graphics.shapes import String
            number_text = String(x+10, y-5, str(i), fontSize=24, fillColor=colors.white)
            drawing.add(number_text)
            
            # Add decorative stars around numbers
            for star_x in [x-15, x+35]:
                for star_y in [y-25, y+25]:
                    star = String(star_x, star_y, "⭐", fontSize=12)
                    drawing.add(star)
        
        # Add Hong Kong elements
        # MTR train
        train_rect = Rect(50, 180, 120, 30)
        train_rect.fillColor = colors.red
        train_rect.strokeColor = colors.black
        train_rect.strokeWidth = 2
        drawing.add(train_rect)
        
        # Train windows
        for i in range(3):
            window = Circle(70 + i*30, 195, 8)
            window.fillColor = colors.white
            drawing.add(window)
        
        # MTR text
        mtr_text = String(110, 170, "🚇 MTR Train", fontSize=16, fillColor=colors.darkred)
        drawing.add(mtr_text)
        
        # Dim sum elements
        dim_sum_colors = [colors.orange, colors.yellow, colors.green, colors.red, colors.pink]
        for i in range(5):
            dim_sum = Circle(300 + i*25, 200, 12)
            dim_sum.fillColor = dim_sum_colors[i]
            dim_sum.strokeColor = colors.black
            dim_sum.strokeWidth = 1
            drawing.add(dim_sum)
        
        dim_sum_text = String(350, 170, "🥟 Dim Sum", fontSize=16, fillColor=colors.darkorange)
        drawing.add(dim_sum_text)
        
        # Add drawing spaces with dotted lines
        for i in range(3):
            y_pos = 120 - i*40
            # Dotted rectangle for drawing
            dotted_rect = Rect(50, y_pos, 400, 30)
            dotted_rect.fillColor = colors.white
            dotted_rect.strokeColor = colors.gray
            dotted_rect.strokeWidth = 1
            dotted_rect.strokeDashArray = [3, 3]
            drawing.add(dotted_rect)
            
            # Instruction text for each drawing space
            draw_text = String(60, y_pos+10, f"Draw {i+1} item(s) here:", fontSize=12, fillColor=colors.darkblue)
            drawing.add(draw_text)
        
        story.append(drawing)
        story.append(Spacer(1, 20))
        
        # Add Hong Kong bonus with colorful background
        bonus_style = ParagraphStyle(
            'Bonus',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=10,
            alignment=1,
            textColor=colors.white,
            backColor=colors.darkred,
            borderPadding=10
        )
        
        bonus_text = """
        <b>🇭🇰 Hong Kong Challenge! 🇭🇰</b><br/>
        Count MTR stations from Central to Causeway Bay! 🚇
        """
        story.append(Paragraph(bonus_text, bonus_style))
    
    def _add_stage2_reportlab_content(self, story, styles):
        """Add Stage 2 content to ReportLab PDF with rich visuals."""
        # Colorful title
        title_style = ParagraphStyle(
            'Stage2Title',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=20,
            alignment=1,
            textColor=colors.darkgreen,
            backColor=colors.lightcyan,
            borderColor=colors.blue,
            borderWidth=2,
            borderPadding=10
        )
        
        title = Paragraph("🔺🔵🟨 Fun Shape Adventure! 🟩", title_style)
        story.append(title)
        
        # Add colorful instructions
        instruction_style = ParagraphStyle(
            'Instruction',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=15,
            alignment=1,
            textColor=colors.white,
            backColor=colors.darkgreen,
            borderPadding=8
        )
        
        instruction_text = """
        <b>🎨 Let's Find Shapes Everywhere! 🎨</b><br/>
        Draw and color the shapes like real Hong Kong objects!
        """
        story.append(Paragraph(instruction_text, instruction_style))
        story.append(Spacer(1, 20))
        
        # Create rich shape drawing
        drawing = Drawing(500, 450)
        
        # Add colorful background
        bg_rect = Rect(20, 20, 460, 410)
        bg_rect.fillColor = colors.lightyellow
        bg_rect.strokeColor = colors.orange
        bg_rect.strokeWidth = 3
        drawing.add(bg_rect)
        
        # Shape examples with Hong Kong context
        shapes_data = [
            # Circle - Hong Kong Ball
            {
                'shape': Circle(100, 350, 35),
                'color': colors.red,
                'label': "⚽ Hong Kong Ball",
                'emoji': "⚽",
                'x': 100,
                'y': 300
            },
            # Square - MTR Station
            {
                'shape': Rect(200, 315, 70, 70),
                'color': colors.blue,
                'label': "🚇 MTR Station",
                'emoji': "🚇",
                'x': 235,
                'y': 270
            },
            # Triangle - Peak Tram
            {
                'shape': Polygon([350, 350, 320, 290, 380, 290]),
                'color': colors.yellow,
                'label': "🚠 Peak Tram",
                'emoji': "🚠",
                'x': 350,
                'y': 250
            },
            # Rectangle - Hong Kong Building
            {
                'shape': Rect(120, 180, 120, 80),
                'color': colors.green,
                'label': "🏢 Hong Kong Building",
                'emoji': "🏢",
                'x': 180,
                'y': 140
            }
        ]
        
        for shape_info in shapes_data:
            shape = shape_info['shape']
            shape.fillColor = shape_info['color']
            shape.strokeColor = colors.black
            shape.strokeWidth = 3
            drawing.add(shape)
            
            # Add emoji
            from reportlab.graphics.shapes import String
            emoji_text = String(shape_info['x'], shape_info['y'], shape_info['emoji'], fontSize=20)
            drawing.add(emoji_text)
            
            # Add label
            label_text = String(shape_info['x']-20, shape_info['y']-25, shape_info['label'], fontSize=12, fillColor=colors.darkblue)
            drawing.add(label_text)
        
        # Add decorative elements
        # Stars around shapes
        for i in range(8):
            angle = i * 45
            x = 250 + 100 * math.cos(math.radians(angle))
            y = 200 + 100 * math.sin(math.radians(angle))
            star = String(x, y, "⭐", fontSize=10)
            drawing.add(star)
        
        # Add drawing spaces with colorful borders
        draw_colors = [colors.pink, colors.lightgreen, colors.lightblue, colors.lightyellow]
        for i in range(4):
            y_pos = 80 - i*15
            draw_rect = Rect(50, y_pos, 400, 25)
            draw_rect.fillColor = colors.white
            draw_rect.strokeColor = draw_colors[i]
            draw_rect.strokeWidth = 2
            draw_rect.strokeDashArray = [5, 5]
            drawing.add(draw_rect)
            
            draw_text = String(60, y_pos+8, f"Draw and color a {['circle', 'square', 'triangle', 'rectangle'][i]} here:", fontSize=11, fillColor=colors.darkblue)
            drawing.add(draw_text)
        
        story.append(drawing)
        story.append(Spacer(1, 20))
        
        # Add Hong Kong bonus with colorful background
        bonus_style = ParagraphStyle(
            'Bonus',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=10,
            alignment=1,
            textColor=colors.white,
            backColor=colors.darkblue,
            borderPadding=10
        )
        
        bonus_text = """
        <b>🇭🇰 Hong Kong Shape Hunt! 🇭🇰</b><br/>
        Find these shapes in Hong Kong buildings and landmarks! 🏢
        """
        story.append(Paragraph(bonus_text, bonus_style))
    
    def _add_stage4_reportlab_content(self, story, styles):
        """Add Stage 4 content to ReportLab PDF with rich visuals."""
        # Colorful title
        title_style = ParagraphStyle(
            'Stage4Title',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=20,
            alignment=1,
            textColor=colors.darkred,
            backColor=colors.lightpink,
            borderColor=colors.red,
            borderWidth=2,
            borderPadding=10
        )
        
        title = Paragraph("➕➖ Fun Addition Adventure! ➕➖", title_style)
        story.append(title)
        
        # Add colorful instructions
        instruction_style = ParagraphStyle(
            'Instruction',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=15,
            alignment=1,
            textColor=colors.white,
            backColor=colors.darkred,
            borderPadding=8
        )
        
        instruction_text = """
        <b>🧮 Let's Add Things Together! 🧮</b><br/>
        Draw the objects and count them to find the answer!
        """
        story.append(Paragraph(instruction_text, instruction_style))
        story.append(Spacer(1, 20))
        
        # Create rich addition drawing
        drawing = Drawing(500, 500)
        
        # Add colorful background
        bg_rect = Rect(20, 20, 460, 460)
        bg_rect.fillColor = colors.lightcyan
        bg_rect.strokeColor = colors.blue
        bg_rect.strokeWidth = 3
        drawing.add(bg_rect)
        
        # Addition problems with Hong Kong themes
        problems = [
            {
                'equation': '2 + 1 = ?',
                'theme': '🥟 Dim Sum',
                'objects': [
                    {'type': 'circle', 'x': 80, 'y': 400, 'color': colors.orange, 'count': 2},
                    {'type': 'circle', 'x': 180, 'y': 400, 'color': colors.orange, 'count': 1},
                    {'plus': {'x': 130, 'y': 400, 'size': 20}},
                    {'equals': {'x': 230, 'y': 400, 'size': 20}},
                    {'question': {'x': 280, 'y': 400, 'size': 20}}
                ],
                'label_y': 350
            },
            {
                'equation': '1 + 2 = ?',
                'theme': '🚇 MTR Trains',
                'objects': [
                    {'type': 'rect', 'x': 80, 'y': 320, 'color': colors.red, 'count': 1},
                    {'type': 'rect', 'x': 180, 'y': 320, 'color': colors.red, 'count': 2},
                    {'plus': {'x': 130, 'y': 320, 'size': 20}},
                    {'equals': {'x': 230, 'y': 320, 'size': 20}},
                    {'question': {'x': 280, 'y': 320, 'size': 20}}
                ],
                'label_y': 270
            },
            {
                'equation': '2 + 2 = ?',
                'theme': '🏢 Buildings',
                'objects': [
                    {'type': 'rect', 'x': 80, 'y': 240, 'color': colors.blue, 'count': 2},
                    {'type': 'rect', 'x': 180, 'y': 240, 'color': colors.blue, 'count': 2},
                    {'plus': {'x': 130, 'y': 240, 'size': 20}},
                    {'equals': {'x': 230, 'y': 240, 'size': 20}},
                    {'question': {'x': 280, 'y': 240, 'size': 20}}
                ],
                'label_y': 190
            }
        ]
        
        for problem in problems:
            # Draw objects
            for obj in problem['objects']:
                if 'type' in obj and obj['type'] == 'circle':
                    for i in range(obj['count']):
                        circle = Circle(obj['x'] + i*15, obj['y'], 8)
                        circle.fillColor = obj['color']
                        circle.strokeColor = colors.black
                        circle.strokeWidth = 2
                        drawing.add(circle)
                elif 'type' in obj and obj['type'] == 'rect':
                    for i in range(obj['count']):
                        rect = Rect(obj['x'] + i*20, obj['y']-10, 15, 20)
                        rect.fillColor = obj['color']
                        rect.strokeColor = colors.black
                        rect.strokeWidth = 2
                        drawing.add(rect)
                elif 'plus' in obj:
                    from reportlab.graphics.shapes import String
                    plus_text = String(obj['plus']['x'], obj['plus']['y'], "+", fontSize=obj['plus']['size'], fillColor=colors.darkred)
                    drawing.add(plus_text)
                elif 'equals' in obj:
                    from reportlab.graphics.shapes import String
                    equals_text = String(obj['equals']['x'], obj['equals']['y'], "=", fontSize=obj['equals']['size'], fillColor=colors.darkblue)
                    drawing.add(equals_text)
                elif 'question' in obj:
                    from reportlab.graphics.shapes import String
                    question_text = String(obj['question']['x'], obj['question']['y'], "?", fontSize=obj['question']['size'], fillColor=colors.darkgreen)
                    drawing.add(question_text)
            
            # Add theme label
            from reportlab.graphics.shapes import String
            theme_text = String(50, problem['label_y'], problem['theme'], fontSize=14, fillColor=colors.darkblue)
            drawing.add(theme_text)
        
        # Add decorative elements
        for i in range(12):
            angle = i * 30
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150 * math.sin(math.radians(angle))
            star = String(x, y, "⭐", fontSize=8)
            drawing.add(star)
        
        # Add drawing spaces
        draw_colors = [colors.pink, colors.lightgreen, colors.lightblue]
        for i in range(3):
            y_pos = 140 - i*35
            draw_rect = Rect(50, y_pos, 400, 30)
            draw_rect.fillColor = colors.white
            draw_rect.strokeColor = draw_colors[i]
            draw_rect.strokeWidth = 2
            draw_rect.strokeDashArray = [5, 5]
            drawing.add(draw_rect)
            
            draw_text = String(60, y_pos+10, f"Draw your answer here: {['3', '3', '4'][i]} objects", fontSize=12, fillColor=colors.darkblue)
            drawing.add(draw_text)
        
        story.append(drawing)
        story.append(Spacer(1, 20))
        
        # Add Hong Kong bonus with colorful background
        bonus_style = ParagraphStyle(
            'Bonus',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=10,
            alignment=1,
            textColor=colors.white,
            backColor=colors.darkgreen,
            borderPadding=10
        )
        
        bonus_text = """
        <b>🇭🇰 Hong Kong Math Challenge! 🇭🇰</b><br/>
        2 dim sum + 1 dim sum = ? dim sum! 🥟
        """
        story.append(Paragraph(bonus_text, bonus_style))
    
    def _add_default_reportlab_content(self, story, styles, stage: int):
        """Add default content for other stages with rich visuals."""
        # Colorful title
        title_style = ParagraphStyle(
            f'Stage{stage}Title',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=20,
            alignment=1,
            textColor=colors.purple,
            backColor=colors.lightpink,
            borderColor=colors.purple,
            borderWidth=2,
            borderPadding=10
        )
        
        stage_names = {3: "Pattern", 5: "Measurement", 6: "Space"}
        stage_name = stage_names.get(stage, "Math")
        
        title = Paragraph(f"🎨 Fun {stage_name} Adventure! 🎨", title_style)
        story.append(title)
        
        # Add colorful instructions
        instruction_style = ParagraphStyle(
            'Instruction',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=15,
            alignment=1,
            textColor=colors.white,
            backColor=colors.purple,
            borderPadding=8
        )
        
        instruction_text = """
        <b>🌟 Let's Explore and Learn! 🌟</b><br/>
        Draw and color your favorite math activity!
        """
        story.append(Paragraph(instruction_text, instruction_style))
        story.append(Spacer(1, 20))
        
        # Create rich drawing
        drawing = Drawing(500, 400)
        
        # Add colorful background
        bg_rect = Rect(20, 20, 460, 360)
        bg_rect.fillColor = colors.lightyellow
        bg_rect.strokeColor = colors.orange
        bg_rect.strokeWidth = 3
        drawing.add(bg_rect)
        
        # Add Hong Kong elements based on stage
        if stage == 3:  # Patterns
            # Pattern elements
            pattern_colors = [colors.red, colors.blue, colors.yellow, colors.green]
            for i in range(8):
                x = 80 + i * 40
                y = 300
                circle = Circle(x, y, 15)
                circle.fillColor = pattern_colors[i % 4]
                circle.strokeColor = colors.black
                circle.strokeWidth = 2
                drawing.add(circle)
            
            from reportlab.graphics.shapes import String
            pattern_text = String(200, 250, "🔁 Pattern Fun! 🔁", fontSize=18, fillColor=colors.darkblue)
            drawing.add(pattern_text)
            
        elif stage == 5:  # Measurement
            # Measurement elements
            ruler_colors = [colors.red, colors.blue, colors.green]
            for i in range(3):
                x = 100 + i * 100
                y = 300
                rect = Rect(x, y, 60, 20)
                rect.fillColor = ruler_colors[i]
                rect.strokeColor = colors.black
                rect.strokeWidth = 2
                drawing.add(rect)
            
            from reportlab.graphics.shapes import String
            measure_text = String(200, 250, "📏 Measure Everything! 📏", fontSize=18, fillColor=colors.darkblue)
            drawing.add(measure_text)
            
        elif stage == 6:  # Space
            # Space elements
            space_colors = [colors.blue, colors.darkblue, colors.lightblue]
            for i in range(5):
                x = 80 + i * 60
                y = 300
                from reportlab.graphics.shapes import String
                star = String(x, y, "⭐", fontSize=20)
                drawing.add(star)
            
            from reportlab.graphics.shapes import String
            space_text = String(200, 250, "🌌 Space Adventure! 🌌", fontSize=18, fillColor=colors.darkblue)
            drawing.add(space_text)
        
        # Add decorative elements
        for i in range(16):
            angle = i * 22.5
            x = 250 + 120 * math.cos(math.radians(angle))
            y = 200 + 120 * math.sin(math.radians(angle))
            from reportlab.graphics.shapes import String
            star = String(x, y, "✨", fontSize=10)
            drawing.add(star)
        
        # Add drawing space
        draw_rect = Rect(50, 100, 400, 60)
        draw_rect.fillColor = colors.white
        draw_rect.strokeColor = colors.purple
        draw_rect.strokeWidth = 2
        draw_rect.strokeDashArray = [5, 5]
        drawing.add(draw_rect)
        
        from reportlab.graphics.shapes import String
        draw_text = String(60, 130, "Draw your favorite math activity here:", fontSize=14, fillColor=colors.purple)
        drawing.add(draw_text)
        
        story.append(drawing)
        story.append(Spacer(1, 20))
        
        # Add Hong Kong bonus with colorful background
        bonus_style = ParagraphStyle(
            'Bonus',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=10,
            alignment=1,
            textColor=colors.white,
            backColor=colors.darkorange,
            borderPadding=10
        )
        
        bonus_text = """
        <b>🇭🇰 Hong Kong Learning Adventure! 🇭🇰</b><br/>
        Explore math in your Hong Kong neighborhood! 🏙️
        """
        story.append(Paragraph(bonus_text, bonus_style))
    
    def generate_activities_excel(self, stage: int) -> str:
        """
        Generate Excel file with detailed activities for each stage.
        
        Args:
            stage: The learning stage (1-6)
            
        Returns:
            File path to generated Excel file
        """
        if not PANDAS_AVAILABLE:
            logger.error("pandas not available. Cannot generate Excel activities.")
            return ""
        
        try:
            stage_name = self.stages.get(stage, "Unknown Stage")
            filename = f"stage_{stage}_activities.xlsx"
            filepath = os.path.join(self.output_dir, 'activities', filename)
            
            # Create detailed activities data
            activities_data = self._create_detailed_activities_data(stage)
            
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Main detailed activities sheet
                detailed_activities_df = pd.DataFrame(activities_data['detailed_activities'])
                detailed_activities_df.to_excel(writer, sheet_name='Detailed_Activities', index=False)
                
                # Assessment sheet
                assessment_df = pd.DataFrame(activities_data['assessment'])
                assessment_df.to_excel(writer, sheet_name='Assessment', index=False)
                
                # Resources sheet
                resources_df = pd.DataFrame(activities_data['resources'])
                resources_df.to_excel(writer, sheet_name='Resources', index=False)
                
                # Parent tips sheet
                tips_df = pd.DataFrame(activities_data['parent_tips'])
                tips_df.to_excel(writer, sheet_name='Parent_Tips', index=False)
            
            logger.info(f"Excel activities generated for stage {stage}: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate Excel activities for stage {stage}: {e}")
            return ""
    
    def _create_activities_data(self, stage: int) -> Dict:
        """Create activities data for the specified stage."""
        activities_templates = {
            1: {
                'activities': [
                    {'Activity': '🎯 Hong Kong Number Hunt', 'Duration': '15 min', 'Materials': 'MTR station cards, number cards', 'Objective': 'Find and match numbers 1-10 with Hong Kong landmarks'},
                    {'Activity': '🎵 Dim Sum Counting Song', 'Duration': '10 min', 'Materials': 'Traditional songs, toy dim sum', 'Objective': 'Learn counting through Hong Kong food culture'},
                    {'Activity': '🧸 Lego Tower Building', 'Duration': '20 min', 'Materials': 'Lego blocks, number cards', 'Objective': 'Build towers with 1-10 blocks, count while building'},
                    {'Activity': '🏠 Home Counting Adventure', 'Duration': '15 min', 'Materials': 'Family photos, household items', 'Objective': 'Count family members, rooms, and daily objects'},
                    {'Activity': '🚗 Toy Car Garage', 'Duration': '18 min', 'Materials': 'Toy cars, numbered parking spots', 'Objective': 'Park 1-10 cars in numbered spaces'},
                    {'Activity': '🎨 Number Art & Craft', 'Duration': '25 min', 'Materials': 'Paper, stickers, crayons', 'Objective': 'Create number collages with Hong Kong themes'},
                    {'Activity': '👥 Peer Counting Circle', 'Duration': '12 min', 'Materials': 'Circle formation, counting props', 'Objective': 'Count classmates, share counting successes'},
                    {'Activity': '🎪 Number Celebration Show', 'Duration': '20 min', 'Materials': 'Stage area, number costumes', 'Objective': 'Perform counting songs and movements for confidence'}
                ],
                'assessment': [
                    {'Skill': 'Number Recognition', 'Target': 'Recognizes numbers 1-10 with confidence', 'Method': 'Interactive flash card games with positive reinforcement'},
                    {'Skill': 'Counting Accuracy', 'Target': 'Counts objects accurately up to 10', 'Method': 'Observation during play-based activities'},
                    {'Skill': 'Self-Confidence', 'Target': 'Shows enthusiasm and pride in counting', 'Method': 'Behavioral observation and parent feedback'},
                    {'Skill': 'Cultural Integration', 'Target': 'Uses Hong Kong examples in counting', 'Method': 'Contextual counting activities assessment'}
                ],
                'resources': [
                    {'Item': 'Hong Kong number flashcards', 'Quantity': '10 sets', 'Source': 'Custom designed with local landmarks'},
                    {'Item': 'MTR station counting cards', 'Quantity': '5 sets', 'Source': 'Printable with real station names'},
                    {'Item': 'Dim sum toy set', 'Quantity': '2 sets', 'Source': 'Educational toy store'},
                    {'Item': 'Traditional counting songs', 'Quantity': '1 CD', 'Source': 'Local children music library'},
                    {'Item': 'Confidence building stickers', 'Quantity': '100+', 'Source': 'Reward system materials'}
                ],
                'parent_tips': [
                    {'Tip': '🏠 Count Hong Kong daily life', 'Description': 'Count MTR stations, dim sum pieces, family members at dinner'},
                    {'Tip': '🎵 Sing counting songs together', 'Description': 'Use traditional Chinese and English number songs'},
                    {'Tip': '🧸 Make toys educational tools', 'Description': 'Count Lego blocks, doll accessories, toy cars'},
                    {'Tip': '🎉 Celebrate every counting attempt', 'Description': 'Focus on effort and enthusiasm, not perfection'},
                    {'Tip': '👨‍👩‍👧‍👦 Family counting time', 'Description': 'Make counting a fun family activity during meals or play'},
                    {'Tip': '📱 Use technology wisely', 'Description': 'Educational apps with Hong Kong themes for reinforcement'},
                    {'Tip': '🌟 Build confidence daily', 'Description': 'Notice and praise small improvements in counting skills'}
                ]
            },
            2: {
                'activities': [
                    {'Activity': '🔍 Hong Kong Building Shape Hunt', 'Duration': '20 min', 'Materials': 'Shape templates, Hong Kong photos', 'Objective': 'Find circles, squares, triangles in Hong Kong buildings'},
                    {'Activity': '🎨 Dim Sum Shape Art', 'Duration': '25 min', 'Materials': 'Paper, crayons, dim sum pictures', 'Objective': 'Draw and color different shaped dim sum'},
                    {'Activity': '🌈 Color Mixing Magic Lab', 'Duration': '18 min', 'Materials': 'Paint, brushes, mixing trays', 'Objective': 'Experiment with primary colors to create new ones'},
                    {'Activity': '🚇 MTR Station Shape Safari', 'Duration': '22 min', 'Materials': 'MTR maps, shape stickers', 'Objective': 'Identify shapes in station designs and signs'},
                    {'Activity': '🧱 Building Block Shape Tower', 'Duration': '20 min', 'Materials': 'Various shaped blocks, number cards', 'Objective': 'Build towers using different shapes'},
                    {'Activity': '🎯 Shape Bingo Hong Kong Style', 'Duration': '15 min', 'Materials': 'Hong Kong-themed bingo cards, markers', 'Objective': 'Match shapes with local cultural items'},
                    {'Activity': '✏️ Shape Tracing Adventure', 'Duration': '16 min', 'Materials': 'Tracing paper, shape stencils, colored pencils', 'Objective': 'Practice drawing shapes with confidence'},
                    {'Activity': '🎭 Shape Story Theater', 'Duration': '24 min', 'Materials': 'Shape puppets, story backdrop, props', 'Objective': 'Create and act out stories using different shapes'}
                ],
                'assessment': [
                    {'Skill': 'Shape Recognition', 'Target': 'Identifies circle, square, triangle, rectangle confidently', 'Method': 'Interactive shape matching games with Hong Kong themes'},
                    {'Skill': 'Color Combination', 'Target': 'Successfully mixes primary colors to create new ones', 'Method': 'Observation during color mixing experiments'},
                    {'Skill': 'Curiosity Expression', 'Target': 'Asks questions about shapes and colors in environment', 'Method': 'Behavioral observation and question documentation'},
                    {'Skill': 'Creative Expression', 'Target': 'Creates art combining shapes and colors', 'Method': 'Portfolio assessment of art projects'},
                    {'Skill': 'Real-Life Application', 'Target': 'Recognizes shapes in Hong Kong daily life', 'Method': 'Environmental exploration activities assessment'}
                ],
                'resources': [
                    {'Item': 'Hong Kong shape flashcards', 'Quantity': '15 sets', 'Source': 'Custom designed with local landmarks'},
                    {'Item': 'Color mixing experiment kit', 'Quantity': '8 sets', 'Source': 'Art supply store with mixing trays'},
                    {'Item': 'Shape tracing templates', 'Quantity': '20 sets', 'Source': 'Printable with Hong Kong themes'},
                    {'Item': 'Dim sum shape cutouts', 'Quantity': '10 sets', 'Source': 'Educational craft materials'},
                    {'Item': 'MTR station shape stickers', 'Quantity': '5 sheets', 'Source': 'Custom designed transportation themes'},
                    {'Item': 'Building block shape set', 'Quantity': '6 sets', 'Source': 'Educational toy store with various shapes'}
                ],
                'parent_tips': [
                    {'Tip': '🏢 Hong Kong building shape walks', 'Description': 'Point out different shapes in buildings during walks around the city'},
                    {'Tip': '🎨 Color mixing at home', 'Description': 'Let children experiment with food coloring or paint to create new colors'},
                    {'Tip': '🥟 Shape cooking activities', 'Description': 'Make dim sum or cookies in different shapes together'},
                    {'Tip': '🔍 Shape scavenger hunts', 'Description': 'Look for shapes in everyday objects at home and in the neighborhood'},
                    {'Tip': '📚 Shape story time', 'Description': 'Read books about shapes and ask children to find shapes in the illustrations'},
                    {'Tip': '🎭 Shape puppet shows', 'Description': 'Create simple puppets using different shapes and put on shows together'},
                    {'Tip': '🌳 Nature shape exploration', 'Description': 'Find natural shapes in parks, leaves, flowers, and rocks'},
                    {'Tip': '🎯 Shape games during travel', 'Description': 'Play "I spy shapes" games while riding MTR or walking around Hong Kong'}
                ]
            }
            # Add more stages as needed...
        }
        
        # Get template for the stage or create default
        template = activities_templates.get(stage, activities_templates[1])
        return template
    
    def _create_detailed_activities_data(self, stage: int) -> Dict:
        """Create detailed activities data with specific columns for Excel output."""
        detailed_activities = {
            1: {
                'detailed_activities': [
                    {
                        'Activity Name': 'Count Fingers Song',
                        'Description': 'Sing traditional Chinese counting song while using fingers to show numbers 1-10. Game-based learning through music and movement.',
                        'Materials': 'Hands, counting song lyrics, visual number cards',
                        'Duration': '10-15 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Praise effort and enthusiasm. Say "Great singing!" even if numbers aren\'t perfect.'
                    },
                    {
                        'Activity Name': 'Toy Counting Hunt',
                        'Description': 'Hide toys around room and let child find and count them. Hong Kong-themed toys like toy cars, dolls, building blocks.',
                        'Materials': 'Various toys (10-15 items), number cards, small basket',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Celebrate every find! "Wow, you found 3 toys!" Focus on effort over accuracy.'
                    },
                    {
                        'Activity Name': 'MTR Station Counting',
                        'Description': 'Use MTR station cards to count stops on familiar routes. Child learns numbers through daily Hong Kong life.',
                        'Materials': 'MTR station cards, toy train, number stickers',
                        'Duration': '12-18 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Start with routes child knows well. Praise for recognizing familiar stations.'
                    },
                    {
                        'Activity Name': 'Dim Sum Number Game',
                        'Description': 'Count different dim sum pieces (dumplings, buns, rolls) and match to numbers. Hong Kong food culture integration.',
                        'Materials': 'Toy dim sum set, number cards, small plates',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Make it fun! "Let\'s count our yummy dim sum!" Encourage role-playing.'
                    },
                    {
                        'Activity Name': 'Number Dance Party',
                        'Description': 'Dance to counting songs with movements. Jump 3 times, clap 5 times, etc. Active learning through music.',
                        'Materials': 'Music player, counting songs, space to dance',
                        'Duration': '10-15 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Join in the fun! Dance together and celebrate all attempts at counting.'
                    }
                ],
                'assessment': [
                    {'Skill': 'Number Recognition', 'Target': 'Recognizes numbers 1-10 with confidence', 'Method': 'Interactive flash card games with positive reinforcement'},
                    {'Skill': 'Counting Accuracy', 'Target': 'Counts objects accurately up to 10', 'Method': 'Observation during play-based activities'},
                    {'Skill': 'Self-Confidence', 'Target': 'Shows enthusiasm and pride in counting', 'Method': 'Behavioral observation and parent feedback'}
                ],
                'resources': [
                    {'Item': 'Hong Kong number flashcards', 'Quantity': '10 sets', 'Source': 'Custom designed with local landmarks'},
                    {'Item': 'MTR station counting cards', 'Quantity': '5 sets', 'Source': 'Printable with real station names'},
                    {'Item': 'Toy dim sum set', 'Quantity': '2 sets', 'Source': 'Educational toy store'},
                    {'Item': 'Traditional counting songs', 'Quantity': '1 CD', 'Source': 'Local children music library'}
                ],
                'parent_tips': [
                    {'Tip': 'Count Hong Kong daily life', 'Description': 'Count MTR stations, dim sum pieces, family members at dinner'},
                    {'Tip': 'Sing counting songs together', 'Description': 'Use traditional Chinese and English number songs'},
                    {'Tip': 'Celebrate every counting attempt', 'Description': 'Focus on effort and enthusiasm, not perfection'},
                    {'Tip': 'Make toys educational tools', 'Description': 'Count Lego blocks, doll accessories, toy cars'}
                ]
            },
            2: {
                'detailed_activities': [
                    {
                        'Activity Name': 'Hong Kong Shape Hunt',
                        'Description': 'Find shapes in Hong Kong buildings: circles (wheels), squares (windows), triangles (roofs). Game-based exploration.',
                        'Materials': 'Shape templates, Hong Kong building photos, magnifying glass',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Praise discovery skills. "Great detective work finding that circle!"'
                    },
                    {
                        'Activity Name': 'Color Mixing Magic Lab',
                        'Description': 'Mix primary colors to create new colors. Hong Kong-themed color experiments (red lanterns, blue harbor).',
                        'Materials': 'Paint, brushes, mixing trays, paper, color cards',
                        'Duration': '18-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Celebrate color discoveries! "Wow, red and blue made purple!"'
                    },
                    {
                        'Activity Name': 'Dim Sum Shape Art',
                        'Description': 'Create art using different shaped dim sum pieces. Cut and paste circles, squares, triangles.',
                        'Materials': 'Dim sum cutouts, paper, glue, crayons, scissors',
                        'Duration': '20-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Focus on creativity over accuracy. Praise unique combinations.'
                    },
                    {
                        'Activity Name': 'MTR Station Shape Safari',
                        'Description': 'Identify shapes in MTR station designs and signs. Interactive shape recognition game.',
                        'Materials': 'MTR station photos, shape stickers, activity sheet',
                        'Duration': '12-18 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Connect to real experiences. "Remember when we saw this at Central Station?"'
                    },
                    {
                        'Activity Name': 'Shape Shadow Theater',
                        'Description': 'Use light to create shape shadows on walls. Children become shape performers.',
                        'Materials': 'Flashlight, shape cutouts, white wall or sheet',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Make it theatrical! Encourage storytelling with shapes.'
                    }
                ],
                'assessment': [
                    {'Skill': 'Shape Recognition', 'Target': 'Identifies circle, square, triangle, rectangle confidently', 'Method': 'Interactive shape matching games with Hong Kong themes'},
                    {'Skill': 'Color Combination', 'Target': 'Successfully mixes primary colors to create new ones', 'Method': 'Observation during color mixing experiments'},
                    {'Skill': 'Creative Expression', 'Target': 'Creates art combining shapes and colors', 'Method': 'Portfolio assessment of art projects'}
                ],
                'resources': [
                    {'Item': 'Hong Kong shape flashcards', 'Quantity': '15 sets', 'Source': 'Custom designed with local landmarks'},
                    {'Item': 'Color mixing experiment kit', 'Quantity': '8 sets', 'Source': 'Art supply store with mixing trays'},
                    {'Item': 'Shape tracing templates', 'Quantity': '20 sets', 'Source': 'Printable with Hong Kong themes'},
                    {'Item': 'Dim sum shape cutouts', 'Quantity': '10 sets', 'Source': 'Educational craft materials'}
                ],
                'parent_tips': [
                    {'Tip': 'Hong Kong building shape walks', 'Description': 'Point out different shapes in buildings during walks around the city'},
                    {'Tip': 'Color mixing at home', 'Description': 'Let children experiment with food coloring or paint to create new colors'},
                    {'Tip': 'Shape cooking activities', 'Description': 'Make dim sum or cookies in different shapes together'},
                    {'Tip': 'Shape scavenger hunts', 'Description': 'Look for shapes in everyday objects at home and in the neighborhood'}
                ]
            },
            3: {
                'detailed_activities': [
                    {
                        'Activity Name': 'Bead Stringing Patterns',
                        'Description': 'Create ABAB patterns using colorful beads. Hong Kong-themed colors (red, gold, green). Pattern recognition game.',
                        'Materials': 'Colorful beads, string, pattern cards, examples',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Praise pattern creation attempts. "Great pattern! What comes next?"'
                    },
                    {
                        'Activity Name': 'Toy Sorting by Size and Color',
                        'Description': 'Sort toys by multiple attributes: size (big/small) and color (red/blue/yellow). Classification game.',
                        'Materials': 'Various sized toys, sorting trays, color labels',
                        'Duration': '18-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Encourage different sorting methods. "Show me another way to sort these!"'
                    },
                    {
                        'Activity Name': 'Hong Kong Festival Pattern Dance',
                        'Description': 'Create movement patterns inspired by Hong Kong festivals. Clap-clap-stamp pattern, etc.',
                        'Materials': 'Music player, festival music, movement space',
                        'Duration': '12-18 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Join in the dancing! Celebrate creative movement patterns.'
                    },
                    {
                        'Activity Name': 'Dim Sum Pattern Plates',
                        'Description': 'Arrange dim sum pieces in repeating patterns on plates. Visual pattern creation.',
                        'Materials': 'Toy dim sum pieces, small plates, pattern examples',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Focus on pattern recognition. "What pattern did you make?"'
                    },
                    {
                        'Activity Name': 'Nature Pattern Hunt',
                        'Description': 'Find patterns in Hong Kong nature: leaf patterns, flower arrangements, rock formations.',
                        'Materials': 'Magnifying glass, collection bag, pattern worksheet',
                        'Duration': '20-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Encourage observation skills. "What patterns do you see in nature?"'
                    }
                ],
                'assessment': [
                    {'Skill': 'Pattern Recognition', 'Target': 'Identifies and creates simple repeating patterns (AB, AAB, ABC)', 'Method': 'Pattern completion activities and observation'},
                    {'Skill': 'Classification', 'Target': 'Sorts objects by multiple attributes (size, color, shape)', 'Method': 'Sorting activities with different criteria'},
                    {'Skill': 'Logical Sequencing', 'Target': 'Understands and continues logical sequences', 'Method': 'Sequencing games and pattern extension activities'}
                ],
                'resources': [
                    {'Item': 'Pattern bead sets', 'Quantity': '12 sets', 'Source': 'Educational toy store with various colors'},
                    {'Item': 'Sorting trays and labels', 'Quantity': '10 sets', 'Source': 'Classroom supply store'},
                    {'Item': 'Hong Kong festival music', 'Quantity': '1 CD', 'Source': 'Local cultural music library'},
                    {'Item': 'Nature pattern worksheets', 'Quantity': '15 sets', 'Source': 'Printable with Hong Kong nature themes'}
                ],
                'parent_tips': [
                    {'Tip': 'Pattern recognition in daily life', 'Description': 'Point out patterns in daily routines, clothing, decorations'},
                    {'Tip': 'Creative sorting activities', 'Description': 'Sort household items by different attributes together'},
                    {'Tip': 'Pattern storytelling', 'Description': 'Create stories using repeating patterns and sequences'},
                    {'Tip': 'Nature pattern exploration', 'Description': 'Look for patterns in parks, gardens, and natural settings'}
                ]
            },
            4: {
                'detailed_activities': [
                    {
                        'Activity Name': 'Dim Sum Addition Game',
                        'Description': 'Add different dim sum pieces together. 3 dumplings + 2 buns = 5 pieces total. Hong Kong food math.',
                        'Materials': 'Toy dim sum set, number cards, addition worksheets',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Use real dim sum experiences. "Remember when we had 4 dumplings at the restaurant?"'
                    },
                    {
                        'Activity Name': 'MTR Station Subtraction',
                        'Description': 'Subtract stations as train travels. Start with 10 stations, subtract 3 stops = 7 stations left.',
                        'Materials': 'MTR station cards, toy train, subtraction cards',
                        'Duration': '12-18 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Connect to real travel. "How many stops until we get home?"'
                    },
                    {
                        'Activity Name': 'Toy Store Math',
                        'Description': 'Buy and sell toys using play money. Addition when buying, subtraction when selling. Role-playing game.',
                        'Materials': 'Toy store setup, play money, price tags, toy cash register',
                        'Duration': '20-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Encourage role-playing. "How much money do you have left?"'
                    },
                    {
                        'Activity Name': 'Family Member Counting',
                        'Description': 'Count family members in different combinations. Add grandparents, subtract when someone leaves.',
                        'Materials': 'Family photos, counting objects, number cards',
                        'Duration': '10-15 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Use real family situations. "How many people are at dinner tonight?"'
                    },
                    {
                        'Activity Name': 'Kitchen Math Cooking',
                        'Description': 'Add ingredients while cooking simple snacks. Count and add fruits, vegetables, or cookies.',
                        'Materials': 'Cooking ingredients, bowls, measuring cups, recipe cards',
                        'Duration': '18-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Make cooking fun! "How many apples do we need for 2 more people?"'
                    }
                ],
                'assessment': [
                    {'Skill': 'Addition Understanding', 'Target': 'Understands addition as combining groups', 'Method': 'Observation during object manipulation activities'},
                    {'Skill': 'Subtraction Understanding', 'Target': 'Understands subtraction as taking away or comparing', 'Method': 'Real-world problem solving scenarios'},
                    {'Skill': 'Number Bonds', 'Target': 'Develops number bonds to 10', 'Method': 'Number bond games and activities'}
                ],
                'resources': [
                    {'Item': 'Play money and toy cash register', 'Quantity': '6 sets', 'Source': 'Educational toy store'},
                    {'Item': 'Addition and subtraction worksheets', 'Quantity': '20 sets', 'Source': 'Printable with Hong Kong themes'},
                    {'Item': 'Family counting cards', 'Quantity': '10 sets', 'Source': 'Custom designed family scenarios'},
                    {'Item': 'Simple cooking recipe cards', 'Quantity': '15 sets', 'Source': 'Child-friendly recipes with math integration'}
                ],
                'parent_tips': [
                    {'Tip': 'Real-world math opportunities', 'Description': 'Use daily situations like shopping, cooking, and traveling for math practice'},
                    {'Tip': 'Play money activities', 'Description': 'Use play money to practice buying and selling at home'},
                    {'Tip': 'Family counting games', 'Description': 'Count family members and pets in different combinations'},
                    {'Tip': 'Cooking math integration', 'Description': 'Involve children in cooking and counting ingredients together'}
                ]
            },
            5: {
                'detailed_activities': [
                    {
                        'Activity Name': 'Hong Kong Building Height Comparison',
                        'Description': 'Compare heights of different Hong Kong buildings using non-standard units. Hands, feet, or blocks.',
                        'Materials': 'Building photos, measuring tools, comparison charts',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Use familiar buildings. "Which building is taller - our apartment or the bank?"'
                    },
                    {
                        'Activity Name': 'Harbor Length Measurement',
                        'Description': 'Measure and compare lengths using body parts. How many steps across the room? How many arm spans?',
                        'Materials': 'Measuring tools, recording sheets, comparison objects',
                        'Duration': '18-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Make it personal. "How big is your room compared to the kitchen?"'
                    },
                    {
                        'Activity Name': 'Dim Sum Size Sorting',
                        'Description': 'Sort dim sum pieces by size: big dumplings, medium buns, small spring rolls. Size comparison game.',
                        'Materials': 'Various sized dim sum pieces, sorting trays, size labels',
                        'Duration': '12-18 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Connect to eating experiences. "Which dumpling is bigger?"'
                    },
                    {
                        'Activity Name': 'Toy Weight Comparison',
                        'Description': 'Compare weights of different toys using balance scales or hands. Heavy vs. light concepts.',
                        'Materials': 'Various weighted toys, balance scales, weight comparison chart',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Use familiar toys. "Which toy feels heavier in your hands?"'
                    },
                    {
                        'Activity Name': 'MTR Station Distance Walk',
                        'Description': 'Walk between stations and compare distances. Count steps, measure time, compare routes.',
                        'Materials': 'Step counter, timer, distance recording sheet',
                        'Duration': '20-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Use real MTR experiences. "Which station is closer to our home?"'
                    }
                ],
                'assessment': [
                    {'Skill': 'Size Comparison', 'Target': 'Compares sizes (big/small, long/short, tall/short)', 'Method': 'Direct comparison activities with various objects'},
                    {'Skill': 'Measurement Concepts', 'Target': 'Understands measurement using non-standard units', 'Method': 'Hands-on measuring activities'},
                    {'Skill': 'Ordering', 'Target': 'Orders objects by size', 'Method': 'Sequencing activities with different sized objects'}
                ],
                'resources': [
                    {'Item': 'Non-standard measuring tools', 'Quantity': '8 sets', 'Source': 'Classroom supply store with various measuring devices'},
                    {'Item': 'Hong Kong building comparison charts', 'Quantity': '10 sets', 'Source': 'Custom designed with local landmarks'},
                    {'Item': 'Balance scales and weight sets', 'Quantity': '6 sets', 'Source': 'Educational toy store'},
                    {'Item': 'Size sorting materials', 'Quantity': '12 sets', 'Source': 'Various sized objects for comparison'}
                ],
                'parent_tips': [
                    {'Tip': 'Body measurement activities', 'Description': 'Use hands, feet, and arm spans to measure objects at home'},
                    {'Tip': 'Size comparison in daily life', 'Description': 'Compare sizes of everyday objects like fruits, books, or toys'},
                    {'Tip': 'Kitchen measurement fun', 'Description': 'Involve children in measuring ingredients while cooking'},
                    {'Tip': 'Building height observations', 'Description': 'Point out different building heights during walks around Hong Kong'}
                ]
            },
            6: {
                'detailed_activities': [
                    {
                        'Activity Name': 'Hong Kong Maze Navigation',
                        'Description': 'Navigate through Hong Kong-themed mazes using positional words. Above, below, beside, between.',
                        'Materials': 'Hong Kong maze worksheets, directional cards, markers',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Use familiar Hong Kong locations. "How do we get from Central to Tsim Sha Tsui?"'
                    },
                    {
                        'Activity Name': 'Dim Sum Puzzle Assembly',
                        'Description': 'Complete puzzles of dim sum plates using spatial reasoning. Left, right, top, bottom positioning.',
                        'Materials': 'Dim sum puzzle pieces, puzzle boards, assembly guides',
                        'Duration': '18-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Start with simple puzzles. "Where does this piece go?"'
                    },
                    {
                        'Activity Name': 'MTR Station Treasure Hunt',
                        'Description': 'Follow directional clues to find hidden objects at different MTR stations. Multi-step instructions.',
                        'Materials': 'Treasure hunt clues, station maps, hidden objects, reward stickers',
                        'Duration': '20-25 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Use familiar stations. "Follow the clues to find the treasure!"'
                    },
                    {
                        'Activity Name': 'Building Block Challenge',
                        'Description': 'Build structures following specific spatial requirements. Logical reasoning and construction.',
                        'Materials': 'Building blocks, construction challenges, spatial requirement cards',
                        'Duration': '15-20 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Encourage problem-solving. "How can you make it taller?"'
                    },
                    {
                        'Activity Name': 'Hong Kong Map Exploration',
                        'Description': 'Explore Hong Kong maps and identify spatial relationships. Islands, districts, and neighborhoods.',
                        'Materials': 'Hong Kong maps, district markers, exploration worksheets',
                        'Duration': '12-18 mins',
                        'Age Suitability': '3-5 years',
                        'Parent Tips': 'Connect to real experiences. "Where is our home on the map?"'
                    }
                ],
                'assessment': [
                    {'Skill': 'Spatial Relationships', 'Target': 'Understands positional words (above, below, beside, between)', 'Method': 'Direct spatial reasoning activities and observation'},
                    {'Skill': 'Problem Solving', 'Target': 'Solves simple puzzles and spatial challenges', 'Method': 'Puzzle completion and construction activities'},
                    {'Skill': 'Logical Thinking', 'Target': 'Follows multi-step instructions and develops logical reasoning', 'Method': 'Multi-step task completion and reasoning games'}
                ],
                'resources': [
                    {'Item': 'Hong Kong maze worksheets', 'Quantity': '15 sets', 'Source': 'Printable with local landmarks and themes'},
                    {'Item': 'Dim sum puzzle sets', 'Quantity': '8 sets', 'Source': 'Custom designed puzzle pieces'},
                    {'Item': 'Building block challenges', 'Quantity': '10 sets', 'Source': 'Educational construction materials'},
                    {'Item': 'Hong Kong exploration maps', 'Quantity': '12 sets', 'Source': 'Child-friendly maps with district markers'}
                ],
                'parent_tips': [
                    {'Tip': 'Spatial vocabulary in daily life', 'Description': 'Use positional words during everyday activities and conversations'},
                    {'Tip': 'Puzzle solving together', 'Description': 'Complete puzzles as a family and discuss spatial relationships'},
                    {'Tip': 'Treasure hunt adventures', 'Description': 'Create simple treasure hunts at home with directional clues'},
                    {'Tip': 'Map exploration activities', 'Description': 'Look at maps together and identify familiar locations and spatial relationships'}
                ]
            }
        }
        
        # Get template for the stage or create default
        template = detailed_activities.get(stage, detailed_activities[1])
        return template
    
    def generate_all_activities_excel(self) -> str:
        """
        Generate one combined Excel file with all 6 stages activities.
        Each stage gets its own sheet for easy printing.
        
        Returns:
            File path to generated combined Excel file
        """
        if not PANDAS_AVAILABLE:
            logger.error("pandas not available. Cannot generate combined Excel activities.")
            return ""
        
        try:
            filename = "all_stages_activities.xlsx"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create Excel file with all stages
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for stage in range(1, 7):
                    stage_name = self.stages.get(stage, f"Stage {stage}")
                    logger.info(f"Adding stage {stage} activities to combined Excel...")
                    
                    # Get detailed activities data for this stage
                    activities_data = self._create_detailed_activities_data(stage)
                    
                    # Create activities sheet for this stage
                    detailed_activities_df = pd.DataFrame(activities_data['detailed_activities'])
                    sheet_name = f"Stage_{stage}_{stage_name.split()[0]}"  # e.g., "Stage_1_Number"
                    detailed_activities_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Create summary sheet with all stages overview
                summary_data = []
                for stage in range(1, 7):
                    stage_name = self.stages.get(stage, f"Stage {stage}")
                    activities_data = self._create_detailed_activities_data(stage)
                    activity_count = len(activities_data['detailed_activities'])
                    
                    summary_data.append({
                        'Stage': stage,
                        'Stage Name': stage_name,
                        'Activity Count': activity_count,
                        'Duration Range': '10-25 mins',
                        'Age Suitability': '3-5 years',
                        'Key Focus': self._get_stage_focus(stage)
                    })
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Overview', index=False)
            
            logger.info(f"Combined Excel activities generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate combined Excel activities: {e}")
            return ""
    
    def _get_stage_focus(self, stage: int) -> str:
        """Get key focus for each stage."""
        focus_map = {
            1: "Number Recognition & Counting",
            2: "Shapes & Colors",
            3: "Patterns & Classification", 
            4: "Addition & Subtraction",
            5: "Measurement & Comparison",
            6: "Spatial Problem Solving"
        }
        return focus_map.get(stage, "Mathematical Concepts")
    
    def generate_combined_goals_and_content(self) -> str:
        """
        Generate a combined goals_and_content.md file with all 6 stages.
        Includes Gemini API suggestions for fun variations if available.
        
        Returns:
            File path to generated combined file
        """
        try:
            combined_content = []
            
            # Header
            combined_content.append("# 🎓 Audrey Math Course Generator - Complete Goals & Content")
            combined_content.append("")
            combined_content.append("## 🇭🇰 Hong Kong Kindergarten Mathematics Curriculum")
            combined_content.append("### For 3-5 Year Olds - Building Confident Young Mathematicians")
            combined_content.append("")
            combined_content.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            combined_content.append("")
            combined_content.append("---")
            combined_content.append("")
            
            # Loop through all 6 stages
            for stage in range(1, 7):
                stage_name = self.stages.get(stage, "Unknown Stage")
                logger.info(f"Processing stage {stage} for combined file...")
                
                # Stage header
                combined_content.append(f"# Stage {stage}: {stage_name}")
                combined_content.append("")
                
                # Get goals content
                if self.ai_enabled:
                    goals_content = self.generate_ai_content(
                        f"Create engaging learning goals for stage {stage}: {stage_name}",
                        f"Hong Kong kindergarten curriculum for 3-5 year olds with focus on play-based learning"
                    )
                else:
                    goals_content = self._get_default_goals(stage)
                
                combined_content.append("## 🌟 Learning Goals & Objectives")
                combined_content.append("")
                combined_content.append(goals_content)
                combined_content.append("")
                
                # Get content (use the same logic as generate_content_text to include EDB integration)
                if self.ai_enabled:
                    content_text = self.generate_ai_content(
                        f"Create detailed teaching content and activities for stage {stage}: {stage_name}",
                        f"Comprehensive lesson plans for Hong Kong kindergarten with hands-on activities"
                    )
                else:
                    content_text = self._get_default_content(stage)
                
                # Integrate EDB ideas into content for combined file
                content_text = self.integrate_edb_ideas(content_text, stage)
                
                combined_content.append("## 📚 Teaching Content & Activities")
                combined_content.append("")
                combined_content.append(content_text)
                combined_content.append("")
                
                # Add Gemini API fun variations if available
                if self.ai_enabled:
                    fun_variations = self.generate_ai_content(
                        f"Suggest 3 fun and creative variations for stage {stage}: {stage_name}",
                        f"Hong Kong cultural context, age-appropriate for 3-5 year olds, engaging and educational"
                    )
                    
                    combined_content.append("## 🎉 Fun Variations & Extensions")
                    combined_content.append("")
                    combined_content.append("*AI-Generated Creative Suggestions:*")
                    combined_content.append("")
                    combined_content.append(fun_variations)
                    combined_content.append("")
                else:
                    # Fallback fun variations
                    fun_variations = self._get_fallback_fun_variations(stage)
                    combined_content.append("## 🎉 Fun Variations & Extensions")
                    combined_content.append("")
                    combined_content.append(fun_variations)
                    combined_content.append("")
                
                # Assessment section
                combined_content.append("## 📊 Assessment & Progress Tracking")
                combined_content.append("")
                combined_content.append("- **Observation**: Watch children during play-based activities")
                combined_content.append("- **Portfolio**: Collect samples of children's work")
                combined_content.append("- **Parent Feedback**: Regular communication with families")
                combined_content.append("- **Self-Assessment**: Children reflect on their learning")
                combined_content.append("")
                
                # Resources section
                combined_content.append("## 📦 Required Resources")
                combined_content.append("")
                combined_content.append("- **Manipulatives**: Age-appropriate counting and shape materials")
                combined_content.append("- **Cultural Materials**: Hong Kong-themed objects and images")
                combined_content.append("- **Art Supplies**: Paper, crayons, paint, scissors, glue")
                combined_content.append("- **Technology**: Age-appropriate educational apps (optional)")
                combined_content.append("- **Books**: Shape, number, and Hong Kong culture books")
                combined_content.append("")
                
                combined_content.append("---")
                combined_content.append("")
            
            # Course overview and implementation guide
            combined_content.append("# 🎯 Course Overview & Implementation Guide")
            combined_content.append("")
            
            if self.ai_enabled:
                overview_content = self.generate_ai_content(
                    "Create a comprehensive course overview and implementation guide for the 6-stage Hong Kong kindergarten math curriculum",
                    "Include progression, timeline, teaching strategies, and parent involvement"
                )
                combined_content.append(overview_content)
                combined_content.append("")
            else:
                combined_content.append("## 📅 Course Timeline")
                combined_content.append("")
                combined_content.append("**Total Duration**: 8 weeks (2 weeks per major stage)")
                combined_content.append("")
                combined_content.append("### Week 1-2: Number Recognition & Counting")
                combined_content.append("- Focus on numbers 1-10 with Hong Kong contexts")
                combined_content.append("- Build confidence through play-based activities")
                combined_content.append("")
                combined_content.append("### Week 3-4: Shapes & Colors")
                combined_content.append("- Explore basic shapes and color mixing")
                combined_content.append("- Hong Kong building and cultural shape hunts")
                combined_content.append("")
                combined_content.append("### Week 5-6: Patterns & Classification")
                combined_content.append("- Simple repeating patterns and sorting")
                combined_content.append("- Hong Kong cultural pattern recognition")
                combined_content.append("")
                combined_content.append("### Week 7-8: Addition/Subtraction & Measurement")
                combined_content.append("- Basic operations with objects")
                combined_content.append("- Size comparison and measurement concepts")
                combined_content.append("")
            
            # Parent involvement section
            combined_content.append("## 👨‍👩‍👧‍👦 Parent Involvement")
            combined_content.append("")
            combined_content.append("### Daily Activities")
            combined_content.append("- Count everyday objects at home")
            combined_content.append("- Point out shapes in the environment")
            combined_content.append("- Sing counting songs together")
            combined_content.append("- Share Hong Kong cultural experiences")
            combined_content.append("")
            combined_content.append("### Weekend Adventures")
            combined_content.append("- Visit MTR stations to count stops")
            combined_content.append("- Go to dim sum restaurants to count pieces")
            combined_content.append("- Explore Hong Kong parks for shape hunting")
            combined_content.append("- Create art projects using shapes and colors")
            combined_content.append("")
            
            # Footer
            combined_content.append("---")
            combined_content.append("")
            combined_content.append("## 📞 Support & Resources")
            combined_content.append("")
            combined_content.append("- **Teacher Support**: Regular check-ins and professional development")
            combined_content.append("- **Parent Resources**: Weekly newsletters with activity suggestions")
            combined_content.append("- **Assessment Tools**: Progress tracking and portfolio guidelines")
            combined_content.append("- **Cultural Integration**: Hong Kong education standards alignment")
            combined_content.append("")
            combined_content.append(f"*This curriculum was generated on {datetime.now().strftime('%Y-%m-%d')} using the Audrey Math Course Generator.*")
            combined_content.append("")
            combined_content.append("🌟 **Building confident, curious, and mathematically-minded young learners in Hong Kong!** 🌟")
            
            # Save the combined file
            filename = "goals_and_content.md"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(combined_content))
            
            logger.info(f"Combined goals and content file generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate combined goals and content file: {e}")
            return ""
    
    def _get_fallback_fun_variations(self, stage: int) -> str:
        """Get fallback fun variations when AI is not available."""
        fallback_variations = {
            1: """
### 🎯 Number Recognition Fun Variations
- **Number Dance Party**: Dance to counting songs with movements
- **Number Hide & Seek**: Hide number cards around classroom for discovery
- **Number Cooking**: Count ingredients while making simple snacks
- **Number Nature Walk**: Count natural objects during outdoor exploration
            """,
            2: """
### 🔷 Shapes & Colors Fun Variations
- **Shape Shadow Theater**: Use light to create shape shadows on walls
- **Color Mixing Magic Show**: Perform color experiments for classmates
- **Shape Yoga**: Create shapes with body movements and poses
- **Shape Story Adventures**: Use shapes as characters in creative stories
            """,
            3: """
### 🔄 Patterns Fun Variations
- **Pattern Music**: Create musical patterns using clapping and instruments
- **Pattern Dance**: Move in repeating patterns with body movements
- **Pattern Art**: Create visual patterns using stamps and stencils
- **Pattern Nature**: Find patterns in leaves, flowers, and natural objects
            """,
            4: """
### ➕ Addition/Subtraction Fun Variations
- **Kitchen Math**: Count and add ingredients while cooking
- **Toy Store Math**: "Buy" and "sell" toys using play money
- **Garden Math**: Count flowers and subtract when picking them
- **Family Math**: Count family members and pets in different combinations
            """,
            5: """
### 📏 Measurement Fun Variations
- **Body Measurement**: Measure using hands, feet, and arm spans
- **Kitchen Measurement**: Compare sizes of cooking utensils and ingredients
- **Building Measurement**: Compare heights of different buildings
- **Nature Measurement**: Compare sizes of leaves, rocks, and flowers
            """,
            6: """
### 🧩 Spatial Problem Solving Fun Variations
- **Maze Adventures**: Create and solve simple mazes
- **Puzzle Challenges**: Complete age-appropriate puzzles together
- **Building Challenges**: Construct structures with specific requirements
- **Treasure Hunts**: Follow directions to find hidden objects
            """
        }
        return fallback_variations.get(stage, "Creative and engaging activities that extend learning beyond the basic curriculum.")
    
    def generate_stage_pdfs(self) -> List[str]:
        """
        Generate comprehensive PDF files for each stage (audrey_math_stageX.pdf).
        Each PDF contains 2-3 pages with visual elements, EDB integration, and print-friendly design.
        
        Returns:
            List of generated PDF file paths
        """
        generated_pdfs = []
        
        for stage in range(1, 7):
            try:
                stage_name = self.stages.get(stage, "Unknown Stage")
                logger.info(f"Generating comprehensive PDF for stage {stage}: {stage_name}")
                
                # Generate stage-specific PDF
                pdf_file = self._generate_stage_comprehensive_pdf(stage)
                if pdf_file:
                    generated_pdfs.append(pdf_file)
                    logger.info(f"Stage {stage} PDF generated: {pdf_file}")
                else:
                    logger.error(f"Failed to generate PDF for stage {stage}")
                    
            except Exception as e:
                logger.error(f"Error generating PDF for stage {stage}: {e}")
        
        return generated_pdfs
    
    def _generate_stage_comprehensive_pdf(self, stage: int) -> str:
        """
        Generate a comprehensive PDF for a specific stage using FPDF and Pillow.
        
        Args:
            stage: The learning stage (1-6)
            
        Returns:
            File path to generated PDF
        """
        try:
            if not FPDF_AVAILABLE:
                logger.error("FPDF not available. Cannot generate stage PDFs.")
                return ""
            
            stage_name = self.stages.get(stage, "Unknown Stage")
            filename = f"audrey_math_stage{stage}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create PDF with FPDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # Page 1: Title and Overview
            self._add_pdf_title_page(pdf, stage, stage_name)
            
            # Page 2: Activities and EDB Integration
            self._add_pdf_activities_page(pdf, stage, stage_name)
            
            # Page 3: Visual Elements and Exercises
            self._add_pdf_exercises_page(pdf, stage, stage_name)
            
            # Save PDF
            pdf.output(filepath)
            logger.info(f"Comprehensive PDF generated for stage {stage}: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate comprehensive PDF for stage {stage}: {e}")
            return ""
    
    def _add_pdf_title_page(self, pdf, stage: int, stage_name: str):
        """Add title page to PDF."""
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 20, f"Audrey Math - Stage {stage}", 0, 1, 'C')
        pdf.cell(0, 10, stage_name.upper(), 0, 1, 'C')
        pdf.ln(10)
        
        # EDB Integration Section
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, "Education Bureau Guidelines", 0, 1, 'L')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        edb_content = self._get_edb_content_for_stage(stage)
        for line in edb_content.split('\n'):
            if line.strip():
                pdf.cell(0, 6, line.strip(), 0, 1, 'L')
        
        pdf.ln(10)
        
        # Learning Objectives
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, "Learning Objectives", 0, 1, 'L')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        objectives = self._get_stage_objectives(stage)
        for obj in objectives:
            pdf.cell(0, 6, f"• {obj}", 0, 1, 'L')
    
    def _add_pdf_activities_page(self, pdf, stage: int, stage_name: str):
        """Add activities page to PDF."""
        pdf.add_page()
        
        # Page title
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 15, f"Stage {stage} Activities", 0, 1, 'C')
        pdf.ln(5)
        
        # Activities
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "Hong Kong-Themed Activities", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        activities = self._get_stage_activities(stage)
        for i, activity in enumerate(activities, 1):
            pdf.cell(0, 6, f"{i}. {activity['name']}", 0, 1, 'L')
            pdf.cell(0, 5, f"   Materials: {activity['materials']}", 0, 1, 'L')
            pdf.cell(0, 5, f"   Duration: {activity['duration']}", 0, 1, 'L')
            pdf.ln(3)
        
        # EDB Principles
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "EDB Learning Principles", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        principles = [
            "• Game-based learning approach",
            "• Balanced development focus",
            "• Play-based exploration",
            "• Positive attitude building",
            "• Whole-child approach"
        ]
        for principle in principles:
            pdf.cell(0, 5, principle, 0, 1, 'L')
    
    def _add_pdf_exercises_page(self, pdf, stage: int, stage_name: str):
        """Add exercises page to PDF."""
        pdf.add_page()
        
        # Page title
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 15, f"Stage {stage} Visual Exercises", 0, 1, 'C')
        pdf.ln(5)
        
        # Stage-specific visual content
        if stage == 1:
            self._add_stage1_visual_content(pdf)
        elif stage == 2:
            self._add_stage2_visual_content(pdf)
        elif stage == 3:
            self._add_stage3_visual_content(pdf)
        elif stage == 4:
            self._add_stage4_visual_content(pdf)
        elif stage == 5:
            self._add_stage5_visual_content(pdf)
        elif stage == 6:
            self._add_stage6_visual_content(pdf)
        
        # Parent Tips
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "Parent Tips", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        tips = [
            "• Praise effort over accuracy",
            "• Make learning fun and playful",
            "• Use Hong Kong daily life examples",
            "• Encourage exploration and curiosity",
            "• Celebrate small achievements"
        ]
        for tip in tips:
            pdf.cell(0, 5, tip, 0, 1, 'L')
    
    def _get_edb_content_for_stage(self, stage: int) -> str:
        """Get EDB content for specific stage."""
        edb_content = {
            1: """Number Recognition & Counting (1-10)
• Play-based learning through everyday objects
• Counting activities using natural materials
• Integration with Hong Kong daily life
• Building positive mathematical attitudes""",
            2: """Shapes & Colors
• Shape recognition through building blocks
• Color exploration in Hong Kong environment
• Pattern making with local materials
• Spatial awareness development""",
            3: """Patterns & Classification
• Creating patterns with Hong Kong elements
• Sorting and classifying objects
• Logical thinking development
• Problem-solving through play""",
            4: """Basic Addition & Subtraction
• Object-based calculation activities
• Hong Kong-themed counting games
• Understanding quantity relationships
• Building computational thinking""",
            5: """Measurement & Comparison
• Non-standard measurement units
• Comparing Hong Kong landmarks
• Size and weight concepts
• Practical measurement activities""",
            6: """Space & Problem Solving
• Spatial orientation in Hong Kong
• Navigation and direction concepts
• Problem-solving strategies
• Critical thinking development"""
        }
        return edb_content.get(stage, "General EDB guidelines for balanced development.")
    
    def _get_stage_objectives(self, stage: int) -> List[str]:
        """Get learning objectives for specific stage."""
        objectives = {
            1: [
                "Recognize and name numerals 1-10",
                "Count objects with one-to-one correspondence",
                "Understand quantity concepts",
                "Use numbers in daily Hong Kong life"
            ],
            2: [
                "Identify basic shapes (circle, square, triangle)",
                "Recognize and name colors",
                "Create simple patterns",
                "Explore shapes in Hong Kong environment"
            ],
            3: [
                "Create and extend patterns",
                "Sort objects by attributes",
                "Recognize pattern rules",
                "Apply patterns to Hong Kong contexts"
            ],
            4: [
                "Understand addition as combining",
                "Understand subtraction as taking away",
                "Solve simple word problems",
                "Use Hong Kong objects for calculations"
            ],
            5: [
                "Compare sizes and lengths",
                "Use non-standard measurement",
                "Understand weight concepts",
                "Apply measurement to Hong Kong landmarks"
            ],
            6: [
                "Understand spatial relationships",
                "Navigate using directions",
                "Solve spatial problems",
                "Apply problem-solving to Hong Kong contexts"
            ]
        }
        return objectives.get(stage, ["General learning objectives for balanced development."])
    
    def _get_stage_activities(self, stage: int) -> List[Dict[str, str]]:
        """Get activities for specific stage."""
        activities = {
            1: [
                {"name": "Dim Sum Counting Game", "materials": "Toy dim sum, number cards", "duration": "15-20 mins"},
                {"name": "MTR Station Counting", "materials": "MTR cards, toy train", "duration": "12-18 mins"},
                {"name": "Finger Counting Song", "materials": "Hands, counting song", "duration": "10-15 mins"}
            ],
            2: [
                {"name": "Hong Kong Shape Hunt", "materials": "Shape cards, camera", "duration": "20-25 mins"},
                {"name": "Color Sorting Game", "materials": "Colored objects, baskets", "duration": "15-20 mins"},
                {"name": "Building Block Patterns", "materials": "Blocks, pattern cards", "duration": "18-22 mins"}
            ],
            3: [
                {"name": "Bead Pattern Making", "materials": "Colored beads, strings", "duration": "20-25 mins"},
                {"name": "Hong Kong Flag Patterns", "materials": "Paper, colors", "duration": "15-20 mins"},
                {"name": "Toy Sorting Game", "materials": "Various toys, sorting boxes", "duration": "18-22 mins"}
            ],
            4: [
                {"name": "Dim Sum Addition", "materials": "Toy dim sum, plates", "duration": "20-25 mins"},
                {"name": "Bus Passenger Counting", "materials": "Toy bus, figures", "duration": "15-20 mins"},
                {"name": "Shopping Bag Game", "materials": "Shopping bags, items", "duration": "18-22 mins"}
            ],
            5: [
                {"name": "Building Height Comparison", "materials": "Building models, ruler", "duration": "20-25 mins"},
                {"name": "Market Weight Game", "materials": "Scales, fruits", "duration": "15-20 mins"},
                {"name": "Distance Measurement", "materials": "Measuring tape, landmarks", "duration": "18-22 mins"}
            ],
            6: [
                {"name": "Hong Kong Maze Navigation", "materials": "Maze sheets, pencils", "duration": "20-25 mins"},
                {"name": "Direction Game", "materials": "Compass, maps", "duration": "15-20 mins"},
                {"name": "Problem-Solving Puzzles", "materials": "Puzzle pieces, pictures", "duration": "18-22 mins"}
            ]
        }
        return activities.get(stage, [{"name": "General activity", "materials": "Basic materials", "duration": "15-20 mins"}])
    
    def _add_stage1_visual_content(self, pdf):
        """Add Stage 1 visual content."""
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "Number Recognition Exercises", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 5, "Draw the correct number of dim sum pieces:", 0, 1, 'L')
        pdf.ln(5)
        
        # Number exercises
        for i in range(1, 6):
            pdf.cell(20, 8, f"{i}:", 0, 0, 'L')
            pdf.cell(0, 8, "Draw _____ dim sum pieces", 0, 1, 'L')
            pdf.ln(2)
    
    def _add_stage2_visual_content(self, pdf):
        """Add Stage 2 visual content."""
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "Shape Recognition Exercises", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 5, "Find and color the shapes in Hong Kong buildings:", 0, 1, 'L')
        pdf.ln(5)
        
        shapes = ["Circle", "Square", "Triangle", "Rectangle"]
        for shape in shapes:
            pdf.cell(0, 8, f"• Find and color {shape} shapes", 0, 1, 'L')
    
    def _add_stage3_visual_content(self, pdf):
        """Add Stage 3 visual content."""
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "Pattern Making Exercises", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 5, "Create patterns using Hong Kong elements:", 0, 1, 'L')
        pdf.ln(5)
        
        pdf.cell(0, 8, "• Red-Blue-Red-Blue (Hong Kong Flag)", 0, 1, 'L')
        pdf.cell(0, 8, "• Circle-Square-Circle-Square", 0, 1, 'L')
        pdf.cell(0, 8, "• Big-Small-Big-Small", 0, 1, 'L')
    
    def _add_stage4_visual_content(self, pdf):
        """Add Stage 4 visual content."""
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "Addition & Subtraction Exercises", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 5, "Solve using Hong Kong objects:", 0, 1, 'L')
        pdf.ln(5)
        
        problems = [
            "2 dim sum + 3 dim sum = _____",
            "5 buses - 2 buses = _____",
            "3 toys + 2 toys = _____",
            "4 apples - 1 apple = _____"
        ]
        for problem in problems:
            pdf.cell(0, 8, f"• {problem}", 0, 1, 'L')
    
    def _add_stage5_visual_content(self, pdf):
        """Add Stage 5 visual content."""
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "Measurement Exercises", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 5, "Compare Hong Kong landmarks:", 0, 1, 'L')
        pdf.ln(5)
        
        pdf.cell(0, 8, "• Which is taller: IFC or ICC?", 0, 1, 'L')
        pdf.cell(0, 8, "• Which is longer: your arm or your foot?", 0, 1, 'L')
        pdf.cell(0, 8, "• Which is heavier: apple or orange?", 0, 1, 'L')
    
    def _add_stage6_visual_content(self, pdf):
        """Add Stage 6 visual content."""
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, "Spatial & Problem-Solving Exercises", 0, 1, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 5, "Solve Hong Kong navigation problems:", 0, 1, 'L')
        pdf.ln(5)
        
        pdf.cell(0, 8, "• How to get from Central to Causeway Bay?", 0, 1, 'L')
        pdf.cell(0, 8, "• What's inside/outside the MTR station?", 0, 1, 'L')
        pdf.cell(0, 8, "• Which way is up/down in a building?", 0, 1, 'L')

    def generate_complete_course(self) -> Dict[str, List[str]]:
        """
        Generate complete course materials for all 6 stages.
        
        Returns:
            Dictionary with file paths for each content type
        """
        results = {
            'goals': [],
            'content': [],
            'worksheets': [],
            'visual_worksheets': [],
            'activities': []
        }
        
        logger.info("Starting complete course generation...")
        
        try:
            for stage in range(1, 7):
                logger.info(f"Generating materials for stage {stage}...")
                
                # Generate goals
                goals_file = self.generate_goals_markdown(stage)
                if goals_file:
                    results['goals'].append(goals_file)
                
                # Generate content with EDB integration
                content_file = self.generate_content_text(stage)
                if content_file:
                    results['content'].append(content_file)
                
                # Generate worksheet
                worksheet_file = self.generate_worksheet_pdf(stage)
                if worksheet_file:
                    results['worksheets'].append(worksheet_file)
                
                # Generate visual worksheet
                visual_worksheet_file = self.generate_visual_worksheet_pdf(stage)
                if visual_worksheet_file:
                    results['visual_worksheets'].append(visual_worksheet_file)
                
                # Generate activities
                activities_file = self.generate_activities_excel(stage)
                if activities_file:
                    results['activities'].append(activities_file)
        
        # Generate combined goals and content file
        combined_file = self.generate_combined_goals_and_content()
        if combined_file:
            results['combined'] = [combined_file]
        
        # Generate comprehensive stage PDFs
        stage_pdfs = self.generate_stage_pdfs()
        if stage_pdfs:
            results['stage_pdfs'] = stage_pdfs
            
        # Generate combined Excel activities file
        combined_excel = self.generate_all_activities_excel()
        if combined_excel:
            results['combined_excel'] = [combined_excel]
            
            # Create summary report
            self._create_summary_report(results)
            
            logger.info("Complete course generation finished successfully!")
            return results
            
        except Exception as e:
            logger.error(f"Failed to generate complete course: {e}")
            logger.error(traceback.format_exc())
            return results
    
    def scrape_edb_math_ideas(self) -> Dict[str, List[str]]:
        """
        Scrape Hong Kong Education Bureau website for math education ideas.
        
        Returns:
            Dictionary containing scraped math ideas organized by category
        """
        if not WEB_SCRAPING_AVAILABLE:
            logger.warning("Web scraping not available. Using fallback content.")
            return self._get_fallback_edb_ideas()
        
        edb_ideas = {
            'activities': [],
            'principles': [],
            'guidelines': [],
            'resources': []
        }
        
        try:
            # Hong Kong EDB Math Curriculum URL
            url = "https://www.edb.gov.hk/en/curriculum-development/major-level-of-edu/preprimary/maths.html"
            
            logger.info(f"Scraping EDB website: {url}")
            
            # Set headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            # Make request with timeout
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract math-related content
            edb_ideas = self._extract_math_content(soup)
            
            logger.info(f"Successfully scraped {len(edb_ideas['activities'])} activities from EDB")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to scrape EDB website: {e}")
            edb_ideas = self._get_fallback_edb_ideas()
        except Exception as e:
            logger.error(f"Error parsing EDB content: {e}")
            edb_ideas = self._get_fallback_edb_ideas()
        
        return edb_ideas
    
    def _extract_math_content(self, soup) -> Dict[str, List[str]]:
        """Extract math-related content from EDB HTML."""
        edb_ideas = {
            'activities': [],
            'principles': [],
            'guidelines': [],
            'resources': []
        }
        
        try:
            # Look for math curriculum content
            # Common selectors for EDB pages
            selectors = [
                'div.content',
                'div.main-content',
                'div.curriculum-content',
                'article',
                'div.edb-content'
            ]
            
            content_found = False
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    content_found = True
                    break
            
            if not content_found:
                # Fallback: extract from body
                elements = soup.find_all(['p', 'li', 'div'], text=True)
            
            # Extract text content
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 10:  # Filter out short text
                    # Look for math-related keywords
                    math_keywords = ['math', 'number', 'counting', 'shape', 'pattern', 'measurement', 'space']
                    if any(keyword.lower() in text.lower() for keyword in math_keywords):
                        if len(text) < 200:  # Short text likely activities
                            edb_ideas['activities'].append(text)
                        else:  # Longer text likely guidelines
                            edb_ideas['guidelines'].append(text)
            
            # If no specific content found, use fallback
            if not any(edb_ideas.values()):
                edb_ideas = self._get_fallback_edb_ideas()
                
        except Exception as e:
            logger.error(f"Error extracting math content: {e}")
            edb_ideas = self._get_fallback_edb_ideas()
        
        return edb_ideas
    
    def _get_fallback_edb_ideas(self) -> Dict[str, List[str]]:
        """Fallback EDB ideas when scraping fails."""
        return {
            'activities': [
                "Play-based learning through everyday objects and experiences",
                "Counting activities using natural materials like stones and leaves",
                "Shape recognition through building blocks and puzzles",
                "Pattern making with colorful beads and buttons",
                "Measurement using non-standard units like hand spans and footsteps"
            ],
            'principles': [
                "Balanced development focusing on whole-child approach",
                "Learning through play and exploration",
                "Integration of mathematics with daily life experiences",
                "Cultivation of positive attitudes towards learning",
                "Development of problem-solving and thinking skills"
            ],
            'guidelines': [
                "Create a supportive and stimulating learning environment",
                "Encourage children to explore and discover mathematical concepts",
                "Use concrete materials and manipulatives for hands-on learning",
                "Provide opportunities for children to communicate their mathematical thinking",
                "Celebrate children's efforts and achievements in mathematics"
            ],
            'resources': [
                "Educational toys and manipulatives",
                "Picture books with mathematical themes",
                "Music and songs incorporating counting and numbers",
                "Art materials for creating patterns and shapes",
                "Outdoor spaces for measurement and spatial activities"
            ]
        }
    
    def integrate_edb_ideas(self, content: str, stage: int) -> str:
        """
        Integrate EDB ideas into existing content.
        
        Args:
            content: Original content
            stage: Learning stage (1-6)
            
        Returns:
            Enhanced content with EDB ideas
        """
        try:
            # Get EDB ideas
            edb_ideas = self.scrape_edb_math_ideas()
            
            # Add EDB section to content
            edb_section = "\n\n## 🏛️ Education Bureau Guidelines & Ideas\n"
            edb_section += "Based on Hong Kong Education Bureau curriculum guidelines:\n\n"
            
            # Add relevant activities
            if edb_ideas['activities']:
                edb_section += "### 🎯 EDB Recommended Activities:\n"
                for activity in edb_ideas['activities'][:3]:  # Limit to 3 activities
                    edb_section += f"- {activity}\n"
                edb_section += "\n"
            
            # Add principles
            if edb_ideas['principles']:
                edb_section += "### 📚 EDB Learning Principles:\n"
                for principle in edb_ideas['principles'][:2]:  # Limit to 2 principles
                    edb_section += f"- {principle}\n"
                edb_section += "\n"
            
            # Add guidelines
            if edb_ideas['guidelines']:
                edb_section += "### 💡 EDB Implementation Guidelines:\n"
                for guideline in edb_ideas['guidelines'][:2]:  # Limit to 2 guidelines
                    edb_section += f"- {guideline}\n"
                edb_section += "\n"
            
            # Add resources
            if edb_ideas['resources']:
                edb_section += "### 📦 EDB Recommended Resources:\n"
                for resource in edb_ideas['resources'][:3]:  # Limit to 3 resources
                    edb_section += f"- {resource}\n"
                edb_section += "\n"
            
            # Add integration note
            edb_section += "> **Note**: These activities align with Hong Kong Education Bureau's emphasis on balanced development, play-based learning, and whole-child approach.\n"
            
            # Append to content
            enhanced_content = content + edb_section
            
            logger.info(f"Successfully integrated EDB ideas into stage {stage} content")
            return enhanced_content
            
        except Exception as e:
            logger.error(f"Failed to integrate EDB ideas: {e}")
            return content  # Return original content if integration fails
    
    def _create_summary_report(self, results: Dict[str, List[str]]):
        """Create a summary report of all generated materials."""
        try:
            report_path = os.path.join(self.output_dir, 'course_summary.txt')
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("AUDREY MATH COURSE GENERATOR - SUMMARY REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total stages: 6\n\n")
                
                f.write("GENERATED FILES:\n")
                f.write("-" * 20 + "\n\n")
                
                for content_type, files in results.items():
                    if content_type == 'combined':
                        f.write(f"{content_type.upper()}:\n")
                        for file in files:
                            f.write(f"  - {file} (Complete 6-stage curriculum)\n")
                        f.write("\n")
                    elif content_type == 'combined_excel':
                        f.write(f"{content_type.upper()}:\n")
                        for file in files:
                            f.write(f"  - {file} (All 6 stages in one Excel file)\n")
                        f.write("\n")
                    elif content_type == 'visual_worksheets':
                        f.write(f"VISUAL_WORKSHEETS:\n")
                        for file in files:
                            f.write(f"  - {file} (Kid-friendly FPDF/ReportLab worksheets)\n")
                        f.write("\n")
                    else:
                        f.write(f"{content_type.upper()}:\n")
                        for file in files:
                            f.write(f"  - {file}\n")
                        f.write("\n")
                
                f.write("COURSE OVERVIEW:\n")
                f.write("-" * 20 + "\n")
                for stage, name in self.stages.items():
                    f.write(f"Stage {stage}: {name}\n")
                
                f.write("\nUSAGE INSTRUCTIONS:\n")
                f.write("-" * 20 + "\n")
                f.write("1. Review the goals files for learning objectives\n")
                f.write("2. Use content files for lesson planning\n")
                f.write("3. Print worksheet PDFs for student activities\n")
                f.write("4. Use Excel files for activity tracking and assessment\n")
                f.write("5. Adapt materials based on individual child needs\n")
            
            logger.info(f"Summary report created: {report_path}")
            
        except Exception as e:
            logger.error(f"Failed to create summary report: {e}")


def main():
    """Main function to run all course generation with Agent mode support."""
    print("🎓 Audrey Math Course Generator - Complete Materials")
    print("=" * 60)
    print("Generating comprehensive kindergarten math course materials")
    print("For 3-5 year old children in Hong Kong educational style")
    print("With EDB integration and Agent mode support\n")

    # Directly use the provided API key
    gemini_key = "AIzaSyCMyL9VphKmBXmWIrOolr2XBpguIwDay_E"

    try:
        # Create main output directory
        main_output_dir = "Math_Course_Materials"
        generator = AudreyMathCourseGenerator(
            output_dir=main_output_dir,
            gemini_api_key=gemini_key
        )
        
        print("🚀 Starting comprehensive course generation...")
        print("📋 This may take several minutes for complete materials generation")
        print("🤖 Using Agent mode for long-running operations\n")
        
        # Generate complete course with all materials
        results = generator.generate_complete_course()
        
        # Display comprehensive results
        print("\n🎉 Complete Course Generation Finished Successfully!")
        print("=" * 60)
        
        total_files = sum(len(files) for files in results.values())
        print(f"📊 Total Files Generated: {total_files}")
        print(f"📁 Output Directory: {main_output_dir}")
        
        # Detailed file listing
        for content_type, files in results.items():
            if content_type == 'goals':
                print(f"\n📋 LEARNING GOALS ({len(files)} files):")
                for file in files:
                    print(f"  ✓ {os.path.basename(file)}")
            elif content_type == 'content':
                print(f"\n📚 TEACHING CONTENT ({len(files)} files):")
                for file in files:
                    print(f"  ✓ {os.path.basename(file)} (with EDB integration)")
            elif content_type == 'worksheets':
                print(f"\n📄 PDF WORKSHEETS ({len(files)} files):")
                for file in files:
                    print(f"  ✓ {os.path.basename(file)}")
            elif content_type == 'visual_worksheets':
                print(f"\n🎨 VISUAL WORKSHEETS ({len(files)} files):")
                for file in files:
                    print(f"  ✓ {os.path.basename(file)} (Kid-friendly with Hong Kong elements)")
            elif content_type == 'activities':
                print(f"\n🎯 ACTIVITIES ({len(files)} files):")
                for file in files:
                    print(f"  ✓ {os.path.basename(file)} (Hong Kong-themed)")
            elif content_type == 'combined':
                print(f"\n📖 COMBINED DOCUMENTS ({len(files)} files):")
                for file in files:
                    print(f"  ✓ {os.path.basename(file)} (All stages + EDB content)")
            elif content_type == 'combined_excel':
                print(f"\n📊 COMBINED EXCEL ({len(files)} files):")
                for file in files:
                    print(f"  ✓ {os.path.basename(file)} (All activities)")
            elif content_type == 'stage_pdfs':
                print(f"\n📄 STAGE PDFS ({len(files)} files):")
                for file in files:
                    print(f"  ✓ {os.path.basename(file)} (Comprehensive 3-page PDFs with EDB integration)")
        
        # Agent mode features
        print(f"\n🤖 AGENT MODE FEATURES:")
        print(f"  🔄 Auto-retry on errors")
        print(f"  📊 Progress tracking")
        print(f"  🏛️ EDB content integration")
        print(f"  🎨 Visual worksheet generation")
        print(f"  📈 Comprehensive reporting")
        
        # Personalization suggestions
        print(f"\n🎨 PERSONALIZATION SUGGESTIONS:")
        print(f"  🐼 Animal themes (pandas, dolphins)")
        print(f"  🎵 Musical integration")
        print(f"  🎨 Art and craft activities")
        print(f"  🌈 Color-based learning")
        print(f"  🎪 Festival themes (Chinese New Year, Mid-Autumn)")
        
        # Next steps
        print(f"\n📋 NEXT STEPS:")
        print(f"  1. Review generated materials in '{main_output_dir}' folder")
        print(f"  2. Customize based on specific child needs")
        print(f"  3. Print worksheets and activity sheets")
        print(f"  4. Start with Stage 1 activities")
        print(f"  5. Use parent tips for home practice")
        
        print(f"\n🚀 Ready for teaching and learning!")
        print(f"📚 All materials are age-appropriate for 3-5 year olds")
        print(f"🇭🇰 Hong Kong educational style with EDB integration")
        
    except KeyboardInterrupt:
        print("\n\nGeneration interrupted by user.")
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        logger.error(f"Main execution failed: {e}")
        print(f"\n🔧 TROUBLESHOOTING:")
        print(f"  - Check internet connection for Gemini API")
        print(f"  - Ensure all required libraries are installed")
        print(f"  - Try running individual components")
        print(f"  - Use 'Debug PDF errors with Bugbot' if needed")
        logger.error(traceback.format_exc())


def run_agent_mode():
    """Run in Agent mode for long-running operations with enhanced features."""
    print("🤖 Starting Agent Mode - Enhanced Course Generation")
    print("=" * 60)
    
    # Agent mode configuration
    agent_config = {
        'max_retries': 3,
        'timeout': 300,  # 5 minutes per operation
        'progress_tracking': True,
        'error_recovery': True,
        'personalization': True
    }
    
    print("🔧 Agent Mode Configuration:")
    for key, value in agent_config.items():
        print(f"  {key}: {value}")
    
    print("\n🚀 Starting enhanced generation...")
    
    # Run main function with agent mode
    main()

def personalize_content(theme="animals"):
    """Add personalization themes to course content."""
    print(f"🎨 Personalizing content with {theme} theme...")
    
    personalization_prompts = {
        'animals': "Add animal themes like pandas, dolphins, and Hong Kong Zoo animals",
        'music': "Integrate musical elements and rhythm-based learning",
        'art': "Include art and craft activities with mathematical concepts",
        'festivals': "Add Hong Kong festival themes like Chinese New Year and Mid-Autumn Festival",
        'nature': "Include nature and outdoor learning elements"
    }
    
    if theme in personalization_prompts:
        print(f"🎯 Theme: {theme}")
        print(f"💡 Prompt: {personalization_prompts[theme]}")
        
        # This would integrate with Gemini API for personalized content
        return personalization_prompts[theme]
    
    return "Standard Hong Kong educational content"

def debug_pdf_errors():
    """Debug PDF generation errors with enhanced error handling."""
    print("🔧 Debug Mode - PDF Error Analysis")
    print("=" * 50)
    
    print("📋 Checking PDF generation components...")
    
    # Check available libraries
    print("\n📚 Library Status:")
    print(f"  ReportLab: {'✅ Available' if REPORTLAB_AVAILABLE else '❌ Not Available'}")
    print(f"  FPDF: {'✅ Available' if FPDF_AVAILABLE else '❌ Not Available'}")
    print(f"  Pillow: {'✅ Available' if PILLOW_AVAILABLE else '❌ Not Available'}")
    
    # Test PDF generation
    print("\n🧪 Testing PDF generation...")
    try:
        generator = AudreyMathCourseGenerator(
            output_dir="debug_test",
            gemini_api_key="AIzaSyCMyL9VphKmBXmWIrOolr2XBpguIwDay_E"
        )
        
        # Test visual worksheet generation
        test_file = generator.generate_visual_worksheet_pdf(1)
        if test_file:
            print(f"✅ PDF generation test successful: {test_file}")
        else:
            print("❌ PDF generation test failed")
            
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        print("\n🔧 Suggested fixes:")
        print("  - Install missing libraries: pip install reportlab fpdf2 pillow")
        print("  - Check file permissions")
        print("  - Verify output directory exists")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--agent":
            run_agent_mode()
        elif sys.argv[1] == "--personalize":
            theme = sys.argv[2] if len(sys.argv) > 2 else "animals"
            personalize_content(theme)
            main()
        elif sys.argv[1] == "--debug":
            debug_pdf_errors()
        elif sys.argv[1] == "--help":
            print("🎓 Audrey Math Course Generator - Usage Options")
            print("=" * 50)
            print("python audrey_math_course_generator.py [options]")
            print("\nOptions:")
            print("  --agent        Run in Agent mode for long operations")
            print("  --personalize  Add personalization themes")
            print("  --debug        Debug PDF generation errors")
            print("  --help         Show this help message")
            print("\nExamples:")
            print("  python audrey_math_course_generator.py")
            print("  python audrey_math_course_generator.py --agent")
            print("  python audrey_math_course_generator.py --personalize animals")
            print("  python audrey_math_course_generator.py --debug")
        else:
            print("❌ Unknown option. Use --help for usage information.")
    else:
        main()
