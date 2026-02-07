# POSITIONS.CSV ENHANCEMENT - QUICK REFERENCE

## What Changed?

**Old positions.csv**: 4 columns, basic staffing numbers  
**New positions.csv**: 11 columns, workforce planning ready

---

## New Columns Added (7 new fields)

| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| `grade` | Analyst \| Senior Analyst \| Manager | Normalize role levels | "Analyst" |
| `role_family` | Policy \| Technical \| Corporate \| Digital | Group by function | "Technical" |
| `filled_positions` | Integer | Current headcount | 24 |
| `vacancy_count` | Integer | Open positions (required - filled) | 3 |
| `vacancy_rate` | Float | Vacancy percentage | 11.1% |
| `hiring_priority` | Low \| Medium \| High | Recruitment urgency | "High" |
| `succession_risk` | Low \| Medium \| High | Departure risk | "High" |

---

## Key Numbers (18 Positions)

| Metric | Value | Insight |
|--------|-------|---------|
| **Total Required** | 415 | Target headcount |
| **Total Filled** | 360 | Current staffing |
| **Total Vacancies** | 55 | Open roles |
| **Overall Vacancy Rate** | 13.3% | Realistic for intl org |

---

## Vacancy Rate Reality Check

| Grade | Vacancy % | Why? |
|-------|-----------|------|
| **Analyst** | 18.7% | Entry-level turnover, external hiring friendly |
| **Senior Analyst** | 13.7% | Some retention, but still competitive market |
| **Manager** | 8.3% | Scarce talent, long hiring cycles, low turnover |

This reflects international organization hiring realities.

---

## Succession Risk by Grade

| Grade | High Risk % | Strategic Implication |
|-------|------------|----------------------|
| **Analyst** | 17% | Replaceable; can tolerate turnover |
| **Senior Analyst** | 33% | Key positions; need pipeline |
| **Manager** | 100% | All critical; urgent succession planning |

---

## Hiring Priority Logic

### High Priority (9 of 18 positions, 50%)
- All 7 critical_skill=True positions
- Plus 2 strategic Manager roles
- **Action**: Aggressive recruiting, top salary bands

### Medium Priority (4 positions, 22%)
- Senior Analyst non-critical roles
- **Action**: Moderate recruiting, career pipeline

### Low Priority (5 positions, 28%)
- Non-critical Analyst roles
- **Action**: Monitor, reactive hiring

---

## Real Insight Examples

### 1. Economics & Policy Analyst
- Required: 20 | Filled: 16 | Vacant: 4 (20% vacancy)
- Priority: Low | Risk: Low | Grade: Analyst
- **Interpretation**: Can fill when candidate appears; not urgent

### 2. Data & Analytics Senior Analyst
- Required: 19 | Filled: 18 | Vacant: 1 (5.3% vacancy)
- Priority: High | Risk: High | Grade: Senior Analyst
- Critical Skill: Yes
- **Interpretation**: Urgent strategic hire; scarce talent

### 3. IT & Digital Manager
- Required: 28 | Filled: 27 | Vacant: 1 (3.6% vacancy)
- Priority: High | Risk: High | Grade: Manager
- **Interpretation**: Nearly fully staffed; excellent; protect this team

---

## How to Use This Data

### For Recruitment Planning
```
SELECT * WHERE hiring_priority = 'High'
→ 9 positions requiring immediate attention
→ Focus resources on these 50%
```

### For Succession Planning
```
SELECT * WHERE succession_risk = 'High'
→ 9 positions (all Managers + critical roles)
→ Develop succession plans, track exit risk
```

### For Departmental Staffing Health
```
GROUP BY department, SUM(vacancy_rate)
→ Finance: 13.7% avg | Data: 11.1% avg
→ Identify over/understaffed departments
```

### For Capacity Planning
```
WHERE vacancy_rate > 15%
→ Analyst roles (18.7% avg)
→ Consider: hiring budget, training budget, deadline impacts
```

---

## Validation Summary

✅ 18/18 filled_positions ≤ required_headcount  
✅ 18/18 vacancy_count = required - filled  
✅ No negative vacancies  
✅ Succession risk increases with grade  
✅ 100% of critical skills → High priority  
✅ Realistic vacancy rates by grade level  

---

## Files Included

| File | Purpose |
|------|---------|
| `positions.csv` | Enhanced dataset (ready to use) |
| `enhance_positions.py` | Transparent Python script (reproducible) |
| `POSITIONS_ENHANCEMENT_SUMMARY.md` | Full technical documentation |

---

## Next Steps for Analytics

1. **Link with employees.csv** 
   - Department + Grade matching
   - Analyze actual vs. planned staffing

2. **Build workforce dashboards**
   - Vacancy rate by department / grade / family
   - Succession risk heatmaps
   - Hiring priority vs. open headcount

3. **Predictive modeling**
   - Forecast vacancy rates based on attrition
   - Succession risk trending
   - Recruitment cycle analysis

4. **Strategic planning**
   - Critical skill gap analysis
   - Department growth scenarios
   - Career progression pathways

---

**Status**: ✅ Production Ready | **Date**: Feb 7, 2026 | **Review Level**: Senior HR Professional
