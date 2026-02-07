# WORKFORCE PLANNING MASTER DATASET - DOCUMENTATION

**Date**: February 7, 2026  
**Purpose**: Unified analytical dataset for workforce planning, vacancy analysis, and succession risk assessment  
**Status**: ✅ Production Ready

---

## OVERVIEW

The **workforce_planning_master.csv** dataset combines:
- **positions.csv**: HR strategic planning (required headcount, priorities, risks)
- **employees.csv** (aggregated): Actual workforce reality (age, retirement risk, staffing levels)

Result: Executive-ready analytical dataset supporting management decision-making on hiring, succession planning, and departmental staffing strategies.

---

## JOIN METHODOLOGY

### Source Data
1. **positions.csv** (18 rows)
   - HR-planned positions by department + grade
   - Represents target staffing architecture
   - Includes hard-to-fill role indicators and succession risk flags

2. **employees.csv** (1,200 records → 1,102 active)
   - Aggregated by department + grade
   - Actual current staffing levels
   - Age demographics and retirement risk calculations

### Join Logic
```
LEFT JOIN(positions, employees_aggregated) ON (department, grade)

Result:
- All 18 planned positions preserved
- Matched with actual workforce metrics
- Positions with zero employees filled with zeros
```

---

## SCHEMA (19 COLUMNS)

### Organizational Dimensions
| Column | Definition | Source |
|--------|-----------|--------|
| **department** | Org unit (Economics & Policy, Energy & Climate, etc.) | positions.csv |
| **role** | Job title (Analyst, Senior Analyst, Manager) | positions.csv |
| **grade** | Grade level  | positions.csv |
| **role_family** | Functional grouping (Policy, Technical, Corporate, Digital) | positions.csv |

### Planning & Staffing
| Column | Definition | Source |
|--------|-----------|--------|
| **required_headcount** | HR target positions | positions.csv |
| **filled_positions** | Current staffing level | positions.csv |
| **vacancy_count** | Open roles (required - filled) | positions.csv |
| **vacancy_rate** | Vacancy % (derived) | Calculated |

### Workforce Demographics
| Column | Definition | Source |
|--------|-----------|--------|
| **avg_age** | Average age of employees in role | employees aggregation |
| **age_stdev** | Standard deviation of ages | employees aggregation |
| **retirement_risk_count** | Number of employees age 55+ | employees aggregation |
| **retirement_risk_pct** | Percentage of staff age 55+ | employees aggregation |

### Strategic Flags
| Column | Definition | Source |
|--------|-----------|--------|
| **critical_skill** | Is this a hard-to-fill role? (True/False) | positions.csv |
| **hiring_priority** | Urgency (High/Medium/Low) | positions.csv |
| **succession_risk** | Risk of key person departure (High/Medium/Low) | positions.csv |

### Derived Risk Indicators (NEW)
| Column | Definition | Logic |
|--------|-----------|-------|
| **staffing_risk_flag** | Staffing urgency | High: vacancy > 25% OR succession_risk = High<br/>Medium: 10-25% vacancy<br/>Low: otherwise |
| **retirement_pressure_flag** | Retirement urgency | High: 55+ staff ≥ 20%<br/>Medium: 10-20%<br/>Low: < 10% |
| **combined_risk_score** | Overall priority (2-6) | Sum of (staffing score 1-3 + retirement score 1-3) |

---

## KEY FINDINGS

### 1. Overall Staffing Position
- **Required**: 415 positions
- **Filled**: 360 employees
- **Vacancies**: 55 open roles
- **Vacancy Rate**: 13.3% (realistic for international organizations)

### 2. Staffing Risk Distribution
- **High Risk**: 9 positions (50%) - immediate action needed
- **Medium Risk**: 9 positions (50%) - monitor and plan
- **Low Risk**: 0 positions (0%) - stable

### 3. Retirement Pressure Distribution
- **High Pressure**: 5 positions (27.8%) - succession planning urgent
  - All Manager roles: 29.7% avg staff age 55+
  - Energy & Climate Manager: 36% retirement risk
- **Medium Pressure**: 1 position (5.6%)
- **Low Pressure**: 12 positions (66.7%) - stable demographics

### 4. Critical Roles Assessment
- **Total Critical Positions**: 7 (39% of all roles)
- **Critical with Vacancies**: 7 (100% have open positions)
- **Avg Vacancy Rate (Critical)**: 7.7%
- **Critical Roles at High Risk**: 7 (100%)
- **🚨 Alert**: All critical roles flagged for high staffing attention

### 5. Department Vacancy Ranking (Hiring Focus)
1. **Communications**: 15.1% vacancy (11 of 73)
2. **Energy & Climate**: 13.8% vacancy (9 of 65)
3. **HR & Operations**: 13.8% vacancy (8 of 58)
4. **Economics & Policy**: 13.7% vacancy (10 of 73)
5. **IT & Digital**: 12.2% vacancy (9 of 74)
6. **Data & Analytics**: 11.1% vacancy (8 of 72)

### 6. Staffing by Grade
| Grade | Required | Filled | Vacancy % | Avg Age | Retirement % |
|-------|----------|--------|-----------|---------|--------------|
| Analyst | 145 | 118 | 18.6% | 33.8 | 0.0% |
| Senior Analyst | 112 | 97 | 13.4% | 42.3 | 0.0% |
| Manager | 158 | 145 | 8.2% | 50.2 | **29.7%** |

**Key Insight**: Managers represent critical succession risk (30% nearing retirement age).

---

## EXECUTIVE INSIGHTS FOR DECISION-MAKING

### 🎯 Immediate Priorities (High Staffing Risk)

**All 6 Manager roles** at combined high risk (succession + staffing):
1. **Communications Manager** - 35 required, 31 filled (11.4% vacancy, 35% retirement risk)
2. **HR & Operations Manager** - 17 required, 15 filled (11.8% vacancy, 27% retirement risk)
3. **Data & Analytics Manager** - 25 required, 24 filled (4% vacancy, 35% retirement risk)
4. **IT & Digital Manager** - 28 required, 27 filled (3.6% vacancy, 28% retirement risk)
5. **Energy & Climate Manager** - 26 required, 24 filled (7.7% vacancy, 36% retirement risk) ← **Highest retirement risk**
6. **Economics & Policy Manager** - 27 required, 24 filled (11.1% vacancy, 17% retirement risk)

**Action**: Develop succession pipelines NOW. All are key institutional knowledge holders.

### 📊 High-Priority Hiring Focus

**9 High-Priority Positions** (100% of critical skills roles):
- Average vacancy: 8.9%
- All 7 critical-skill roles + 2 strategic manager roles
- Recommendation: Accelerate recruitment, increase salary bands if needed

### ⚠️ Non-Critical But Understaffed

**Analyst Roles** show highest vacancy rate (18.6% avg):
- HR & Operations Analyst: 12% vacancy (critical skill role)
- Data & Analytics Analyst: 21.4% vacancy
- Communication Analyst: 21.1% vacancy
- IT & Digital Analyst: 19.4% vacancy

Recommendation: Increase junior hiring, consider training/upskilling current staff.

### 💡 Departments Health Check

**Healthiest**: Data & Analytics (11.1% vacancy) - good talent retention
**Stretched**: Communications (15.1% vacancy) - may need capacity review

---

## VALIDATION & QUALITY

✅ **All logical constraints satisfied**:
- filled_positions ≤ required_headcount (100%)
- vacancy_count = required - filled (100% match)
- No negative values (0 violations)
- No data integrity issues

✅ **Realism checks**:
- Vacancy rates 11-15% → realistic for OECD-style org
- Manager retirement risk ~30% → realistic demographic profile
- Grade-level staffing proportions → align with employee distribution

---

## ANALYTICAL CAPABILITIES ENABLED

This dataset now supports:

### For HR Analytics Teams
- **Vacancy forecasting** by department, grade, role
- **Succession planning** with clear high-risk roles
- **Recruitment ROI** by priority level
- **Headcount trending** over time

### For Management Dashboards
- Real-time vacancy rate tracking
- Succession risk heatmaps
- Department staffing health
- Critical role alert system

### For Strategic Planning
- Workforce capacity scenarios
- Hiring budget allocation
- Career development pathways
- Risk mitigation strategies

---

## HOW TO USE THIS DATASET

### In Tableau / Power BI
```
Dimensions: department, grade, role_family, hiring_priority, staffing_risk_flag
Measures: required_headcount, vacancy_count, vacancy_rate, avg_age, retirement_risk_pct
Colored by: staffing_risk_flag, retirement_pressure_flag
Sorted by: combined_risk_score (descending)
```

### In SQL / Python Analytics
```sql
SELECT department, 
       SUM(vacancy_count) as dept_vacancies,
       AVG(vacancy_rate) as avg_vacancy_pct,
       SUM(retirement_risk_count) as at_risk_staff
FROM workforce_planning_master
WHERE staffing_risk_flag = 'High'
GROUP BY department
ORDER BY dept_vacancies DESC
```

### Interview Scenarios
**Q: Where should we hire first?**  
A: "High-priority critical skill roles (9 positions, 8.9% avg vacancy) - all flagged for urgent attention."

**Q: What's our succession risk?**  
A: "All 6 Manager roles have 28-36% staff age 55+. Immediate succession pipeline development recommended."

**Q: How does departmental staffing compare?**  
A: "Communications most stretched (15.1%). Data & Analytics most stable (11.1%). Overall 13.3% vacancy realistic."

---

## FILES GENERATED

| File | Purpose | Size |
|------|---------|------|
| **workforce_planning_master.csv** | Main analytical dataset (18 rows, 19 columns) | 2.1 KB |
| **create_workforce_planning_master.py** | Python script (fully reproducible) | 16.4 KB |
| **WORKFORCE_PLANNING_MASTER_DOCUMENTATION.md** | This document | - |

---

## NEXT STEPS

1. **Load into BI tool** (Tableau, Power BI, Looker)
2. **Build executive dashboard** on staffing_risk_flag, retirement_pressure_flag
3. **Weekly monitoring** of critical roles
4. **Quarterly reviews** of vacancy_rate trends by department
5. **Succession planning** for all High retirement_pressure roles

---

**Status**: ✅ PRODUCTION READY - Suitable for OECD senior management review  
**Audience**: HR Directors, Department Heads, CFO/HR Planning Committee  
**Last Updated**: February 7, 2026  
**Data Quality**: ✅ All validations passed
