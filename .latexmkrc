$pdf_mode = 5;  # Use xelatex
$postscript_mode = $dvi_mode = 0;

# Some editors invoke latexmk with -pdf (pdflatex mode).
# This thesis uses fontspec/xeCJK, so force those calls to XeLaTeX as well.
$pdflatex = 'xelatex %O %S';
$xelatex = 'xelatex %O %S';
