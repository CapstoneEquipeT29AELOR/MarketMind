# Standalone experiments

Existing: generate_signals.py, preserved without code changes. It downloads
NVDA prices, computes 20/50-day moving averages, and plots crossover markers.
It runs immediately when executed or imported, so use it as a script until
you deliberately refactor it.

Add small prototypes and research comparisons here. Move stable application
functionality to backend/ or ml/. No broker execution is implemented by this
plotting script. See requirements/research.txt for plotting dependencies.
