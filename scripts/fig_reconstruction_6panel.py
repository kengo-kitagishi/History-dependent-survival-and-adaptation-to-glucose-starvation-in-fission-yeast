"""修論 fig:reconstruction の6枚版（2段×3列）。ICBBS 2026 ポスターの図
（共有ドライブ kitagishi/conferences/ICBBS_2026/work_poster_1115/recon2row/make_recon_2row_large.py）をもとにし、
Sideband cropped → Sideband centred を矢印でつなぐ。つなぎ方は2通り:
  snake: 2段目を右から左へ並べる（Sideband centred が右下）。右の列で真下へ1本の矢印。
  elbow: 2段目は左から右のまま。Sideband cropped の下から出て、直角に2回曲がり Sideband centred の上に入る。
元データ: figure-hub fig_qpi_reconstruction_chain_quad v001 の npz（260729 Pos94 frame 1566）。
再構成は build_fig1c_260729_data.py の field() と同じ
（fftshift(fft2) → 中心 (1638, 439)・直径 511 px の円板で切る → 511×511 を ifftshift → ifft2 → angle → unwrap）。
単位は pt（1 px = 1 pt）。  python scripts/fig_reconstruction_6panel.py --layout snake --out _view/recon6_snake
"""
import argparse
import pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.path import Path
from skimage.restoration import unwrap_phase

ap = argparse.ArgumentParser()
ap.add_argument("--layout", choices=["snake", "elbow"], required=True)
ap.add_argument("--out", required=True, help="拡張子なしの出力先（.png と .pdf を書く）")
args = ap.parse_args()

_HUB = "Desktop/figure-hub/library/fig_qpi_reconstruction_chain_quad/versions/v001/sources"
SRC = (pathlib.Path("G:/マイドライブ") / _HUB) if pathlib.Path("G:/マイドライブ").exists() else pathlib.Path.home() / _HUB
arr = np.load(SRC / "fig1c_260729_arrays.npz")
raw = arr["raw_full"].astype(np.float64)
N, AP, (CY, CX) = 2048, 511, (1638, 439)
PX_RAW = 3.45 / 40                    # µm/px
H = AP // 2
yy, xx = np.mgrid[0:N, 0:N]
disc = (yy - CY) ** 2 + (xx - CX) ** 2 < (AP / 2) ** 2

F = np.fft.fftshift(np.fft.fft2(raw))
logF = np.log1p(np.abs(F))
cropped = np.where(disc, logF, np.nan)
centred = np.full((N, N), np.nan)
c = N // 2
centred[c - H:c + H + 1, c - H:c + H + 1] = cropped[CY - H:CY + H + 1, CX - H:CX + H + 1]
sub = (F * disc)[CY - H:CY + H + 1, CX - H:CX + H + 1]
ph = unwrap_phase(np.angle(np.fft.ifft2(np.fft.ifftshift(sub))))
print("check vs npz: uncorrected max|diff| =", float(np.abs(ph - arr["phase_uncorrected"]).max()))
corr = arr["phase_background_subtracted"].astype(np.float64)
corr -= np.median(corr)               # 定数の位相オフセットを除く（表示用）

# ---- 配置（pt） ----
plt.rcParams.update({"font.family": "Arial", "font.size": 20, "pdf.fonttype": 42, "svg.fonttype": "none"})
P, GAP, TOP, ROWGAP, M = 133, 64, 27, 56, 14
CBG, CBW, CBL, BM = 8, 9, 58, 10              # カラーバー: パネルとの隙間・幅・目盛りの文字の幅（パネルの外に置く）
W = 2 * M + 3 * P + 2 * GAP + CBG + CBW + CBL
X0 = M + (CBG + CBW + CBL if args.layout == "snake" else 0)   # snake は Corrected phase が左下なので左に場所を空ける
Hh = 2 * (TOP + P) + ROWGAP + BM     # BM: 下の余白（目盛りの文字が切れないように）
fig = plt.figure(figsize=(W / 72, Hh / 72))
xs = [X0, X0 + P + GAP, X0 + 2 * (P + GAP)]
y_top0 = Hh - TOP                     # 1段目のパネル上端
y_bot0 = Hh - TOP - P                 # 1段目のパネル下端
y_top1 = y_bot0 - ROWGAP - TOP        # 2段目のパネル上端
yc = [y_bot0 + P / 2, y_top1 - P / 2] # 各段のパネル中央の高さ

def ax_at(col, row):
    y = y_bot0 if row == 0 else y_top1 - P
    return fig.add_axes([xs[col] / W, y / Hh, P / W, P / Hh])

TF, AF, CF = 20, 20, 15
cols2 = [2, 1, 0] if args.layout == "snake" else [0, 1, 2]   # 2段目の列の並び
pos = [(0, 0), (1, 0), (2, 0)] + [(cols2[i], 1) for i in range(3)]
gray = matplotlib.colormaps["gray"].copy(); gray.set_bad("black")
titles = ["Hologram", "Fourier transform", "Sideband cropped", "Sideband centred", "Phase", "Corrected phase"]
axes = [ax_at(cl, rw) for cl, rw in pos]
axes[0].imshow(raw, cmap="gray", vmin=40, vmax=1500, interpolation="lanczos")
for a, img in zip(axes[1:4], [logF, cropped, centred]):
    a.imshow(img, cmap=gray, vmin=10, vmax=21.5, interpolation="lanczos")
axes[4].imshow(ph, cmap="viridis", vmin=-60, vmax=2, interpolation="nearest")
im5 = axes[5].imshow(corr, cmap="viridis", vmin=-3, vmax=1, interpolation="nearest")
for a, t in zip(axes, titles):
    a.set_xticks([]); a.set_yticks([])
    a.set_title(t, fontsize=TF, pad=4)

# Fourier 面: 選んだ側波帯（実線、半径 NA/λ）と 0 次の範囲（破線、半径 2NA/λ）
axes[1].add_patch(Circle((CX, CY), AP / 2, fill=False, ec="white", lw=2))
axes[1].add_patch(Circle((N / 2, N / 2), AP, fill=False, ec="white", lw=2, ls=(0, (4, 2))))

# ホログラム: 縞が見える拡大（48 px ≈ 4 µm 四方）。拡大は右上
x0, y0, s = 1000, 1400, 48           # 元の位置: 右上の拡大・右下のスケールバーと重ならない所
axes[0].add_patch(Rectangle((x0, y0), s, s, fill=False, ec="#ffd166", lw=1.6))
ins = axes[0].inset_axes([0.52, 0.52, 0.46, 0.46])   # 拡大は右上
patch = raw[y0:y0 + s, x0:x0 + s]
ins.imshow(patch, cmap="gray", interpolation="nearest", vmin=np.percentile(patch, 1), vmax=np.percentile(patch, 99))
ins.set_xticks([]); ins.set_yticks([])
for sp in ins.spines.values(): sp.set_edgecolor("#ffd166"); sp.set_linewidth(2)
# 30 µm のスケールバー: 右下（左端のチャネル・右上の拡大と重ならない）（実空間の3枚に共通の縮尺）
bar = 30 / PX_RAW
axes[0].add_patch(Rectangle((N - 90 - bar, N - 130), bar, 28, color="white"))
axes[0].text(N - 90 - bar / 2, N - 160, "30 µm", color="white", fontsize=10, fontweight="bold", ha="center", va="bottom")
ins.add_patch(Rectangle((3, s - 6), 1 / PX_RAW, 2.2, color="white"))
ins.text(3, s - 9, "1 µm", color="white", fontsize=8.5, fontweight="bold")

# 色の目盛り（Corrected phase の右下）
# 色の目盛り: Corrected phase の外側（snake は左、elbow は右）に、パネルと同じ高さで置く
x5 = xs[cols2[2]]
cbx = x5 - CBG - CBW if args.layout == "snake" else x5 + P + CBG
cax = fig.add_axes([cbx / W, (y_top1 - P) / Hh, CBW / W, P / Hh])
cb = fig.colorbar(im5, cax=cax, ticks=[-3, -2, -1, 0, 1])
cb.ax.tick_params(labelsize=CF, length=3)
side = "left" if args.layout == "snake" else "right"
cax.yaxis.set_ticks_position(side); cax.yaxis.set_label_position(side)
cb.set_label("Phase (rad)", fontsize=CF, rotation=90 if side == "left" else 270, labelpad=2 if side == "left" else 16)

# ---- 矢印 ----
def f(p):                              # pt → figure 座標
    return (p[0] / W, p[1] / Hh)

def arrow_path(pts):
    path = Path([f(p) for p in pts], [Path.MOVETO] + [Path.LINETO] * (len(pts) - 1))
    fig.add_artist(FancyArrowPatch(path=path, transform=fig.transFigure, arrowstyle="-|>",
                                   mutation_scale=18, lw=2, color="black", joinstyle="miter"))

def h_arrow(col_from, col_to, y, label):
    if col_to > col_from:
        a, b = xs[col_from] + P + 8, xs[col_to] - 8
    else:
        a, b = xs[col_from] - 8, xs[col_to] + P + 8
    arrow_path([(a, y), (b, y)])
    fig.text((a + b) / 2 / W, (y + 14) / Hh, label, ha="center", va="bottom", fontsize=AF)

h_arrow(0, 1, yc[0], "FT")
h_arrow(1, 2, yc[0], "crop")
h_arrow(cols2[0], cols2[1], yc[1], "IFT")
h_arrow(cols2[1], cols2[2], yc[1], "− ref.")

y_start = y_bot0 - 4                  # Sideband cropped の下端のすぐ下
y_end = y_top1 + TOP - 2              # Sideband centred の見出しのすぐ上
xr = xs[2] + P / 2
if args.layout == "snake":
    arrow_path([(xr, y_start), (xr, y_end)])
    fig.text((xr + 8) / W, (y_start + y_end) / 2 / Hh, "shift", ha="left", va="center", fontsize=AF)
else:
    ym = y_bot0 - ROWGAP / 2
    xl = xs[0] + P / 2
    arrow_path([(xr, y_start), (xr, ym), (xl, ym), (xl, y_end)])
    fig.text((xs[1] + P + GAP / 2) / W, (ym + 3) / Hh, "shift", ha="center", va="bottom", fontsize=AF)

out = pathlib.Path(args.out)
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out.with_suffix(".png"), dpi=72 * 4)
fig.savefig(out.with_suffix(".pdf"))
print("saved", out.with_suffix(".png"), W, Hh)
