# Lorem Ipsum to Handwritten Text Converter

A simplified script to convert large blocks of text (like lorem ipsum) into handwritten-style images formatted for A4 paper size.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Note: This project uses TensorFlow 1.6.0. For modern Python versions, you may need to use:
```bash
pip install numpy scipy matplotlib svgwrite pandas scikit-learn
pip install tensorflow  # or tensorflow==1.15.5 for last TF 1.x version
```

### 2. Run the Script

**Generate demo with sample lorem ipsum (2-3 pages):**
```bash
python lorem_to_handwritten.py --demo
```

**Convert your own text file:**
```bash
python lorem_to_handwritten.py -i yourtext.txt -o output_name
```

**Customize handwriting style and neatness:**
```bash
python lorem_to_handwritten.py --demo -b 0.8 -s 5
```

## Options

- `-i, --input FILE` - Input text file to convert
- `-o, --output PREFIX` - Output file prefix (default: 'output')
- `-b, --bias FLOAT` - Handwriting neatness 0.0-1.0 (default: 0.75)
  - 0.0 = very messy/creative
  - 0.5 = default neatness
  - 1.0 = very neat/constrained
- `-s, --style INT` - Handwriting style 0-12 (default: 9)
- `--demo` - Generate demo with sample lorem ipsum text

## Output Format

- **Format**: SVG (Scalable Vector Graphics)
- **Page size**: A4 (794px × 1123px at 96 DPI)
- **Lines per page**: ~18 lines
- **Max characters per line**: 75 characters
- **Output files**: `{prefix}_page_01.svg`, `{prefix}_page_02.svg`, etc.

## Converting SVG to PNG

The script generates SVG files. To convert to PNG, you can use:

### Option 1: ImageMagick (recommended)
```bash
sudo apt-get install imagemagick
convert output_page_01.svg output_page_01.png
```

### Option 2: Inkscape
```bash
sudo apt-get install inkscape
inkscape output_page_01.svg --export-png=output_page_01.png
```

### Option 3: cairosvg (Python)
```bash
pip install cairosvg
python -c "import cairosvg; cairosvg.svg2png(url='output_page_01.svg', write_to='output_page_01.png')"
```

### Batch convert all pages:
```bash
for file in output_page_*.svg; do
    convert "$file" "${file%.svg}.png"
done
```

## How It Works

1. **Text Processing**: Splits input text into lines (max 75 chars each)
2. **Pagination**: Groups lines into pages (~18 lines per A4 page)
3. **Neural Network**: Uses pretrained RNN model to generate handwriting strokes
4. **Style Control**:
   - 13 different handwriting styles (0-12)
   - Bias parameter controls writing neatness
5. **SVG Generation**: Converts stroke data to scalable vector graphics

## Examples

### Example 1: Clean, neat handwriting
```bash
python lorem_to_handwritten.py --demo -b 0.9 -s 9 -o neat_lorem
```

### Example 2: Messier, more creative style
```bash
python lorem_to_handwritten.py --demo -b 0.3 -s 7 -o messy_lorem
```

### Example 3: Convert your essay
```bash
python lorem_to_handwritten.py -i essay.txt -o handwritten_essay -b 0.75 -s 5
```

## Technical Details

- **Model**: Recurrent Neural Network with attention mechanism
- **Based on**: Alex Graves' "Generating Sequences with Recurrent Neural Networks" (2013)
- **Pretrained checkpoint**: `checkpoints/model-17900.*`
- **Style priming data**: `styles/style-{0-12}-*.npy`

## Limitations

- Maximum 75 characters per line
- Only supports ASCII characters (a-z, A-Z, 0-9, basic punctuation)
- Requires TensorFlow for inference
- SVG output only (requires external tools for PNG/PDF conversion)

## Tips

- For longer documents (5+ pages), generation may take several minutes
- Try different style numbers (0-12) to find your preferred handwriting
- Higher bias values (0.8-1.0) work better for formal documents
- Lower bias values (0.2-0.5) look more natural and human-like
- Keep lines under 75 characters for best results
