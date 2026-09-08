<!-- genre: thesis | layer: sentence | section: introduction | source: 1.Introduction.tex の 48–163行目 Stage 3/4: センテンスレベル First Draft（英語）
     2026-09-08 に .tex から切り出した。Markdown が .tex の中にあってビルドが壊れていたため。
     中身は一字も変えていない。 -->

**この英語ドラフトは、1.Introduction.tex の本文（旧247行目以降）とは別物。**
どちらが新しいか未確認。採用するほうを決めて .tex に移す。

## Stage 3 / 4: センテンスレベル First Draft（英語）
 
---
 
### Section 1: General Background — The history-dependence of cell survival
 
**Para A — Glucose as the primary energy source and starvation as a universal challenge**
 
Glucose is the primary carbon and energy source for most living organisms, from bacteria to mammalian cells.
In natural environments, glucose availability fluctuates dramatically over time, subjecting cells to repeated cycles of feast and famine.
The ability to survive and recover from glucose starvation is therefore a fundamental determinant of evolutionary fitness in microorganisms and a critical process in physiological contexts ranging from microbial ecology to metabolic disease and cancer [Broach 2012, Genetics; Vander Heiden et al. 2009, Science].
Understanding how cells manage to survive nutrient deprivation — and how they resume growth upon nutrient restoration — is a central question in cell biology.
 
**Para B — Phenotypic heterogeneity: not all cells respond equally**
 
Even within a genetically identical population exposed to identical starvation conditions, individual cells display remarkably diverse outcomes: some die rapidly, while others survive for extended periods and eventually resume proliferation [Kussell & Leibler 2005, Science; Levy et al. 2012, Nature].
This phenotypic heterogeneity is not simply experimental noise; it reflects genuine cell-to-cell variability in the physiological state at the time of starvation onset.
Such variability has been documented across diverse organisms — bacteria, budding yeast, fission yeast, and mammalian cells — indicating that it is an evolutionarily conserved feature of cellular responses to environmental stress.
A key question is therefore what determines whether an individual cell will survive or perish under starvation.
 
**Para C — History-dependent responses: the past shapes the future**
 
A growing body of evidence indicates that the survival outcome of individual cells is not solely determined by their current environment, but is strongly influenced by their prior history — the sequence and intensity of stress exposures they have experienced [Acar et al. 2008, Nature Genetics; Bhattacharyya et al. 2020, Curr Biol].
Cells that have previously encountered starvation often display enhanced resistance to subsequent starvation challenges, a phenomenon akin to "cellular memory" or stress priming [Mitchell et al. 2009, Nature; Guan et al. 2023].
Conversely, cells that have been maintained under rich nutrient conditions may be more vulnerable to sudden starvation.
This history-dependence implies that cells carry some form of physical or molecular memory of past events that persists and influences future behavior.
 
**Para D — The central question: what is the physical substrate of this memory?**
 
The mechanisms underlying history-dependent survival remain poorly understood.
Proposed molecular bases include epigenetic modifications, persistent changes in protein complex composition, and alterations in the physical state of the cytoplasm [Bhattacharyya et al. 2020].
Among these, the physical state of the cytoplasm — specifically, its macromolecular crowding and fluidity — is an attractive candidate: it is a global, cell-wide property that reflects the cumulative physiological state of the cell and can, in principle, persist across timescales relevant to history-dependent responses.
This thesis addresses the hypothesis that history-dependent differences in cytoplasmic physical state underlie the heterogeneous survival outcomes of individual cells exposed to glucose starvation.
 
---
 
### Section 2: Technical Background — Crowding, fluidity, and dormancy
 
**Para E — Dormancy as a survival strategy**
 
The most prominent survival strategy adopted by cells under severe glucose starvation is dormancy — a reversible state of profoundly reduced metabolic activity in which cells cease proliferation but maintain viability [Gray et al. 2004, Microbiol Mol Biol Rev; De Virgilio 2012, FEMS Microbiol Rev].
In the budding yeast *Saccharomyces cerevisiae* and the fission yeast *Schizosaccharomyces pombe*, glucose depletion triggers entry into a quiescent (G0-like) state characterized by cell cycle arrest, downregulation of biosynthetic activities, and dramatic remodeling of the cytoplasm.
Dormant cells can remain viable for weeks to months and resume growth rapidly upon glucose restoration, demonstrating the reversibility of this state.
Critically, the probability of successfully entering and maintaining dormancy, and of exiting it upon nutrient readdition, varies substantially among individual cells in a population — and depends on their starvation history.
 
**Para F — Molecular crowding: the physical context of the cytoplasm**
 
The cytoplasm is not a dilute aqueous solution; it is a densely crowded environment containing 20–40% macromolecules by volume, with total macromolecular concentrations estimated at 300–400 g/L in *Escherichia coli* and comparable values in eukaryotic cells [Zimmerman & Trach 1991, J Mol Biol; Milo & Phillips 2015].
This "molecular crowding" has profound consequences for virtually all intracellular biochemical processes.
Through excluded volume effects, crowding increases the effective concentration of macromolecules, shifts protein folding equilibria toward more compact states, accelerates protein–protein association, and alters the thermodynamics of complex formation [Minton 2001, J Biol Chem; Ellis 2001, Trends Biochem Sci].
Moreover, changes in intracellular crowding — for instance, due to cell volume changes under osmotic stress or nutrient deprivation — rapidly modulate these processes, rendering crowding a dynamic regulator of cell physiology [Delarue et al. 2018, Cell].
 
**Para G — Cytoplasmic glass transition: from fluid to solid-like state during dormancy entry**
 
A pivotal discovery linking cytoplasmic physical state to dormancy came from Munder et al. (2016), who demonstrated that glucose starvation in *S. cerevisiae* drives the cytoplasm from a fluid-like to a solid-like (glass-like) state [Munder et al. 2016, eLife].
This transition is triggered by intracellular pH acidification that occurs upon glucose removal, and results in a dramatic reduction of macromolecular mobility throughout the cytoplasm.
Concurrent work by Joyner et al. (2016) showed that glucose starvation in *S. cerevisiae* causes a global reduction in cytoplasmic diffusivity that is reversible upon glucose readdition [Joyner et al. 2016, eLife].
The solidification of the cytoplasm has been proposed to serve a protective function during dormancy: by reducing molecular mobility, it may limit aberrant biochemical reactions, prevent protein aggregation, and minimize energy expenditure [Franzmann et al. 2018, Science].
Whether this cytoplasmic glass transition and its protective function are history-dependent — that is, whether cells with different starvation histories undergo different extents of cytoplasmic solidification — remains unknown.
 
**Para H — Liquid–liquid phase separation and biomolecular condensates under stress**
 
In parallel with the global cytoplasmic solidification, glucose starvation induces the formation of numerous discrete biomolecular condensates — membraneless organelles formed through liquid–liquid phase separation (LLPS) [Hyman et al. 2014, Annu Rev Cell Dev Biol].
These include stress granules, P-bodies, and various metabolic enzyme assemblies, such as the filaments formed by glutamine synthetase and other metabolic enzymes under advanced starvation [Petrovska et al. 2014, eLife; Buchan 2014, RNA Biol].
Molecular crowding is a key driver of LLPS: by increasing the effective concentration of phase-separating proteins and nucleic acids, crowding shifts the phase boundary and promotes condensate formation [Delarue et al. 2018, Cell; Alfano et al. 2024, Chem Rev].
Condensates, once formed, can mature over time from fluid-like droplets to gel-like or solid-like aggregates — a process termed aging — and this maturation is accelerated by crowding.
Whether the condensate landscape of a cell is shaped by its starvation history represents an open and biologically important question.
 
**Para I — Intracellular fluidity and passive microrheology**
 
The term "intracellular fluidity" describes the mechanical properties of the cytoplasm as experienced by macromolecular probes undergoing thermal motion — a property that is distinct from bulk viscosity and reflects the complex viscoelastic nature of the crowded cytoplasm [Höfling & Franosch 2013, Rep Prog Phys].
In a purely viscous (Newtonian) fluid, the mean square displacement (MSD) of a tracer particle increases linearly with time; in a viscoelastic cytoplasm, tracers typically exhibit subdiffusive (anomalous) motion with MSD ∝ t^α (α < 1), reflecting the elastic memory of the surrounding medium [Weiss et al. 2004, Biophys J].
As the cytoplasm transitions toward a gel-like or glass-like state under starvation, α decreases progressively toward zero, reflecting an increasingly arrested cytoplasm.
Passive microrheology — tracking the Brownian motion of inert probe particles and extracting rheological parameters via the generalized Stokes-Einstein relation — thus provides a sensitive and quantitative readout of the cytoplasmic physical state.
The development of genetically encoded multimeric nanoparticles (GEMs) — self-assembling ~40 nm fluorescent nanoparticles that can be expressed endogenously in living cells — has enabled non-perturbative passive microrheology in vivo [Delarue et al. 2018, Cell], opening the door to systematic characterization of intracellular fluidity changes during starvation and dormancy.
 
---
 
### Section 3: Specific Problem
 
**Para J — Technical limitations of existing approaches**
 
Despite the importance of cytoplasmic physical state, its quantitative measurement at the single-cell level in living cells during starvation has been technically challenging.
Fluorescence recovery after photobleaching (FRAP) and fluorescence correlation spectroscopy (FCS) provide diffusion measurements but typically require fluorescent labeling of specific endogenous proteins, making it difficult to isolate crowding-dependent effects from changes in specific protein–protein interactions [Lippincott-Schwartz et al. 2001, Science].
In-cell NMR spectroscopy offers exquisite molecular resolution but requires ensemble averaging over large cell populations and is not compatible with time-lapse measurements of individual cells [Theillet et al. 2016, Nature].
Moreover, most existing studies have focused on end-point measurements at a single starvation time point, rather than tracking how the cytoplasmic physical state evolves as a function of starvation history in individual cells.
 
**Para K — The unresolved link between physical state, history, and survival**
 
A quantitative, single-cell understanding of how starvation history shapes the cytoplasmic physical state — and how this physical state relates to the probability of survival — has not been established.
Specifically, it is unknown whether cells that differ in their starvation history (e.g., cells that have experienced one versus multiple starvation cycles, or gradual versus abrupt starvation) develop systematically different crowding or fluidity profiles.
Furthermore, the extent to which individual variation in cytoplasmic physical state within an isogenic population predicts single-cell survival outcomes under subsequent starvation challenges has not been directly tested.
Answering these questions requires new approaches that combine high-throughput single-cell measurement of cytoplasmic physical properties with survival tracking — capabilities that are now within reach.
 
---
 
### Section 4: This Thesis
 
**Para L — Approach: QPM + GEM microrheology in S. pombe**
 
In this thesis, we address these questions using *Schizosaccharomyces pombe* — an established model organism for cell cycle biology and stress responses — as a tractable system to study the physical basis of history-dependent survival under glucose starvation.
We combine two complementary, non-perturbative approaches for single-cell quantification of cytoplasmic physical state.
First, quantitative phase microscopy (QPM) is used to measure intracellular dry mass density — an optical proxy for macromolecular crowding — in individual living cells with high temporal resolution and without exogenous labels [Mir et al. 2014, Proc Natl Acad Sci; Park et al. 2018].
Second, genetically encoded multimeric nanoparticle (GEM) probes are used to perform passive microrheology measurements of intracellular fluidity in individual cells, enabling quantification of the cytoplasmic glass transition during starvation [Delarue et al. 2018, Cell].
By applying these approaches to cells with defined starvation histories, we systematically characterize how past starvation experience shapes the cytoplasmic physical state and how this state relates to future survival probability.
 
**Para M — Thesis structure**
 
The thesis is organized as follows.
Chapter 2 describes the QPM-based characterization of intracellular crowding dynamics during glucose starvation in *S. pombe*, establishing how crowding changes as a function of starvation duration and history.
Chapter 3 presents GEM-based passive microrheology measurements of intracellular fluidity, examining the fluid-to-solid-like cytoplasmic transition during dormancy entry and its dependence on starvation history.
Chapter 4 integrates these physical measurements with survival assays to establish quantitative relationships between cytoplasmic physical state and history-dependent survival outcomes.
Chapter 5 provides a general discussion synthesizing these findings in the broader context of cellular memory, dormancy, and the biophysics of the crowded cytoplasm, and outlines key open questions for future investigation.
 
---
 
