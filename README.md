# Workforce Planning & Staffing Risk Analytics

## Business Context
International organisations rely on effective workforce planning to ensure continuity of operations, maintain institutional knowledge, and deliver strategic objectives under budgetary and staffing constraints.

This project simulates a realistic OECD-style organisational environment and demonstrates how workforce data can be transformed into actionable insights for senior management and HR leadership.

The analysis focuses on staffing capacity, vacancy exposure, and succession risk across departments and grades.

---

## Management Questions
This project addresses the following decision-oriented questions:

- Where are current staffing gaps across the organisation?
- Which departments and grades are at highest staffing risk?
- How exposed is the organisation to retirement and succession risk?
- Which roles should be prioritised for hiring in the short to medium term?

---

## Data & Methodology

### Data Sources
All data used in this project is **fully synthetic**, created to simulate a realistic international organisation workforce while respecting data confidentiality and ethical standards.

Datasets:
- `employees.csv`: Individual-level workforce data (headcount, age, contract type, tenure)
- `positions.csv`: Role-level staffing requirements, critical skills, and succession risk
- `recruitment_pipeline.csv`: Recruitment capacity and time-to-fill metrics
- `workforce_planning_master.csv`: Analytical dataset joining employees and positions data

### Methodology
- Employee data was aggregated by department and grade to calculate filled positions, retirement exposure, and average age.
- Staffing requirements were compared against filled positions to compute vacancy counts and vacancy rates.
- Risk flags were derived using clear, management-friendly thresholds for vacancy and succession risk.
- All metrics were designed to support executive decision-making rather than exploratory analysis.

---

## Key Insights

### 1. Staffing risk is concentrated in technical and analytical roles
Several departments show elevated vacancy rates in Analyst and Senior Analyst grades, particularly in roles identified as critical skills.

### 2. Retirement exposure creates medium-term succession risk
Manager and Director grades show a higher proportion of staff aged 55+, indicating potential loss of institutional knowledge within the next 3–5 years.

### 3. Recruitment capacity does not fully offset vacancy pressure
Roles with long time-to-fill periods also tend to have limited recruitment pipelines, increasing operational risk.

### 4. Staffing risk varies significantly by department
While some departments remain stable, others combine high vacancy rates with high succession risk, requiring targeted intervention rather than organisation-wide measures.

---

## Recommendations

Based on the analysis, the following actions are recommended:

- Prioritise hiring for critical roles with both high vacancy and high succession risk.
- Initiate early recruitment or talent pipeline development for roles with long time-to-fill.
- Strengthen succession planning for senior grades in departments with elevated retirement exposure.
- Use vacancy and risk dashboards as part of regular management reporting cycles.

---

## Dashboard Design & Implementation

### Visualisation Overview
The analysis is supported by an executive-level Power BI dashboard titled **"Workforce Planning & Staffing Risk Overview"** designed specifically for director-level decision-making.

**Dashboard Components:**
1. **Executive KPI Overview** – Four key metrics at a glance:
   - Total filled headcount across the organisation
   - Overall vacancy rate (% of required positions unfilled)
   - Count of roles flagged as High staffing risk
   - % of workforce aged 55+ (retirement exposure indicator)

2. **Vacancy Rate by Department** – Bar chart with colour-coded risk levels (Red: >25%, Amber: 10–25%, Green: <10%) to identify departments under critical staffing pressure

3. **Staffing Risk Heatmap** – Department-by-grade matrix showing risk concentration across the organisation (High/Medium/Low flags)

4. **Retirement & Succession Risk** – Stacked bar chart displaying workforce age distribution by department to quantify medium-term succession exposure

5. **High-Risk Roles Summary Table** – Filterable table of priority hiring targets, sorted by combined staffing and succession risk, with vacancy rates and hiring recommendations

### Build Instructions
Complete step-by-step Power BI implementation guide, including:
- All required DAX measures (copy-paste ready)
- Visual-by-visual formatting and conditional colour rules
- Recommended canvas layout (16:9 dashboard design)
- Export guidance for clean GitHub portfolio screenshots

👉 **See [POWER_BI_BUILD_GUIDE.md](documentation/POWER_BI_BUILD_GUIDE.md) for full implementation details.**

---

## Portfolio Visualisations

Dashboard screenshots are included in the `/dashboard` folder.

---

## Tools Used
- Python (pandas, numpy)
- SQL (data aggregation and KPI logic)
- Power BI (executive dashboard)
- GitHub & VS Code (version control and documentation)

---

## Notes
This project is designed to reflect real-world workforce planning practices in international organisations and is intended for portfolio and demonstration purposes only.
