#!/usr/bin/env python3
"""
Simplified script to convert lorem ipsum text to handwritten-style images.
Outputs SVG files formatted for A4 paper size.
"""

import os
import sys
import argparse
from demo import Hand


# A4 dimensions at 96 DPI: 794px × 1123px
# Line height in demo.py is 60px, so roughly 18 lines fit on A4
LINES_PER_PAGE = 18
MAX_CHARS_PER_LINE = 75
A4_WIDTH = 794
A4_HEIGHT = 1123


def generate_lorem_ipsum(pages=2):
    """Generate sample lorem ipsum text for testing."""
    lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem
accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
quae ab illo inventore veritatis et quasi architecto beatae vitae
dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
aspernatur aut odit aut fugit, sed quia consequuntur magni dolores
eos qui ratione voluptatem sequi nesciunt.

Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet,
consectetur, adipisci velit, sed quia non numquam eius modi tempora
incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut
enim ad minima veniam, quis nostrum exercitationem ullam corporis
suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur.

At vero eos et accusamus et iusto odio dignissimos ducimus qui
blanditiis praesentium voluptatum deleniti atque corrupti quos
dolores et quas molestias excepturi sint occaecati cupiditate non
provident, similique sunt in culpa qui officia deserunt mollitia
animi, id est laborum et dolorum fuga.

Et harum quidem rerum facilis est et expedita distinctio. Nam libero
tempore, cum soluta nobis est eligendi optio cumque nihil impedit
quo minus id quod maxime placeat facere possimus, omnis voluptas
assumenda est, omnis dolor repellendus."""

    # Repeat to get desired number of pages
    return (lorem + "\n\n") * pages


def split_text_into_lines(text, max_chars=75):
    """Split text into lines, breaking at word boundaries."""
    lines = []
    for paragraph in text.split('\n'):
        paragraph = paragraph.strip()
        if not paragraph:
            lines.append('')  # Preserve blank lines
            continue

        words = paragraph.split()
        current_line = ''

        for word in words:
            # If adding this word would exceed max, start new line
            if current_line and len(current_line) + len(word) + 1 > max_chars:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += ' ' + word
                else:
                    current_line = word

        if current_line:
            lines.append(current_line)

    return lines


def split_into_pages(lines, lines_per_page=18):
    """Split lines into page-sized chunks."""
    pages = []
    for i in range(0, len(lines), lines_per_page):
        pages.append(lines[i:i + lines_per_page])
    return pages


def convert_to_handwritten(input_text=None, output_prefix='output',
                           bias=0.75, style=9, input_file=None):
    """
    Convert text to handwritten SVG images on A4-sized pages.

    Args:
        input_text: Text string to convert (optional)
        output_prefix: Prefix for output files (default: 'output')
        bias: Handwriting neatness, 0.0-1.0 (default: 0.75)
        style: Handwriting style, 0-12 (default: 9)
        input_file: Path to text file to read (optional)
    """
    # Get input text
    if input_file:
        with open(input_file, 'r') as f:
            text = f.read()
    elif input_text:
        text = input_text
    else:
        print("Generating sample lorem ipsum text...")
        text = generate_lorem_ipsum(pages=2)

    # Process text into lines
    print("Splitting text into lines...")
    lines = split_text_into_lines(text, MAX_CHARS_PER_LINE)

    # Split into pages
    print(f"Splitting into pages ({LINES_PER_PAGE} lines per page)...")
    pages = split_into_pages(lines, LINES_PER_PAGE)
    print(f"Total pages: {len(pages)}")

    # Initialize handwriting model
    print("Loading handwriting model...")
    hand = Hand()

    # Generate each page
    for page_num, page_lines in enumerate(pages, 1):
        output_file = f'{output_prefix}_page_{page_num:02d}.svg'
        print(f"Generating page {page_num}/{len(pages)}: {output_file}")

        # Set parameters for all lines on this page
        biases = [bias] * len(page_lines)
        styles = [style] * len(page_lines)

        # Generate the handwritten output
        hand.write(
            filename=output_file,
            lines=page_lines,
            biases=biases,
            styles=styles,
            stroke_colors=['black'] * len(page_lines),
            stroke_widths=[2] * len(page_lines)
        )

    print(f"\nDone! Generated {len(pages)} pages.")
    print(f"Output files: {output_prefix}_page_*.svg")


def main():
    parser = argparse.ArgumentParser(
        description='Convert text to handwritten-style SVG images on A4 pages'
    )
    parser.add_argument('-i', '--input', type=str, help='Input text file')
    parser.add_argument('-o', '--output', type=str, default='output',
                       help='Output file prefix (default: output)')
    parser.add_argument('-b', '--bias', type=float, default=0.75,
                       help='Handwriting neatness 0.0-1.0 (default: 0.75)')
    parser.add_argument('-s', '--style', type=int, default=9,
                       help='Handwriting style 0-12 (default: 9)')
    parser.add_argument('--demo', action='store_true',
                       help='Generate demo with sample lorem ipsum text')

    args = parser.parse_args()

    if args.demo:
        convert_to_handwritten(
            output_prefix=args.output,
            bias=args.bias,
            style=args.style
        )
    elif args.input:
        convert_to_handwritten(
            input_file=args.input,
            output_prefix=args.output,
            bias=args.bias,
            style=args.style
        )
    else:
        parser.print_help()
        print("\nExample usage:")
        print("  # Generate demo with lorem ipsum:")
        print("  python lorem_to_handwritten.py --demo")
        print("\n  # Convert your own text file:")
        print("  python lorem_to_handwritten.py -i mytext.txt -o myhandwriting")
        print("\n  # Adjust style and neatness:")
        print("  python lorem_to_handwritten.py --demo -b 0.5 -s 7")


if __name__ == '__main__':
    main()
