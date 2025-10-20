# Audrey Math Course Generator

A comprehensive Python script to create kindergarten math course materials for 3-year-old children in Hong Kong style.

## Features

- **6 Progressive Learning Stages**: Number recognition, shapes/colors, patterns, addition/subtraction, measurement, and spatial problem-solving
- **Multiple Output Formats**: Markdown goals, text content, PDF worksheets with drawings, Excel activity sheets
- **AI-Powered Content**: Integration with Gemini API for intelligent content generation
- **Error-Resistant Design**: Comprehensive try-except handling and graceful degradation
- **Hong Kong Educational Style**: Culturally appropriate content and examples

## Learning Stages

1. **Number Recognition and Counting (1-10)**
2. **Shapes and Colors**
3. **Patterns and Classification**
4. **Basic Addition/Subtraction with Objects**
5. **Measurement and Comparison**
6. **Space and Problem Solving**

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set up Gemini API key for AI content generation:
   - Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - The script will prompt for the key when running

## Usage

### Basic Usage
```bash
python audrey_math_course_generator.py
```

### Programmatic Usage
```python
from audrey_math_course_generator import AudreyMathCourseGenerator

# Initialize generator
generator = AudreyMathCourseGenerator(
    output_dir="my_course_output",
    gemini_api_key="your_api_key_here"
)

# Generate complete course
results = generator.generate_complete_course()

# Generate specific stage
goals_file = generator.generate_goals_markdown(stage=1)
worksheet_file = generator.generate_worksheet_pdf(stage=1)
```

## Output Structure

The generator creates the following directory structure:

```
audrey_math_output/
├── goals/           # Markdown learning goals
├── content/         # Detailed text content
├── worksheets/      # PDF worksheets with drawings
├── activities/      # Excel activity sheets
├── images/          # Generated images
├── temp/           # Temporary files
└── course_summary.txt
```

## Dependencies

- **reportlab**: PDF generation with drawings
- **pandas**: Excel file creation and data handling
- **Pillow**: Image processing and manipulation
- **google-generativeai**: AI content generation (optional)

## Error Handling

The script is designed to be error-resistant:
- Graceful degradation when optional libraries are missing
- Fallback content when AI services are unavailable
- Comprehensive logging for troubleshooting
- Try-except blocks around all major operations

## Customization

### Adding New Stages
1. Add stage definition to `self.stages` dictionary
2. Implement stage-specific content methods
3. Add corresponding PDF content generation

### Modifying Content
- Edit fallback content in `_get_default_*` methods
- Customize AI prompts in `generate_ai_content`
- Adjust PDF layouts in `_add_*_content_to_pdf` methods

## Hong Kong Educational Features

- Cultural context integration (MTR stations, dim sum, traditional buildings)
- Bilingual-friendly content structure
- Play-based learning approach
- Parent involvement activities
- Assessment aligned with Hong Kong curriculum

## License

This project is created for educational purposes. Please ensure compliance with any applicable educational standards and copyright requirements.

## Support

For issues or questions:
1. Check the log file: `audrey_math_generator.log`
2. Review error messages in the console output
3. Ensure all dependencies are properly installed
