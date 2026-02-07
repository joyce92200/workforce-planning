# Workforce Planning — Synthetic Dataset

This repository contains synthetic, portfolio-safe workforce datasets and scripts for an OECD-style workforce analytics project.

Contents:
- `employees.csv` — synthetic individual-level employee records
- `positions.csv` — enhanced role-level staffing plan
- `recruitment_pipeline.csv` — recruitment metrics
- `generate_workforce_data.py` — script to generate synthetic data
- `enhance_positions.py` — script that enhances `positions.csv` for planning
- `create_workforce_planning_master.py` — joins employees and positions into an analytical master dataset
- `workforce_planning_master.csv` — final analytical dataset (derived)
- Documentation files: `POSITIONS_ENHANCEMENT_SUMMARY.md`, `POSITIONS_QUICK_REFERENCE.md`, `WORKFORCE_PLANNING_MASTER_DOCUMENTATION.md`

Usage
```
# Install dependencies
python -m pip install pandas numpy faker

# Regenerate datasets
python generate_workforce_data.py
python enhance_positions.py
python create_workforce_planning_master.py

# Open CSV files or import into Power BI / Tableau
```

Notes
- All data is fully synthetic and safe for portfolio/demo use.
- This repo is connected to https://github.com/joyce92200/workforce-planning.git

Maintainer: joyce92200 (jowork2024@gmail.com)
