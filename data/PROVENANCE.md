# Data provenance

Manually transcribed numeric entries from Tables B1–B3 of Humpage et al. (2024),
Greenhouse gas column observations from a portable spectrometer in Uganda,
Atmospheric Measurement Techniques 17, 5679–5707.
https://doi.org/10.5194/amt-17-5679-2024
Source article: https://amt.copernicus.org/articles/17/5679/2024/
Article distributed under Creative Commons Attribution 4.0. Attribution retained.
These are published comparison summary statistics, not raw satellite soundings.
Difference sign is satellite minus EM27/SUN, following the paper’s comparisons:
the text states that OCO-2 is lower than EM27/SUN by 1.20 ppm, matching -1.20 in B1.
CO2 units ppm; CH4 and CO units ppb. SD is spread across matched daily differences,
not a confidence interval. Wider-radius rows are nested samples, not independent trials.

OCO-3 500 and 600 km rows are retained exactly as printed in Table B1, including
values matching OCO-2; this project does not silently amend possibly surprising
published entries. Raw paired observations would be needed to independently verify them.

Collocation code is tested on explicitly constructed coordinates/times. It has not
been used to claim new satellite-ground validation. It computes geometric/time
matches only; satellite quality flags, priors and averaging-kernel harmonisation
must be added before scientific validation of real retrieval files.

## Time matching in the source paper

The source study uses ±2 h around TROPOMI overpasses for CH4/CO and retains
days with at least 10 good soundings. For OCO-2/OCO-3 CO2, it compares whole-day
ground medians because overpass timing varies. The generic collocator's ±2 h
default is a testable building block, not a literal implementation of every
gas-specific decision in the paper.
