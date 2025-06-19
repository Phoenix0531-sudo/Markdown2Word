import pypandoc

def convert_md_to_any(md_path, out_path, fmt, template=None, extra_args=None):
    args = extra_args.copy() if extra_args else []
    if template:
        args.extend(['--template', template])
    # 针对 PDF，增加中文支持参数，全部用微软雅黑
    if fmt == "pdf":
        args.extend([
            '--pdf-engine=xelatex',
            '-V', 'mainfont=Microsoft YaHei',
            '-V', 'monofont=Microsoft YaHei'
        ])

    pypandoc.convert_file(
        md_path,
        to=fmt,
        outputfile=out_path,
        extra_args=args
    )
