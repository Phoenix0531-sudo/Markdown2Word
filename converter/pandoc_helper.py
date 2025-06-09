import pypandoc

def convert_md_to_any(md_path, out_path, fmt, template=None, extra_args=None):
    args = ['--from=gfm']
    if template and fmt == "docx":
        args += [f'--reference-doc={template}']
    if extra_args:
        args += extra_args
    pypandoc.convert_file(md_path, fmt, outputfile=out_path, extra_args=args)
