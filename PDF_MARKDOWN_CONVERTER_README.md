# PDF to Markdown Converter - Complete Guide

A powerful, all-in-one PDF to Markdown converter for the HDM (Human Digital Memory) research project. This converter supports multiple modes, parallel processing, and intelligent handling of images and descriptions.

## 🚀 Quick Start

```bash
# Default dual mode (images + descriptions)
./venv/bin/python pdf-markdown-converter.py

# With progress tracking
./venv/bin/python pdf-markdown-converter.py --progress

# Convert 10 PDFs with 8 workers
./venv/bin/python pdf-markdown-converter.py --limit 10 --workers 8 --progress
```

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Conversion Modes](#conversion-modes)
- [Usage Examples](#usage-examples)
- [Command Line Options](#command-line-options)
- [Output Structure](#output-structure)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## ✨ Features

### Core Features
- **Three Conversion Modes**: Dual (default), Images only, Descriptions only
- **Parallel Processing**: Multi-worker support for faster conversion
- **Checkpoint System**: Automatic resume from interruptions
- **Progress Tracking**: Real-time progress bar with ETA
- **Smart Filtering**: Filter by file size, count limits
- **Comprehensive Logging**: Detailed logs for debugging
- **Error Recovery**: Automatic retry and error handling

### Image Handling Options

#### 1. **Dual Mode (Default)** - Best of Both Worlds
- ✅ Extracts actual image files
- ✅ Generates detailed text descriptions
- ✅ Perfect for comprehensive research analysis
- ✅ Optimal for both visual reference and LLM processing

#### 2. **Images Mode** - Visual Preservation
- ✅ Extracts and saves all images
- ✅ Maintains visual references
- ✅ Good for archival purposes
- ✅ Faster than dual mode

#### 3. **Descriptions Mode** - LLM Optimized
- ✅ Converts images to detailed text descriptions
- ✅ Smaller file sizes
- ✅ Optimal for LLM processing
- ✅ No external image dependencies

## 🔧 Installation

```bash
# Ensure you're in the project directory
cd /Users/invoture/dev.local/hdm

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install python-dotenv psutil

# Make script executable
chmod +x pdf-markdown-converter.py

# Create .env file with your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

## 🎯 Conversion Modes

### Dual Mode (Default)
Generates both image files AND text descriptions in a single pass.

```bash
# Default behavior
./venv/bin/python pdf-markdown-converter.py

# Explicitly specify dual mode
./venv/bin/python pdf-markdown-converter.py --mode dual
```

**Output Example:**
```markdown
![Figure 1](_page_1_Figure_1.jpeg)

**[Image Description]** This figure illustrates a hierarchical knowledge graph 
architecture with three main layers: data ingestion at the bottom, processing 
middleware in the center, and application interfaces at the top...
```

### Images Mode
Extracts only image files without descriptions.

```bash
./venv/bin/python pdf-markdown-converter.py --mode images
```

### Descriptions Mode
Generates only text descriptions without extracting images.

```bash
./venv/bin/python pdf-markdown-converter.py --mode descriptions
```

## 📚 Usage Examples

### Basic Usage

```bash
# Convert all PDFs with default settings
./venv/bin/python pdf-markdown-converter.py

# Show progress during conversion
./venv/bin/python pdf-markdown-converter.py --progress

# Check conversion status
./venv/bin/python pdf-markdown-converter.py --status
```

### Performance Optimization

```bash
# Use 8 parallel workers for faster processing
./venv/bin/python pdf-markdown-converter.py --workers 8

# Fast mode (no LLM processing)
./venv/bin/python pdf-markdown-converter.py --fast --workers 8

# Custom timeout for large PDFs
./venv/bin/python pdf-markdown-converter.py --timeout 600
```

### Filtering and Limits

```bash
# Convert only 10 PDFs
./venv/bin/python pdf-markdown-converter.py --limit 10

# Convert PDFs between 1MB and 10MB
./venv/bin/python pdf-markdown-converter.py --min-size 1024 --max-size 10

# Test with 5 small PDFs
./venv/bin/python pdf-markdown-converter.py --limit 5 --max-size 5 --progress
```

### Advanced Usage

```bash
# Full production run with all features
./venv/bin/python pdf-markdown-converter.py --workers 8 --progress --enhance

# Resume interrupted conversion
./venv/bin/python pdf-markdown-converter.py --workers 8 --progress

# Force reconversion of all PDFs
./venv/bin/python pdf-markdown-converter.py --force --reset

# Custom directories
./venv/bin/python pdf-markdown-converter.py --input-dir /path/to/pdfs --output-dir /path/to/output
```

## 🛠 Command Line Options

### Mode Selection
- `--mode {dual,images,descriptions}` - Conversion mode (default: dual)

### Input/Output
- `--input-dir PATH` - Input directory with PDFs (default: papers/)
- `--output-dir PATH` - Output directory (auto-generated if not specified)

### Performance
- `--workers N` - Number of parallel workers (default: 4)
- `--timeout N` - Timeout per PDF in seconds (default: 300)
- `--fast` - Fast mode without LLM processing
- `--max-size-fast N` - Max file size for fast mode in MB (default: 20)

### Filtering
- `--limit N` - Limit number of PDFs to convert
- `--min-size N` - Minimum file size in KB
- `--max-size N` - Maximum file size in MB

### Control
- `--status` - Show conversion status and exit
- `--reset` - Reset checkpoint and start fresh
- `--force` - Force reconversion of completed PDFs
- `--progress` - Show progress bar during conversion

### Enhancement
- `--enhance` - Enhance descriptions for better LLM understanding
- `--format-lines` - Format lines for readability (default: True)
- `--no-llm` - Disable LLM usage (for images mode)

### Debugging
- `--debug` - Enable debug logging
- `--no-log` - Disable file logging
- `--no-checkpoint` - Disable checkpoint saving

## 📁 Output Structure

### Dual Mode (Default)
```
markdown_dual/
├── paper_name/
│   ├── paper_name.md          # Markdown with images and descriptions
│   ├── _page_1_Figure_1.jpeg  # Extracted image
│   ├── _page_2_Table_1.jpeg   # Extracted image
│   └── ...
```

### Images Mode
```
markdown_images/
├── paper_name/
│   ├── paper_name.md          # Markdown with image references
│   ├── *.jpeg                 # All extracted images
│   └── ...
```

### Descriptions Mode
```
markdown_descriptions/
├── paper_name/
│   └── paper_name.md          # Markdown with text descriptions only
```

## ⚡ Performance Optimization

### Understanding --workers

The `--workers` parameter controls parallel processing - how many PDFs are converted simultaneously.

```bash
# Single worker (sequential)
--workers 1  # Processes one PDF at a time

# Default (balanced)
--workers 4  # Processes 4 PDFs simultaneously

# High performance
--workers 8  # Processes 8 PDFs simultaneously
```

### Performance Comparison
- **1 worker**: 100 PDFs × 30 seconds each = 50 minutes
- **8 workers**: 100 PDFs ÷ 8 parallel = ~6-7 minutes

### Optimal Settings

Check your CPU cores:
```bash
# Mac/Linux
sysctl -n hw.ncpu
```

Set workers to match your CPU cores for best performance:
- 4-core CPU: `--workers 4`
- 8-core CPU: `--workers 8`
- 16-core CPU: `--workers 12` (leave some for system)

## 🔍 Checkpoint System

The converter automatically saves progress:
- `checkpoint_markdown_dual.json` - For dual mode
- `checkpoint_markdown_images.json` - For images mode
- `checkpoint_markdown_descriptions.json` - For descriptions mode

### Resume After Interruption
```bash
# Just run the same command again - it will resume automatically
./venv/bin/python pdf-markdown-converter.py --workers 8 --progress
```

### Check Status
```bash
./venv/bin/python pdf-markdown-converter.py --status
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Timeout Errors
```bash
# Increase timeout for large PDFs
./venv/bin/python pdf-markdown-converter.py --timeout 600
```

#### 2. Memory Issues
```bash
# Reduce workers to use less memory
./venv/bin/python pdf-markdown-converter.py --workers 2
```

#### 3. Large PDFs Failing
```bash
# Use fast mode for large files
./venv/bin/python pdf-markdown-converter.py --fast --max-size-fast 50
```

#### 4. API Key Issues
```bash
# Ensure .env file exists with your key
cat .env
# Should show: GOOGLE_API_KEY=your_key_here
```

### Debug Mode
```bash
# Enable detailed logging
./venv/bin/python pdf-markdown-converter.py --debug --limit 1
```

## 🎯 Best Practices

### For HDM Research (Recommended)
Use default dual mode with optimal workers:
```bash
./venv/bin/python pdf-markdown-converter.py --workers 8 --progress --enhance
```

### For Quick Testing
Test with a few PDFs first:
```bash
./venv/bin/python pdf-markdown-converter.py --limit 5 --progress
```

### For Large Batches
Use checkpoint system for reliability:
```bash
# Start conversion
./venv/bin/python pdf-markdown-converter.py --workers 8

# If interrupted, resume automatically
./venv/bin/python pdf-markdown-converter.py --workers 8
```

### For Different Scenarios

#### Fast Initial Scan
```bash
./venv/bin/python pdf-markdown-converter.py --mode images --fast --workers 8
```

#### High-Quality LLM Processing
```bash
./venv/bin/python pdf-markdown-converter.py --mode descriptions --enhance
```

#### Complete Archive
```bash
# Run both modes separately if needed
./venv/bin/python pdf-markdown-converter.py --mode dual --workers 8
```

## 📊 Performance Metrics

The converter tracks:
- Conversion rate (PDFs/second)
- Success/failure counts
- Time estimates
- Image extraction counts

## 🔐 Security

- All API keys stored in `.env` file
- No hardcoded credentials
- Secure handling of Google API key

## 📈 Current Project Status

- **Converter**: Fully consolidated into single script
- **Modes**: All three modes (dual, images, descriptions) working
- **Performance**: Optimized for parallel processing
- **Checkpoint**: Full resume capability implemented
- **Production**: Ready for full 453 PDF conversion

## 🎉 Summary

The PDF to Markdown Converter is a comprehensive solution that handles all conversion needs with sensible defaults and extensive customization options. The dual mode default ensures you get both visual preservation and LLM-optimized descriptions in a single pass, making it perfect for research applications.