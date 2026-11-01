# Python dependencies

| File | Purpose |
| --- | --- |
| required_libraries.txt | The original short ML dependency list, unchanged |
| research.txt | Includes that list plus matplotlib and jupyter for the existing research code |
| environment-original.txt | The original pinned requirements.txt, unchanged, retained as an environment snapshot |
| ../requirements.txt | Convenient root entrypoint including required_libraries.txt |

The two supplied lists differ: the pinned environment snapshot omits some
imports required by the ML scripts, including xgboost, scikit-learn, joblib,
transformers, and torch. The short list is unpinned. Neither list was
dependency-resolved or installed during this organization, so this package
does not claim a tested reproducible environment.

When you add backend code, create backend.txt here with the packages that
code actually uses. Add dev.txt when you choose testing/lint tools. Frontend
dependencies belong in frontend/package.json after framework setup.
Once the environment works, record tested versions and Python version.
