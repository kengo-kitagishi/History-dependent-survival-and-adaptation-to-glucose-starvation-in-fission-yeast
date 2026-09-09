<!-- genre: thesis | layer: paragraph | section: measurement-system | parent: plot/2_measurement_system.md | child: 2.Measurement system.tex

各段落を Topic → Evidence → Implication → Bridge で組む。
Evidence の数値は ~/QPI_Omni の実コード・解析出力で裏を取る。裏が取れないものは本文に書かず、その旨を書く。
節ごとに plot が決まってから降ろす。
-->

# 第2章 QPIによる長期1細胞計測系の構築 — paragraph

## 2.4 位相像の再構成

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
- Evidence: カットオフ f = NA/λ（Abbe 限界 λ/NA、コヒーレント照明）。N×N 画素・物体面画素 Δp のホログラムで FOV = NΔp。円窓の直径 D_ap = 2·round((NA/λ)·FOV)+1 画素（コード qpi.py の aperturesize と同じ式）。再構成画素 Δp_recon = FOV/D_ap ≈ λ/2NA。
- Implication: 位相像の画素は分解能要素の半分で、Nyquist をちょうど満たす。
- Bridge: 生ホログラムの側にも条件がある。

**P4 サンプリング条件**
- Topic: 条件は2段階。
- Evidence: 生ホログラムは Δp < λ/2NA。干渉縞を写すので実際は 2〜4 倍の余裕をとる。位相像は 1 分解能要素 λ/NA ≈ 2 画素。
- Implication: 生ホログラムの余裕は、干渉項が Nyquist を超えないという 2.5 の設計条件 (ii) と同じ要求。
- Bridge: 我々の系の値。

**P5 我々の値**
- Topic: 我々の系はこの条件を満たす。
- Evidence: λ = 658 nm、NA 0.95、40×、カメラ画素 3.45 µm。Δp = 3.45/40 = 86.25 nm。FOV = 2048 × 86.25 nm = 176.64 µm。Abbe 692 nm。Nyquist 346 nm。余裕 346/86.25 = 4.0。(NA/λ)·FOV = 255.0 → D_ap = 2·round(255.0) + 1 = 511。Δp_recon = 176.64 µm / 511 = 346 nm。
- Implication: 位相像は 511×511 画素、画素 0.346 µm。論文の値と一致する。
- Bridge: k^off をどの範囲に置くかが光学系の設計条件になる → 2.5。

## 2.5 光学系

**P1 設計条件**
- Topic: off-axis DH の設計条件は2つ。
- Evidence: (i) 干渉項と非干渉項が重ならない: 干渉項の半径 2πNA/λM、非干渉項はその2倍 → k^off ≥ 3·2πNA/λM。(ii) 干渉項が Nyquist を超えない、対角方向が最も厳しい → k^off/√2 + 2πNA/λM ≤ πf_pitch。合わせて 2π·3NA/λM ≤ k^off ≤ √2π(f_pitch − 2NA/λM)。NA 0.95、M 40、λ 658 nm、画素 3.45 µm（f_pitch = 2.90×10⁵ m⁻¹）で 6.80×10⁵ ≤ k^off ≤ 9.68×10⁵ rad/m。
- Implication: k^off の許容範囲は NA・倍率・画素ピッチだけで決まる。
- Bridge: 実際の k^off は格子で決まる。

**P2 構成**
- Topic: common-path off-axis DH（diffraction phase microscopy）を Ti-E の出力ポートに組んだ。
- Evidence: 658 nm・20 mW LD（LP660-SF20）→ コリメータ（CFC2-B, f = 2 mm）→ 試料 → 40×/0.95 乾燥系（CFI Plan Apochromat Lambda D, MRD70470）→ 像面の Ronchi 格子 120 lines/mm（#66-342）→ 4f リレー 2×ACT508-200-A（f = 200 mm）→ Fourier 面の 25 µm ピンホール（P25K）で 0 次を参照光、1 次はそのまま物体光、他の次数は遮る → CMOS acA2440-75um（2448×2048、3.45 µm、FWC ≈ 10 ke⁻）。生ホログラム 2048×2048、位相像 511×511・0.346 µm。図 fig:qpi_optical_system。
- Implication: 2光が同じ光路を通るので振動と光学系のずれに強い（2.1.2 の条件 (2)）。
- Bridge: 格子の周期が k^off を決める。

**P3 格子から決まる k^off**
- Topic: k^off = 2π/8.33 µm = 7.54×10⁵ rad/m。
- Evidence: 格子 120 lines/mm、4f リレーの倍率 1 なのでセンサ面でも周期 8.33 µm。
- Implication: P1 の範囲に入る。
- Bridge: 実測で確かめる。

**P4 off-axis 配置の検証**
- Topic: 実測のキャリア周波数が格子からの計算と一致する。
- Evidence: 2048² ホログラムの FT で DC (1024, 1024)、+1 次の中心 (1623, 1621)、ずれ (599, 597) 画素、大きさ 845.8 画素。Δf_sensor = 1/(2048 × 3.45 µm) = 141.5 m⁻¹。f = 845.8 × 141.5 = 1.20×10⁵ cycles/m → k_exp = 7.53×10⁵ rad/m。
- Implication: 格子による off-axis 配置は設計どおり。
- Bridge: 位相ノイズの実測は 2.9。

## 2.6 マイクロ流路デバイス

**P1 mother machine の原理**
- Topic: 細胞を同じ視野に数日とどめ、子孫を除きながら培地を一定に保つために mother machine を使う。
- Evidence: 主流路1本と、それに垂直な行き止まりの観察チャネル多数。チャネル幅は細胞1個分。閉端の母細胞はとどまり、娘は主流路へ押し出されて流される。培地は拡散で秒の桁で届き、取り込み（分の桁）より速い（Wang 2010）。分裂酵母でも老化・寿命の計測に使われた（Nakaoka 2017）。図 fig:mm_schematic。
- Implication: 2.1.2 の条件 (1) 長期の1細胞追跡を満たす。
- Bridge: 本研究のデバイスの寸法。

**P2 デバイスの構成**
- Topic: Nakaoka 2017 の設計に倣って自作した。
- Evidence: 観察チャネル 幅 5.3 µm × 高さ 6.2 µm。主流路（ドレイン）幅 214 µm × 高さ 19.75 µm（2026-08-20 に本人が確定した値。長さ・間隔・本数は設計ファイル待ち）。高さが2段階なので鋳型は SU-8 2層。両端をチューブでシリンジと廃液につなぎ、2 mL/h で灌流。図 fig:mm_layout。
- Implication: チャネルの幅と高さが細胞1個分なので、細胞は1列で増える。
- Bridge: 作製の工程。

**P3 鋳型とフォトマスク**
- Topic: 鋳型はシリコンウェハ上の SU-8 2層。
- Evidence: マスクは μMLA（Heidelberg）でマスクブランクス（Clean Surface Technology）に描画、チャネルとドレインで別。観察チャネル層: SU-8 2 + 3005 を 3000 rpm 30 s、65 °C 1 min・95 °C 2 min、MA-20 で 5 s × 3 露光、65 °C 1 min・95 °C 3 min、現像・IPA。ドレイン層: SU-8 3010 を 1500 rpm 30 s、65 °C 1 min・95 °C 8 min、1層目のマークに合わせて 30 s 露光、65 °C 3 min・95 °C 10 min、現像。
- Implication: 2層の高さがチャネルとドレインの高さになる。
- Bridge: 鋳型から PDMS を作る。

**P4 PDMS と接合**
- Topic: PDMS を鋳造してカバーガラスに接合する。
- Evidence: SYLGARD 184 を 10:1、真空脱泡 1 h、65 °C 12 h 以上。0.5 mm 生検トレパン（BP-A05F）で穴。エタノール超音波洗浄、65 °C 乾燥。カバーガラス（Neo No.1, Matsunami）は Contaminon LS-II 希釈液・超純水・エタノール・超純水で超音波洗浄、0.1 M NaOH、超純水、140 °C 乾燥。FA-1（Samco）で 10 s プラズマ処理して貼り合わせ。
- Implication: 流路は PDMS とカバーガラスで密閉され、カバーガラス側から観察する。
- Bridge: 日常の鋳造。

**P5 エポキシレプリカ**
- Topic: 日常の鋳造にはエポキシのレプリカを型にする。
- Evidence: 鋳型から PDMS のネガ型を取り、EA E-30CL（Loctite）を流して 24 h 以上硬化。図 fig:pdms_process。手順書（受け入れ条件・トラブル対応）は Appendix C。
- Implication: シリコンの鋳型を消耗させずに済む。
- Bridge: 細胞の準備と計測へ（2.7）。
