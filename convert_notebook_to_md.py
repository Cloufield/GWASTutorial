#!/usr/bin/env python3
"""
Convert Jupyter notebooks (.ipynb) to Markdown (.md) files.
Extracts images and other outputs, saving them to a specified directory.
Handles HTML tables by converting them to markdown tables.
"""

import os
import re
import json
import argparse
import base64
from pathlib import Path
from typing import Optional, Tuple, Dict, List, Any
from html.parser import HTMLParser

try:
    import nbformat
    from nbconvert import MarkdownExporter
    from traitlets.config import Config
except ImportError:
    print("Error: nbformat and nbconvert are required.")
    print("Install them with: pip install nbformat nbconvert")
    exit(1)


class TableHTMLParser(HTMLParser):
    """Parser to extract table data from HTML."""
    def __init__(self):
        super().__init__()
        self.headers = []
        self.rows = []
        self.current_row = []
        self.in_table = False
        self.in_thead = False
        self.in_tbody = False
        self.in_tr = False
        self.in_cell = False
        self.current_cell = []
    
    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower == 'table':
            self.in_table = True
        elif tag_lower == 'thead':
            self.in_thead = True
        elif tag_lower == 'tbody':
            self.in_tbody = True
        elif tag_lower == 'tr':
            self.in_tr = True
            self.current_row = []
        elif tag_lower in ('td', 'th'):
            self.in_cell = True
            self.current_cell = []
    
    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower == 'table':
            self.in_table = False
        elif tag_lower == 'thead':
            self.in_thead = False
        elif tag_lower == 'tbody':
            self.in_tbody = False
        elif tag_lower == 'tr':
            if self.current_row:
                if self.in_thead:
                    if not self.headers:
                        self.headers = self.current_row[:]
                else:
                    self.rows.append(self.current_row[:])
            self.current_row = []
            self.in_tr = False
        elif tag_lower in ('td', 'th'):
            if self.in_cell:
                cell_text = ''.join(self.current_cell).strip()
                self.current_row.append(cell_text)
                self.current_cell = []
                self.in_cell = False
    
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)


def parse_html_table(html: str) -> Optional[Tuple[List[str], List[List[str]]]]:
    """Parse HTML table and return (headers, rows)."""
    parser = TableHTMLParser()
    try:
        parser.feed(html)
        if parser.headers and parser.rows:
            return (parser.headers, parser.rows)
    except Exception:
        pass
    return None


def html_table_to_markdown(html: str, max_rows: int = 20) -> Optional[str]:
    """Convert HTML table to markdown table format."""
    # Try to extract table size info
    table_size_info = None
    size_patterns = [
        r'\[(\d+)\s+rows?\s+x\s+(\d+)\s+columns?\]',
        r'(\d+)\s+rows?\s+x\s+(\d+)\s+columns?',
        r'\[(\d+)\s+rows?,\s+(\d+)\s+columns?\]',
    ]
    
    for pattern in size_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            num_rows = int(match.group(1))
            num_cols = int(match.group(2))
            table_size_info = f"[{num_rows} rows x {num_cols} columns]"
            break
    
    table_data = parse_html_table(html)
    if not table_data:
        return None
    
    headers, rows = table_data
    
    if not headers or not rows:
        return None
    
    # Remove index column (first column if header is empty or mostly numeric)
    remove_first = False
    if len(headers) > 1 and len(rows) > 0:
        first_header = headers[0].strip()
        if not first_header:
            remove_first = True
        else:
            try:
                sample_rows = min(50, len(rows))
                first_col_values = [row[0].strip() for row in rows[:sample_rows] if len(row) > 0 and row[0].strip()]
                
                if len(rows) > sample_rows:
                    last_col_values = [row[0].strip() for row in rows[-sample_rows:] if len(row) > 0 and row[0].strip()]
                    first_col_values.extend(last_col_values)
                
                if len(first_col_values) >= 5:
                    numeric_count = sum(1 for val in first_col_values if val.isdigit())
                    if numeric_count >= len(first_col_values) * 0.8:
                        remove_first = True
            except (ValueError, IndexError):
                pass
    
    if remove_first and len(headers) > 1:
        headers = headers[1:]
        rows = [row[1:] if len(row) > 1 else row for row in rows]
    
    # Remove columns with empty headers
    empty_header_indices = [i for i, header in enumerate(headers) if not header.strip()]
    if empty_header_indices:
        for idx in sorted(empty_header_indices, reverse=True):
            if idx < len(headers):
                headers.pop(idx)
                rows = [row[:idx] + row[idx+1:] if len(row) > idx else row for row in rows]
    
    # Ensure all headers are non-empty
    if not headers or any(not h.strip() for h in headers):
        valid_indices = [i for i, h in enumerate(headers) if h.strip()]
        if not valid_indices:
            return None
        headers = [headers[i] for i in valid_indices]
        rows = [[row[i] if i < len(row) else '' for i in valid_indices] for row in rows]
    
    # Create markdown table
    md_lines = []
    md_lines.append('| ' + ' | '.join(headers) + ' |')
    md_lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    
    # Show preview if table is large
    if len(rows) > max_rows:
        for row in rows[:max_rows//2]:
            while len(row) < len(headers):
                row.append('')
            row = row[:len(headers)]
            md_lines.append('| ' + ' | '.join(row) + ' |')
        
        ellipsis_row = ['...'] * len(headers)
        md_lines.append('| ' + ' | '.join(ellipsis_row) + ' |')
        
        for row in rows[-max_rows//2:]:
            while len(row) < len(headers):
                row.append('')
            row = row[:len(headers)]
            md_lines.append('| ' + ' | '.join(row) + ' |')
    else:
        for row in rows:
            while len(row) < len(headers):
                row.append('')
            row = row[:len(headers)]
            md_lines.append('| ' + ' | '.join(row) + ' |')
    
    if table_size_info:
        md_lines.append('')
        md_lines.append(f'*{table_size_info}*')
    
    return '\n'.join(md_lines)


def save_image(image_data: str, image_format: str, notebook_name: str, image_index: int,
               output_dir: Path, images_dir: Path) -> str:
    """Save image to disk and return markdown image reference."""
    images_dir.mkdir(parents=True, exist_ok=True)
    
    image_filename = f"{notebook_name}_img_{image_index}.{image_format}"
    image_path = images_dir / image_filename
    
    if image_format == 'svg':
        with open(image_path, 'w', encoding='utf-8') as f:
            f.write(image_data)
    else:
        image_bytes = base64.b64decode(image_data)
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
    
    # Return relative path from output_dir to image
    rel_path = os.path.relpath(image_path, output_dir)
    return rel_path.replace('\\', '/')


def extract_image_data(output: Dict[str, Any]) -> Optional[tuple]:
    """Extract image data from notebook output."""
    if 'data' in output:
        data = output['data']
        if 'image/png' in data:
            return ('png', data['image/png'])
        elif 'image/jpeg' in data:
            return ('jpeg', data['image/jpeg'])
        elif 'image/svg+xml' in data:
            return ('svg', data['image/svg+xml'])
    return None


def convert_notebook_to_md(
    ipynb_path: Path,
    md_output_path: Optional[Path] = None,
    images_dir: Optional[Path] = None,
    include_outputs: bool = True,
    strip_outputs: bool = False,
) -> Tuple[Path, Path]:
    """
    Convert a Jupyter notebook (.ipynb) to a Markdown (.md) file.
    Saves images/attachments to images_dir and updates links accordingly.

    Args:
        ipynb_path: Path to the input .ipynb file
        md_output_path: Where to save .md; default same name as ipynb with .md extension
        images_dir: Directory to save image files (relative to md_output_path parent)
        include_outputs: Whether to include code outputs in markdown
        strip_outputs: Whether to remove outputs from code cells before conversion

    Returns:
        Tuple of (markdown_path, images_directory_path)
    """
    # Resolve paths
    ipynb_path = Path(ipynb_path).resolve()
    if not ipynb_path.exists():
        raise FileNotFoundError(f"Notebook not found: {ipynb_path}")

    notebook_base = ipynb_path.stem
    notebook_dir = ipynb_path.parent

    # Determine output markdown path
    if md_output_path is None:
        md_output_path = notebook_dir / f"{notebook_base}.md"
    else:
        md_output_path = Path(md_output_path).resolve()

    # Determine images directory - use central images/notebooks/ directory
    if images_dir is None:
        # Default: use docs/images/notebooks/ for central storage
        docs_dir = md_output_path.parent
        images_dir = docs_dir / 'images' / 'notebooks'
    else:
        images_dir = Path(images_dir).resolve()

    # Create images directory
    images_dir.mkdir(parents=True, exist_ok=True)

    # Read notebook as JSON for better control
    print(f"Reading notebook: {ipynb_path}")
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Build markdown content manually for better control
    md_lines = []
    image_index = 0

    for cell in notebook.get('cells', []):
        cell_type = cell.get('cell_type', '')
        source = cell.get('source', [])
        
        if isinstance(source, list):
            cell_content = ''.join(source)
        else:
            cell_content = str(source)
        
        if cell_type == 'markdown':
            md_lines.append(cell_content)
            md_lines.append('')
        
        elif cell_type == 'code':
            if cell_content.strip():
                language = 'python'
                if cell_content.strip().startswith('%%'):
                    first_line = cell_content.split('\n')[0]
                    if 'bash' in first_line or 'sh' in first_line:
                        language = 'bash'
                    elif 'r' in first_line or 'R' in first_line:
                        language = 'r'
                
                md_lines.append(f'```{language}')
                md_lines.append(cell_content.rstrip())
                md_lines.append('```')
                md_lines.append('')
            
            # Handle outputs
            if include_outputs and not strip_outputs:
                outputs = cell.get('outputs', [])
                for output in outputs:
                    output_type = output.get('output_type', '')
                    
                    if output_type == 'stream':
                        name = output.get('name', 'stdout')
                        text = ''.join(output.get('text', []))
                        if text.strip():
                            md_lines.append(f'**{name}:**')
                            md_lines.append('```')
                            md_lines.append(text.rstrip())
                            md_lines.append('```')
                            md_lines.append('')
                    
                    elif output_type in ('execute_result', 'display_data'):
                        # Check for images first
                        image_info = extract_image_data(output)
                        if image_info:
                            image_format, image_data = image_info
                            image_path = save_image(
                                image_data, image_format, notebook_base, image_index,
                                md_output_path.parent, images_dir
                            )
                            md_lines.append(f'![Output image]({image_path})')
                            md_lines.append('')
                            image_index += 1
                            continue
                        
                        # Check for HTML tables
                        if 'data' in output:
                            data = output['data']
                            if 'text/html' in data:
                                html = ''.join(data['text/html'])
                                if '<table' in html.lower():
                                    markdown_table = html_table_to_markdown(html, max_rows=20)
                                    if markdown_table:
                                        md_lines.append(markdown_table)
                                        md_lines.append('')
                                        continue
                                    else:
                                        # Fallback: wrap HTML in div
                                        md_lines.append(f'<div style="font-size: 0.85em; line-height: 1.3;">\n{html}\n</div>')
                                        md_lines.append('')
                                        continue
                            
                            # Handle text output
                            if 'text/plain' in data:
                                text = ''.join(data['text/plain'])
                                if text.strip():
                                    md_lines.append('```')
                                    md_lines.append(text.rstrip())
                                    md_lines.append('```')
                                    md_lines.append('')

    # Use nbconvert for the rest (markdown cells, etc.) but we've already processed code cells
    # Actually, let's use our manual processing for everything
    body = '\n'.join(md_lines)

    # Post-process markdown body
    body = post_process_markdown(body)

    # Write markdown file
    print(f"Writing markdown: {md_output_path}")
    with open(md_output_path, 'w', encoding='utf-8') as fmd:
        fmd.write(body)

    print(f"✓ Converted {ipynb_path.name} → {md_output_path.name}")
    if image_index > 0:
        print(f"  Saved {image_index} image(s) to {images_dir}")
    
    return md_output_path, images_dir


def post_process_markdown(markdown: str) -> str:
    """
    Post-process the markdown content to fix common issues.
    
    Args:
        markdown: Raw markdown content
        
    Returns:
        Cleaned markdown content
    """
    # Remove excessive blank lines (more than 2 consecutive)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    # Fix code block formatting
    markdown = re.sub(r'\n```(\w+)\n', r'\n\n```\1\n', markdown)
    markdown = re.sub(r'\n```\n', r'\n\n```\n', markdown)
    
    # Clean up trailing whitespace
    lines = markdown.split('\n')
    lines = [line.rstrip() for line in lines]
    markdown = '\n'.join(lines)
    
    return markdown.strip() + '\n'


def convert_all_notebooks(
    root_dir: Path,
    output_dir: Optional[Path] = None,
    include_outputs: bool = True,
    strip_outputs: bool = False,
    recursive: bool = True,
) -> None:
    """
    Convert all notebooks in a directory (recursively).
    
    Args:
        root_dir: Root directory to search for notebooks
        output_dir: Directory to save markdown files (default: same as notebook location)
        include_outputs: Whether to include code outputs
        strip_outputs: Whether to strip outputs before conversion
        recursive: Whether to search recursively
    """
    root_dir = Path(root_dir).resolve()
    
    # Find all .ipynb files
    if recursive:
        notebooks = list(root_dir.rglob('*.ipynb'))
    else:
        notebooks = list(root_dir.glob('*.ipynb'))
    
    # Filter out notebooks in site/ and .ipynb_checkpoints/
    notebooks = [
        nb for nb in notebooks
        if 'site/' not in str(nb) and '.ipynb_checkpoints' not in str(nb)
    ]
    
    print(f"Found {len(notebooks)} notebook(s) to convert")
    print()
    
    for notebook in notebooks:
        try:
            if output_dir:
                rel_path = notebook.relative_to(root_dir)
                md_path = output_dir / rel_path.with_suffix('.md')
                md_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                md_path = None
            
            convert_notebook_to_md(
                notebook,
                md_output_path=md_path,
                include_outputs=include_outputs,
                strip_outputs=strip_outputs,
            )
            print()
        except Exception as e:
            print(f"✗ Error converting {notebook}: {e}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebook(s) to Markdown with images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a single notebook
  python convert_notebook_to_md.py notebook.ipynb

  # Convert with custom output path
  python convert_notebook_to_md.py notebook.ipynb --md output.md

  # Convert all notebooks in current directory
  python convert_notebook_to_md.py --all .

  # Convert all notebooks recursively, strip outputs
  python convert_notebook_to_md.py --all . --strip-outputs

  # Convert to specific output directory
  python convert_notebook_to_md.py --all . --output-dir docs/
        """
    )
    
    parser.add_argument(
        'notebook',
        nargs='?',
        help='Path to .ipynb file to convert'
    )
    
    parser.add_argument(
        '--md',
        '--output',
        dest='md_output',
        help='Output markdown file path (default: same name as notebook with .md)'
    )
    
    parser.add_argument(
        '--images',
        '--images-dir',
        dest='images_dir',
        help='Directory to save images (default: docs/images/notebooks/)'
    )
    
    parser.add_argument(
        '--no-outputs',
        action='store_true',
        help='Exclude code outputs from markdown'
    )
    
    parser.add_argument(
        '--strip-outputs',
        action='store_true',
        help='Remove outputs from code cells before conversion'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Convert all notebooks in the specified directory'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory for batch conversion (used with --all)'
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Do not search recursively (used with --all)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.all and not args.notebook:
        parser.error("Either provide a notebook path or use --all to convert all notebooks")
    
    if args.all:
        # Batch conversion
        if args.notebook:
            root_dir = Path(args.notebook)
        else:
            root_dir = Path.cwd()
        
        if not root_dir.exists():
            parser.error(f"Directory does not exist: {root_dir}")
        
        output_dir = Path(args.output_dir) if args.output_dir else None
        
        convert_all_notebooks(
            root_dir=root_dir,
            output_dir=output_dir,
            include_outputs=not args.no_outputs,
            strip_outputs=args.strip_outputs,
            recursive=not args.no_recursive,
        )
    else:
        # Single notebook conversion
        notebook_path = Path(args.notebook)
        if not notebook_path.exists():
            parser.error(f"Notebook not found: {notebook_path}")
        
        md_output = Path(args.md_output) if args.md_output else None
        images_dir = Path(args.images_dir) if args.images_dir else None
        
        convert_notebook_to_md(
            ipynb_path=notebook_path,
            md_output_path=md_output,
            images_dir=images_dir,
            include_outputs=not args.no_outputs,
            strip_outputs=args.strip_outputs,
        )


if __name__ == '__main__':
    main()
