# Workforce Planning Dashboard

This folder contains exported screenshots of the Power BI dashboard used to communicate workforce planning insights to senior management.

## Dashboard Overview

**Title:** Workforce Planning & Staffing Risk Overview

**Purpose:** To provide executive-level visibility into staffing gaps, vacancy risk, succession exposure, and hiring priorities across the organisation.

**Intended Audience:** Directors, HR leadership, and strategic planning teams

## Files in This Folder

| File | Description |
|------|-------------|
| `workforce_planning_dashboard_YYYY-MM-DD.png` | Main dashboard screenshot in 1920×1080 PNG format (high resolution for portfolio) |

## Dashboard Components

1. **Executive KPI Row**
   - Total headcount (filled positions)
   - Overall vacancy rate (%)
   - High-risk roles count
   - % workforce aged 55+

2. **Vacancy Rate by Department**
   - Bar chart with colour-coded risk (Red >25%, Amber 10–25%, Green <10%)
   - Sorted by highest vacancy pressure

3. **Staffing Risk Heatmap**
   - Department × Grade matrix
   - Identifies risk concentration across roles and departments
   - Colour coded: Red (High), Amber (Medium), Green (Low)

4. **Retirement Exposure by Department**
   - 100% stacked bar chart
   - Shows % workforce <55 (green) vs ≥55 (red)
   - Highlights succession risk by department

5. **High-Risk Roles Summary Table**
   - Lists priority hiring targets
   - Sorted by combined staffing and succession risk
   - Includes vacancy rates and hiring recommendations

## How the Dashboard Supports Decision-Making

**Business Questions Answered:**
- Where are current staffing gaps across the organisation?
- Which departments and grades are at highest staffing risk?
- How exposed is the organisation to retirement and succession risk?
- Which roles should be prioritised for hiring in the short to medium term?

**Key Insights from the Dashboard:**
- [Staffing risk concentration in specific departments/grades]
- [Retirement exposure patterns across the organisation]
- [High-priority hiring focuses]

*Insights to be populated after dashboard is reviewed by stakeholders.*

## Technical Details

- **Data Source:** `workforce_planning_master.csv`
- **Tool:** Microsoft Power BI Desktop
- **Dashboard Page Size:** 16:9 (1920 × 1080 pixels)
- **Export Format:** PNG (high resolution for portfolio/print)

## Next Steps

1. Build the dashboard in Power BI Desktop using the implementation guide
2. Validate metrics and thresholds with HR and business stakeholders
3. Export the dashboard as a high-resolution PNG (1920 × 1080)
4. Add screenshot to this folder with a filename: `workforce_planning_dashboard_YYYY-MM-DD.png`
5. Update the "Key Insights" section above with findings
6. Commit and push to GitHub

---

**Last Updated:** February 2026
