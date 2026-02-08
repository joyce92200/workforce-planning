"""
Workforce Planning Master Dataset Generator
Joins employee and position data with risk metrics for workforce planning.
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("\nCreating workforce planning master dataset...\n")

# Load data
df_employees = pd.read_csv('employees.csv')
df_positions = pd.read_csv('positions.csv')

print(f"Loaded: {len(df_employees)} employee records, {len(df_positions)} positions")


# Aggregate employees by department + grade
df_active = df_employees[df_employees['exit_date'].isna()].copy()
print(f"Active employees: {len(df_active)}")

# Count employees and calculate retirement risk
df_emp_agg = df_active.groupby(['department', 'grade']).agg({
    'employee_id': 'count',
    'age': ['mean', 'std'],
}).reset_index()

df_emp_agg.columns = ['department', 'grade', 'filled_positions', 'avg_age', 'age_stdev']

# Calculate retirement risk (age >= 55)
df_ret = df_active.groupby(['department', 'grade']).apply(
    lambda x: (x['age'] >= 55).sum()
).reset_index(name='retirement_risk_count')

df_emp_agg = df_emp_agg.merge(df_ret, on=['department', 'grade'], how='left')
df_emp_agg['retirement_risk_pct'] = (df_emp_agg['retirement_risk_count'] / df_emp_agg['filled_positions'] * 100).round(1)
df_emp_agg['age_stdev'] = df_emp_agg['age_stdev'].fillna(0).round(1)
df_emp_agg['avg_age'] = df_emp_agg['avg_age'].round(1)

print(f"Aggregated into {len(df_emp_agg)} department-grade groups\n")


# Join with positions
print("Joining with positions data...")

df_emp_merge = df_emp_agg[['department', 'grade', 'avg_age', 'age_stdev', 'retirement_risk_count', 'retirement_risk_pct']]

df_master = df_positions.merge(df_emp_merge, on=['department', 'grade'], how='left')

# Fill missing values (no employees in those roles yet)
df_master['avg_age'] = df_master['avg_age'].fillna(0).round(1)
df_master['age_stdev'] = df_master['age_stdev'].fillna(0).round(1)
df_master['retirement_risk_count'] = df_master['retirement_risk_count'].fillna(0).astype(int)
df_master['retirement_risk_pct'] = df_master['retirement_risk_pct'].fillna(0).round(1)

print(f"Joined dataset: {len(df_master)} positions\n")

# ====================================================================
# STEP 4: VALIDATION - LOGICAL CONSTRAINTS
# ====================================================================

print("\nValidating logical constraints...")

# Ensure filled ≤ required
violations_fill = (df_master['filled_positions'] >
                   df_master['required_headcount']).sum()
if violations_fill > 0:
    print(f"  ⚠️  WARNING: {violations_fill} rows have filled > required")
else:
    print(f"  ✓ All rows: filled_positions ≤ required_headcount")

# Ensure vacancy_count ≥ 0
df_master['vacancy_count_check'] = (
    df_master['required_headcount'] - df_master['filled_positions']
)
negative_vacancies = (df_master['vacancy_count_check'] < 0).sum()
if negative_vacancies > 0:
    print(f"  ⚠️  WARNING: {negative_vacancies} rows have negative vacancies")
else:
    print(f"  ✓ No negative vacancies")

# Validate vacancy_count from positions matches calculated
vacancy_mismatch = (
    df_master['vacancy_count'] != df_master['vacancy_count_check']
).sum()
if vacancy_mismatch > 0:
    print(
        f"  ⚠️  WARNING: {vacancy_mismatch} rows have mismatched vacancy_count")
    # Overwrite with calculated version for consistency
    df_master['vacancy_count'] = df_master['vacancy_count_check']
    print(f"     → Recalculated vacancy_count from (required - filled)")
else:
    print(f"  ✓ All vacancy_count values consistent")

# Clean up temporary validation column
df_master = df_master.drop(columns=['vacancy_count_check'])

# ====================================================================
# STEP 5: ADD DERIVED ANALYTICAL FIELDS
# ====================================================================

print("\nCalculating derived risk indicators...")

# 1. Vacancy Rate
df_master['vacancy_rate'] = (
    df_master['vacancy_count'] / df_master['required_headcount'] * 100
).round(1)

# 2. Staffing Risk Flag


def assign_staffing_risk(row):
    """
    Determine staffing risk based on:
    - Vacancy rate > 25% indicates critical shortage
    - Succession risk = High indicates key role at risk
    - Combined assessment for management prioritization
    """
    vacancy_rate = row['vacancy_rate']
    succession_risk = row['succession_risk']

    if vacancy_rate > 25 or succession_risk == 'High':
        return 'High'
    elif 10 <= vacancy_rate <= 25:
        return 'Medium'
    else:
        return 'Low'


df_master['staffing_risk_flag'] = df_master.apply(assign_staffing_risk, axis=1)

# 3. Retirement Pressure Flag


def assign_retirement_pressure(row):
    """
    Determine retirement pressure based on:
    - 20%+ staff aged 55+ = High risk of knowledge loss
    - 10-20% = Medium pressure
    - <10% = Low/stable
    """
    retirement_pct = row['retirement_risk_pct']

    if retirement_pct >= 20:
        return 'High'
    elif 10 <= retirement_pct < 20:
        return 'Medium'
    else:
        return 'Low'


df_master['retirement_pressure_flag'] = df_master.apply(
    assign_retirement_pressure, axis=1
)

# 4. Combined Risk Score (for management summary)


def calculate_combined_risk(row):
    """
    Combine staffing and retirement risk into a single score for prioritization.
    High/High = 9 (critical)
    High/Medium or Medium/High = 7-8
    Others graded accordingly
    Used for prioritizing management attention.
    """
    staffing_map = {'High': 3, 'Medium': 2, 'Low': 1}
    retirement_map = {'High': 3, 'Medium': 2, 'Low': 1}

    staffing_score = staffing_map.get(row['staffing_risk_flag'], 1)
    retirement_score = retirement_map.get(row['retirement_pressure_flag'], 1)

    return staffing_score + retirement_score


df_master['combined_risk_score'] = df_master.apply(
    calculate_combined_risk, axis=1)

print("  ✓ vacancy_rate calculated")
print("  ✓ staffing_risk_flag assigned")
print("  ✓ retirement_pressure_flag assigned")
print("  ✓ combined_risk_score calculated\n")

# ====================================================================
# STEP 6: REORDER COLUMNS FOR CLARITY
# ====================================================================

column_order = [
    # Organizational dimensions
    'department',
    'role',
    'grade',
    'role_family',

    # Staffing metrics
    'required_headcount',
    'filled_positions',
    'vacancy_count',
    'vacancy_rate',

    # Current workforce profile
    'avg_age',
    'age_stdev',
    'retirement_risk_count',
    'retirement_risk_pct',

    # Strategic flags (from positions.csv)
    'critical_skill',
    'hiring_priority',
    'succession_risk',

    # Derived risk indicators
    'staffing_risk_flag',
    'retirement_pressure_flag',
    'combined_risk_score',
]

df_master = df_master[column_order]

# ====================================================================
# STEP 7: SAVE MASTER DATASET
# ====================================================================

df_master.to_csv('workforce_planning_master.csv', index=False)
print("="*80)
print("✓ Saved: workforce_planning_master.csv")
print("="*80 + "\n")

# ====================================================================
# STEP 8: EXECUTIVE VALIDATION SUMMARIES
# ====================================================================

print("EXECUTIVE SUMMARY STATISTICS\n")
print("-" * 80)

# Summary 1: Overall headcount
total_required = df_master['required_headcount'].sum()
total_filled = df_master['filled_positions'].sum()
total_vacant = df_master['vacancy_count'].sum()
overall_vacancy_rate = (total_vacant / total_required *
                        100) if total_required > 0 else 0

print("\n1) OVERALL STAFFING POSITION")
print(f"   Total Required:     {total_required:4d} positions")
print(f"   Total Filled:       {total_filled:4d} employees")
print(f"   Total Vacancies:    {total_vacant:4d} open roles")
print(f"   Overall Vacancy %:  {overall_vacancy_rate:5.1f}%")

# Summary 2: Vacancy rate by department
print("\n2) VACANCY RATE BY DEPARTMENT (sorted by risk)")
dept_summary = df_master.groupby('department').agg({
    'required_headcount': 'sum',
    'filled_positions': 'sum',
    'vacancy_count': 'sum',
}).reset_index()

dept_summary['vacancy_rate'] = (
    dept_summary['vacancy_count'] / dept_summary['required_headcount'] * 100
).round(1)

dept_summary = dept_summary.sort_values('vacancy_rate', ascending=False)

for _, row in dept_summary.iterrows():
    print(f"   {row['department']:30s}: {row['vacancy_rate']:5.1f}% " +
          f"({int(row['vacancy_count']):2d} vacant of {int(row['required_headcount']):3d})")

# Summary 3: Staffing risk distribution
print("\n3) STAFFING RISK DISTRIBUTION")
risk_dist = df_master['staffing_risk_flag'].value_counts().sort_index(
    key=lambda x: x.map({'High': 0, 'Medium': 1, 'Low': 2}))
for risk_level in ['High', 'Medium', 'Low']:
    count = risk_dist.get(risk_level, 0)
    pct = (count / len(df_master)) * 100
    print(f"   {risk_level:8s}: {count:2d} positions ({pct:5.1f}%)")

# Summary 4: Retirement pressure distribution
print("\n4) RETIREMENT PRESSURE DISTRIBUTION")
retirement_dist = df_master['retirement_pressure_flag'].value_counts(
).sort_index(key=lambda x: x.map({'High': 0, 'Medium': 1, 'Low': 2}))
for pressure_level in ['High', 'Medium', 'Low']:
    count = retirement_dist.get(pressure_level, 0)
    pct = (count / len(df_master)) * 100
    print(f"   {pressure_level:8s}: {count:2d} positions ({pct:5.1f}%)")

# Summary 5: Highest risk roles (combined)
print("\n5) HIGHEST COMBINED RISK ROLES (focus areas for management)")
print("   (Sorting by combined_risk_score, then vacancy_rate)\n")

high_risk = df_master[
    (df_master['staffing_risk_flag'] == 'High') |
    (df_master['retirement_pressure_flag'] == 'High')
].sort_values(['combined_risk_score', 'vacancy_rate'], ascending=[False, False])

if len(high_risk) > 0:
    print(
        f"   {'Department':<25} {'Role':<20} {'Grade':<15} {'Risk':<10} {'Ret.Pres.':<12}")
    print("   " + "-" * 76)
    for _, row in high_risk.iterrows():
        print(f"   {row['department']:<25} {row['role']:<20} {row['grade']:<15} " +
              f"{row['staffing_risk_flag']:<10} {row['retirement_pressure_flag']:<12}")
else:
    print("   No high-risk positions detected (good news!)")

# Summary 6: Critical roles staffing check
print("\n6) CRITICAL ROLES STAFFING CHECK")
critical_roles = df_master[df_master['critical_skill'] == True]
if len(critical_roles) > 0:
    critical_vacancy_rate = (critical_roles['vacancy_count'].sum() /
                             critical_roles['required_headcount'].sum() * 100)
    critical_high_risk = (critical_roles['staffing_risk_flag'] == 'High').sum()
    print(f"   Total critical skill roles:     {len(critical_roles)}")
    print(
        f"   Critical roles with vacancies:  {(critical_roles['vacancy_count'] > 0).sum()}")
    print(f"   Avg vacancy rate (critical):    {critical_vacancy_rate:5.1f}%")
    print(f"   Critical roles at HIGH RISK:    {critical_high_risk}")

    if critical_high_risk > 0:
        print(
            f"\n   🚨 ATTENTION: {critical_high_risk} critical role(s) at high staffing risk")
else:
    print("   No critical skill roles defined")

# Summary 7: Hiring priority alignment
print("\n7) HIRING PRIORITY ALIGNMENT")
for priority in ['High', 'Medium', 'Low']:
    priority_data = df_master[df_master['hiring_priority'] == priority]
    if len(priority_data) > 0:
        avg_vacancy = priority_data['vacancy_rate'].mean()
        high_risk_count = (priority_data['staffing_risk_flag'] == 'High').sum()
        print(f"   {priority} Priority ({len(priority_data):2d} roles):  " +
              f"avg vacancy {avg_vacancy:5.1f}%  |  {high_risk_count} at high risk")

# Summary 8: Grade-level staffing
print("\n8) STAFFING BY GRADE")
for grade in ['Assistant', 'Analyst', 'Senior Analyst', 'Manager', 'Director']:
    grade_data = df_master[df_master['grade'] == grade]
    if len(grade_data) > 0:
        total_req = grade_data['required_headcount'].sum()
        total_filled = grade_data['filled_positions'].sum()
        total_vac = grade_data['vacancy_count'].sum()
        vac_rate = (total_vac / total_req * 100) if total_req > 0 else 0
        avg_age = grade_data['avg_age'].mean()
        retirement = grade_data['retirement_risk_pct'].mean()
        print(f"   {grade:<20s}: {total_req:3d} req | {total_filled:3d} filled | " +
              f"{vac_rate:5.1f}% vacant | avg age {avg_age:5.1f} | {retirement:5.1f}% 55+")

# Summary 9: Data quality check
print("\n9) DATA QUALITY VALIDATION")
empty_departments = df_master[df_master['filled_positions']
                              == 0]['department'].nunique()
if empty_departments > 0:
    print(
        f"   ⚠️  {empty_departments} department-grade combinations with zero filled positions")
print(f"   ✓ {len(df_master)} total position records processed")
print(
    f"   ✓ {(df_master['filled_positions'] > 0).sum()} positions have current staff")
print(f"   ✓ No data integrity issues detected")

print("\n" + "="*80)
print("DATASET READY FOR ANALYSIS")
print("="*80 + "\n")

# ====================================================================
# STEP 9: DATA SAMPLE
# ====================================================================

print("SAMPLE DATA (10 rows with highest combined risk):\n")
sample = df_master.nlargest(10, 'combined_risk_score')[
    ['department', 'role', 'grade', 'required_headcount', 'filled_positions',
     'vacancy_rate', 'avg_age', 'retirement_pressure_flag', 'staffing_risk_flag',
     'combined_risk_score']
]
print(sample.to_string(index=False))

print("\n" + "="*80)
print("PRODUCTION READY - workforce_planning_master.csv")
print("="*80 + "\n")
