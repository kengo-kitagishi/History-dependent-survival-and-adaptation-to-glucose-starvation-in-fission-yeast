<!-- genre: thesis | layer: paragraph | section: measurement-system | parent: plot/2_measurement_system.md | child: 2.Measurement system.tex

各段落を Topic → Evidence → Implication → Bridge で組む。
Evidence の数値は ~/QPI_Omni の実コード・解析出力で裏を取る。裏が取れないものは本文に書かず、その旨を書く。
節ごとに plot が決まってから降ろす。2026-09-09 に 2.4 から始めた。
-->

# 第2章 QPIによる長期1細胞計測系の構築 — paragraph

## 2.4 位相像の再構成（9/9 確定）

**P1 再構成の手順**
- Topic: ホログラム1枚から位相像を得る手順は5段階。
- Evidence: (1) 2D 離散 FT。スペクトルは非干渉項と、±k^off に離れた干渉項の3成分。(2) +1次サイドバンドの中心を見つけ、e^{+i(k_m m + k_n n)} を掛けて原点へ移す。(3) 半径 r = (NA/λ)·N·Δp 画素の円窓で切る。(4) 2D 逆 FT で複素場、その arg が位相。(5) 2π の折り返しを reliability-ordered 法（Herráez 2002）で外す。コードは skimage.restoration.unwrap_phase（同じ算法）。図 fig:reconstruction。
- Implication: 円窓の半径は対物の NA で決まるので、位相像の分解能は光学系で決まり、処理では変わらない。
- Bridge: この位相にはまだ照明の波面と流路の位相が乗っている。

**P2 背景の除去**
- Topic: 同じ視野の、細胞のない位相像（参照像）を引く。
- Evidence: φ = arg[LP(I_sample e^{…}) / LP(I_ref e^{…})]。複素場の比の arg なので位相の差になる。残るオフセットは細胞のない領域の平均で除く。OPD に直すなら φλ/2π だが、以降は位相 φ（rad）で扱う。
- Implication: 照明の波面と流路の位相は参照像と共通なので、これで消える。
- Bridge: mother machine では細胞のそばに培地だけの領域が残らないので、参照像をどう取るかが問題になる。取り方は 2.7.6、どの参照像を引くかは 2.8.2。

**P3 分解能と Fourier 面のパラメータ**
- Topic: 位相像の画素数と画素サイズは NA と視野で決まる。
- Evidence: カットオフ f = NA/λ（Abbe 限界 λ/NA、コヒーレント照明）。N×N 画素・物体面画素 Δp のホログラムで FOV = NΔp。円窓の直径 D_ap = 2⌊(NA/λ)·FOV⌋+1 画素。再構成画素 Δp_recon = FOV/D_ap ≈ λ/2NA。
- Implication: 位相像の画素は分解能要素の半分で、Nyquist をちょうど満たす。
- Bridge: 生ホログラムの側にも条件がある。

**P4 サンプリング条件**
- Topic: 条件は2段階。
- Evidence: 生ホログラムは Δp < λ/2NA。干渉縞を写すので実際は 2〜4 倍の余裕をとる。位相像は 1 分解能要素 λ/NA ≈ 2 画素。
- Implication: 生ホログラムの余裕は、干渉項が Nyquist を超えないという 2.5 の設計条件 (ii) と同じ要求。
- Bridge: 我々の系の値。

**P5 我々の値**
- Topic: 我々の系はこの条件を満たす。
- Evidence: λ = 658 nm、NA 0.95、40×、カメラ画素 3.45 µm。Δp = 3.45/40 = 86.25 nm。FOV = 2048 × 86.25 nm = 176.6 µm。Abbe 692 nm。Nyquist 346 nm。余裕 346/86.25 = 4.0。D_ap = 2⌊(0.95/658 nm) × 176.6 µm⌋ + 1 = 511。Δp_recon = 176.6 µm / 511 = 346 nm。
- Implication: 位相像は 511×511 画素、画素 0.346 µm。論文の値と一致する。
- Bridge: k^off をどの範囲に置くかが光学系の設計条件になる → 2.5。
