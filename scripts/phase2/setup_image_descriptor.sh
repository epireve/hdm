#!/bin/bash

echo "==================================="
echo "Image Descriptor Setup"
echo "==================================="

# Check Python version
echo "Checking Python version..."
python --version

# Install required packages
echo ""
echo "Installing required packages..."
pip install -r scripts/phase2/requirements_image_descriptor.txt

# Verify installation
echo ""
echo "Verifying installation..."
python -c "
try:
    import google.generativeai as genai
    print('✓ google-generativeai installed successfully')
except ImportError:
    print('✗ google-generativeai installation failed')

try:
    from PIL import Image
    print('✓ Pillow (PIL) installed successfully')
except ImportError:
    print('✗ Pillow installation failed')
"

echo ""
echo "Setup complete! You can now run the image descriptor."
echo ""
echo "Next steps:"
echo "1. Get your API key from: https://makersuite.google.com/app/apikey"
echo "2. Set your API key: export GOOGLE_API_KEY='your-key-here'"
echo "3. Run test mode: python scripts/phase2/run_phase2_csv.py --test --step describe-images"
echo "4. Run full mode: python scripts/phase2/run_phase2_csv.py --full --step describe-images"