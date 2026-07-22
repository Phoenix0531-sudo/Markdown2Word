"""Business tests for Markdown2Word converter helpers (no pandoc binary)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_batch_convert_discovers_nested_md(tmp_path, monkeypatch):
    from converter import batch_converter

    src = tmp_path / "in"
    dst = tmp_path / "out"
    (src / "a").mkdir(parents=True)
    (src / "a" / "one.md").write_text("# hi\n", encoding="utf-8")
    (src / "two.md").write_text("# two\n", encoding="utf-8")
    (src / "skip.txt").write_text("x", encoding="utf-8")

    calls = []

    def fake_convert(md_file, out_path, fmt, template=None):
        calls.append((Path(md_file).name, Path(out_path).suffix, fmt))
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_text("ok", encoding="utf-8")

    monkeypatch.setattr(batch_converter, "convert_md_to_any", fake_convert)
    batch_converter.batch_convert(str(src), str(dst), fmt="docx")
    names = sorted(c[0] for c in calls)
    assert names == ["one.md", "two.md"]
    assert all(c[1] == ".docx" for c in calls)
    assert (dst / "two.docx").exists()
    assert (dst / "a" / "one.docx").exists()


def test_pdf_extra_args_include_xelatex(tmp_path, monkeypatch):
    from converter import pandoc_helper

    seen = {}

    def fake_convert_file(md_path, to=None, outputfile=None, extra_args=None):
        seen["to"] = to
        seen["args"] = list(extra_args or [])
        Path(outputfile).parent.mkdir(parents=True, exist_ok=True)
        Path(outputfile).write_text("pdf", encoding="utf-8")

    monkeypatch.setattr(pandoc_helper.pypandoc, "convert_file", fake_convert_file)
    out = tmp_path / "out.pdf"
    pandoc_helper.convert_md_to_any("x.md", str(out), "pdf")
    assert seen["to"] == "pdf"
    joined = " ".join(seen["args"])
    assert "xelatex" in joined
    assert "Microsoft YaHei" in joined
    assert out.exists()
