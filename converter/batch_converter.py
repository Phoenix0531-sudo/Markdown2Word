import os, glob
from .pandoc_helper import convert_md_to_any

def batch_convert(input_dir, output_dir, fmt="docx", template=None, progress_callback=None):
    md_files = glob.glob(os.path.join(input_dir, '**/*.md'), recursive=True)
    total = len(md_files)
    for idx, md_file in enumerate(md_files, 1):
        rel_path = os.path.relpath(md_file, input_dir)
        out_path = os.path.join(output_dir, os.path.splitext(rel_path)[0] + f'.{fmt}')
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        convert_md_to_any(md_file, out_path, fmt, template)
        if progress_callback:
            progress_callback(idx, total, md_file)
