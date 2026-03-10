"""One-off script: convert ordervez_knowledge_base.md to PDF. Run from project root."""
import re
from pathlib import Path

from fpdf import FPDF

DOC_DIR = Path(__file__).resolve().parent
MD_FILE = DOC_DIR / "ordervez_knowledge_base.md"
PDF_FILE = DOC_DIR / "ordervez_knowledge_base.pdf"

MAX_CHAR_WIDTH = 90  # break long lines so they fit in cell


def wrap_long_line(text: str) -> str:
    """Insert newlines so no line exceeds MAX_CHAR_WIDTH (break at spaces)."""
    words = text.split()
    lines = []
    current = []
    for w in words:
        trial = " ".join(current + [w]) if current else w
        if len(trial) <= MAX_CHAR_WIDTH:
            current.append(w)
        else:
            if current:
                lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return "\n".join(lines) if lines else text


def to_ascii(s: str) -> str:
    """Replace non-ASCII with closest ASCII so Helvetica works."""
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2013", "-")
    s = s.replace("\u2022", "-").replace("\u2014", "-")
    return s.encode("ascii", "replace").decode("ascii")


def strip_md(line: str) -> str:
    """Remove markdown bold and headers; return ASCII-safe text."""
    s = line.strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"^-\s*", "  - ", s)
    return to_ascii(s)


def main():
    text = MD_FILE.read_text(encoding="utf-8")
    pdf = FPDF()
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    cell_w = pdf.w - pdf.l_margin - pdf.r_margin

    for line in text.splitlines():
        line = line.strip()
        if not line or line == "---":
            pdf.ln(6)
            continue
        plain = strip_md(line)
        if not plain:
            continue
        if line.startswith("# "):
            pdf.set_font("Helvetica", "B", 16)
            pdf.multi_cell(cell_w, 10, wrap_long_line(plain))
            pdf.set_font("Helvetica", size=11)
        elif line.startswith("## "):
            pdf.set_font("Helvetica", "B", 13)
            pdf.multi_cell(cell_w, 8, wrap_long_line(plain))
            pdf.set_font("Helvetica", size=11)
        elif line.startswith("### "):
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(cell_w, 7, wrap_long_line(plain))
            pdf.set_font("Helvetica", size=11)
        else:
            pdf.multi_cell(cell_w, 6, wrap_long_line(plain))

    pdf.output(str(PDF_FILE))
    print(f"Wrote {PDF_FILE}")


if __name__ == "__main__":
    main()
