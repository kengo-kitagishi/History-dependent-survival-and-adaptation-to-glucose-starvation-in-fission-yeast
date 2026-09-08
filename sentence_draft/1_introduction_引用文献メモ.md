<!-- genre: thesis | layer: references | section: introduction | source: 1.Introduction.tex の 164–246行目 引用文献リスト（主要なもの）
     2026-09-08 に .tex から切り出した。Markdown が .tex の中にあってビルドが壊れていたため。
     中身は一字も変えていない。 -->

## 引用文献リスト（主要なもの）
 
| Reference | 用途 |
|---|---|
| Broach JR (2012) Genetics 192:73 | 酵母の栄養センシング総説 |
| Kussell & Leibler (2005) Science 309:2075 | bet-hedging, 表現型多様性 |
| Gray et al. (2004) Microbiol Mol Biol Rev 68:187 | 酵母休眠（quiescence）総説 |
| De Virgilio (2012) FEMS Microbiol Rev | 酵母飢餓応答総説 |
| Zimmerman & Trach (1991) J Mol Biol 222:599 | 細胞内高分子濃度300-400 g/L |
| Minton AP (2001) J Biol Chem 276:10577 | クラウディング概念 |
| Ellis RJ (2001) Trends Biochem Sci 26:597 | クラウディング総説 |
| Munder et al. (2016) eLife 5:e09347 | 細胞質fluid→solid転移・dormancy |
| Joyner et al. (2016) eLife 5:e09376 | 飢餓時の拡散低下 |
| Franzmann et al. (2018) Science 359:eaao5654 | Sup35相分離・細胞保護 |
| Hyman et al. (2014) Annu Rev Cell Dev Biol 30:39 | LLPS in biology総説 |
| Petrovska et al. (2014) eLife 3:e02409 | 代謝酵素フィラメント・飢餓 |
| Delarue et al. (2018) Cell 174:338 | GEM probe・クラウディング・mTORC1 |
| Höfling & Franosch (2013) Rep Prog Phys | 細胞内異常拡散総説 |
| Alfano et al. (2024) Chem Rev | クラウディング総説（ユーザー提示論文） |
 
一般的背景（Communication purpose)
(Molecular crowding is a prominent physical property of the cytoplasm. )
The very high concentration of macromolecules within cells can potentially have an overwhelming effect on the thermodynamic activity of cellular components
There are several conceptual model used to describe the influence of molecular crowding on biochemical reaction.

- Zhou argued that bulky, macromolecules exclude volume arising from steric repulsion and increase the thermodynamic activity of molecules entropically by reducing the accessible volume, thereby promoting reaction that decrease total excluded volume, such as macromolecular complex formation and protein folding.

- Also, Chen used Xenopus laevis egg extract which is cytoplasmic system that support some biological function, showed that biochemical reaction rate nearly peak at physiological cytoplasmic concentration. Protein synthesis measured by GFP from exogenous mRNA is maximal around 1 x physiological concentration. Also Lohka said that slight dilution disrupts key biological process like mitosis and DNA replication.

(Changes to degree of crowding have shown to impact wide-spread effect within the cell.)

- For instance altering cytoplasmic crowding by changing ribosome concentration strongly affect phase separation. Inhibiting mTORC1 gene which means reduces ribosome levels decreased diffusion of 40 nm GEM probe particle and shrank biomolecular condensates by up to 80% in vivo and in vitro

- Furthermore, crowding directly regulates cytoskeletal dynamics. Researchers acutely manipulated cytoplasmic concentration by applying osmotic pressure using 1.5 M sorbitol to fission yeast, and found that the rates of both microtubule polymerization and depolymerization scale linearly with cytoplasmic concentration.

- This biophysical consequences of crowding also extended to aging and senescence.
Budding yeast forced into excessive growth during G1 arrest by drug addition. the cells failed to scale macromolecule biosynthesis with volume increase and this was sufficient to reduce the average life span. Also when IMR90 fibroblasts are driven into dormancy by G1 arrest using drug, this is accompanied by cytoplasmic dilution detected by reducing mobility of GEM probe.

- Finally, changes in crowding have been implicated in differentiation and stem cell fate
By changing mechanical rigidity of material on cells or using external osmotic pressure (e.g., PEG 300) to change the water content of mesenchymal stem cells (mMSCs), researchers were able to manipulate intracellular crowding and cell stiffness.
The results showed that changing cell volume through water efflux/influx was sufficient to alter the cell's differentiation pathway; increasing molecular crowding via osmotic compression enhanced osteogenic differentiation, while decreasing crowding via hypotonic conditions enhanced adipogenic differentiation.

(Despite its dynamic behavior and functional appearance, the cytoplasm is so densely packed that it can undergo a glass-like transition under certain metabolically inactivated conditions.)

- In E. coli, Parry reported that when cellular metabolism was inhibited, either by the oxidative phosphorylation inhibitor 2,4-dinitrophenol (DNP) or by glucose starvation, the mobility of intracellular particles was drastically reduced, indicating a transition of the cytoplasm from a liquid-like to a solid-like state.

- Ebata used feedback-tracking Active Microrheology (AMR) to measure the complex shear modulus (G) of HeLa cells. They specifically compared untreated cells to those subjected to ATP depletion for 7 hours (using 2-deoxyglucose and NaN3). The mechanical properties were measured using probes.
After ATP depletion, the storage modulus of the HeLa cells showed a significant increase at low frequencies compared to untreated cells. This finding is consistent with the cell cytoplasm solidifying and displaying a glass-like rheological response under severe energy deprivation. Untreated cells, in contrast, maintained lower elasticity, suggesting they actively resist this solidification

(dormancy)
Microorganisms are live in a changing condition, but they often face extremely challenging environmental shifts, such as extreme nutrient deprivation or desiccation. To achieve long-term survival under these harsh conditions, cells activate a crucial strategy known as dormancy or quiescence.
Dormancy is fundamentally defined as a reversible cell cycle arrest induced by the lack of growth stimuli. In this state, cells dramatically slow their metabolism, allowing them to survive using minimal energy. A key point is that dormancy is reversible state — when nutrients become available again, cells can wake up and start growing once more.

(gradual response)
Research by Pluskal showed that cells which abruptly stop growing under extreme glucose deprivation have a shorter lifespan, whereas cells that are gradually adapted to low-glucose conditions before complete glucose starvation can survive for much longer periods.
In their experiment, instead of abruptly shifting cells from a glucose-rich environment to 0\% glucose, they grew cells in medium containing low concentration of glucose ranging from 0.02\% to 0.08\%. As the cells consumed the glucose during growth, they gradually ceased proliferation.The survival of these adapted cells, shown by the green line in their data, was significantly higher under complete glucose starvation compared to cells that experienced a sudden shift.

具体的課題
(Although genes and environmental conditions affecting starvation survival have been identified and numerous mutations and physiological alternations in response to starvation have been discovered, some of the fundamental questions remained unanswered. Specifically, What causes metabolically inactive or energy-depleted cells to irreversibly lose their viability?
how does macromolecular crowding behave in a low-energy state, where growth is arrested but not entirely suppressed?)

(死ぬ細胞と生きる細胞における物理的な状態の違い、どう言った細胞が生きて、どういった細胞が死ぬのかの違いを見極めることがむずかしい。)


個別背景（Technical purpose）
low-glucose accliminated S.pombe profoundly endure in subsequent carbon-free medium
cytoplasmic solidificationとcytoplasmic freezing
死ぬ細胞と生きる細胞における物理的な状態の違い、どう言った細胞が生きて、どういった細胞が死ぬのかの違いを見極めることがむずかしい。

To address these issue, we imaged indivisual starving S.pome with quantitative microscopy, called QPI. QPI is a label-free optical technique for precisely quantifying the physical properties of living cells such as mass concentration and volume. When light passes through a cell, it experiences a phase shift. which is proportional to thickness of the sample and its average refractive index (RI)
The refractive index is directly correlated with the concentration of biomolecules within the cell. This is because the refractive indices of major cellular components like proteins, lipids, and nucleic acids are similar. By measuring the phase shift, QPI provides a non-invasive way to map the mass density.

この論文は、上記具体的課題に対し、どのような解決策や新規知見をもたらしたか
our data showed that the low glucose acclimated cells had an increased ability to resume division after glucose recovery. In addition, the density of intracellular substances was increased in acclimated cells. The changes in cytoplasmic density observed in this study under low concentrations of glucose may be favorable for cell survival and re-growth through cytoplasmic crowding.




Results
acute
osmotic induced endure
... 

