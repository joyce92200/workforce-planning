"""
Enhance positions.csv for Workforce Planning & Vacancy Analysis
OECD-style International Organisation

This script transforms the basic positions.csv into a more realistic,
analytically useful workforce planning dataset that supports:
- Vacancy rate analysis
- Succession risk assessment
- Hiring priority planning
- Grade-level staffing analysis

Assumptions:
- Role_family is mapped by department and function
- Succession risk increases with seniority (Analyst < Senior Analyst < Manager)
- Hiring priority aligns with critical skills but adds nuance
- Filled positions are realistic (80-95% fill rate on average)
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# ====================================================================
# LOAD EXISTING DATA
# ====================================================================

df_positions = pd.read_csv('positions.csv')

print("Original positions.csv shape:", df_positions.shape)
print("\nOriginal schema:")
print(df_positions.head(10))

# ====================================================================
# ENHANCEMENT LOGIC
# ====================================================================


def map_role_to_grade(role):
    """Map role name to grade level."""
    grade_map = {
        'Analyst': 'Analyst',
        'Senior Analyst': 'Senior Analyst',
        'Manager': 'Manager',
    }
    return grade_map.get(role, role)


def map_department_to_role_family(department):
    """
    Map department to role_family.
    Role families represent functional areas:
    - Policy: Policy, strategy, economics
    - Technical: Data, IT, analytics
    - Corporate: HR, operations, communications
    - Digital: Digital transformation, IT infrastructure
    """
    role_family_map = {
        'Economics & Policy': 'Policy',
        'Energy & Climate': 'Policy',
        'Data & Analytics': 'Technical',
        'IT & Digital': 'Digital',
        'HR & Operations': 'Corporate',
        'Communications': 'Corporate',
    }
    return role_family_map.get(department, 'Other')


def assign_succession_risk(grade, critical_skill):
    """
    Assign succession risk based on grade and criticality.

    Logic:
    - Analyst: Low by default, Medium if critical
    - Senior Analyst: Medium, High if critical
    - Manager: High (key leadership positions)
    """
    if grade == 'Analyst':
        return 'High' if critical_skill else 'Low'
    elif grade == 'Senior Analyst':
        return 'High' if critical_skill else 'Medium'
    elif grade == 'Manager':
        return 'High'  # All managers are succession-critical
    return 'Medium'


def assign_hiring_priority(grade, critical_skill, succession_risk):
    """
    Assign hiring priority based on criticality and succession risk.

    Logic:
    - High: Critical skills OR high succession risk
    - Medium: Senior roles without critical flag
    - Low: Analyst roles without critical flag
    """
    if critical_skill or succession_risk == 'High':
        return 'High'
    elif grade in ['Senior Analyst', 'Manager']:
        return 'Medium'
    else:
        return 'Low'


def calculate_filled_positions(required_headcount, grade, critical_skill):
    """
    Calculate realistic filled positions.

    Assumptions:
    - Analyst roles: 80-90% filled (higher demand/churn)
    - Senior Analyst: 85-95% filled (critical talent)
    - Manager: 90-98% filled (senior positions rarer)
    - Critical skills: higher fill rate (more demand to fill)

    This simulates realistic vacancy patterns in international orgs.
    """
    if grade == 'Analyst':
        # Higher vacancy for Analyst (entry-level turnover)
        base_fill_rate = 0.87 if critical_skill else 0.82
    elif grade == 'Senior Analyst':
        # Lower vacancy for senior roles
        base_fill_rate = 0.93 if critical_skill else 0.89
    elif grade == 'Manager':
        # Very low vacancy (hard to find managers)
        base_fill_rate = 0.96 if critical_skill else 0.91
    else:
        base_fill_rate = 0.90

    # Add realistic variation (±3%)
    variation = np.random.uniform(-0.03, 0.03)
    fill_rate = max(0.70, min(0.99, base_fill_rate + variation))

    return int(np.floor(required_headcount * fill_rate))


# ====================================================================
# APPLY ENHANCEMENTS
# ====================================================================

# Add grade column
df_positions['grade'] = df_positions['role'].apply(map_role_to_grade)

# Add role_family column
df_positions['role_family'] = df_positions['department'].apply(
    map_department_to_role_family
)

# Add succession_risk column
df_positions['succession_risk'] = df_positions.apply(
    lambda row: assign_succession_risk(row['grade'], row['critical_skill']),
    axis=1
)

# Add hiring_priority column
df_positions['hiring_priority'] = df_positions.apply(
    lambda row: assign_hiring_priority(
        row['grade'],
        row['critical_skill'],
        row['succession_risk']
    ),
    axis=1
)

# Add filled_positions column
df_positions['filled_positions'] = df_positions.apply(
    lambda row: calculate_filled_positions(
        row['required_headcount'],
        row['grade'],
        row['critical_skill']
    ),
    axis=1
)

# Add vacancy_count column (derived, not random)
df_positions['vacancy_count'] = (
    df_positions['required_headcount'] - df_positions['filled_positions']
)

# Add vacancy_rate for analytics
df_positions['vacancy_rate'] = (
    df_positions['vacancy_count'] / df_positions['required_headcount'] * 100
).round(1)

# ====================================================================
# REORDER COLUMNS FOR CLARITY
# ====================================================================

column_order = [
    'department',
    'role',
    'grade',
    'role_family',
    'required_headcount',
    'filled_positions',
    'vacancy_count',
    'vacancy_rate',
    'critical_skill',
    'hiring_priority',
    'succession_risk',
]

df_positions = df_positions[column_order]

# ====================================================================
# VALIDATION & CONSTRAINTS
# ====================================================================

print("\n" + "="*80)
print("VALIDATION CHECKS")
print("="*80)

# Check 1: No negative vacancies
negative_vacancies = (df_positions['vacancy_count'] < 0).sum()
print(f"\n✓ Negative vacancies: {negative_vacancies} (Expected: 0)")
if negative_vacancies > 0:
    print("  ⚠️ WARNING: Some positions have negative vacancy counts!")

# Check 2: Vacancy count = required - filled
vacancy_matches = (
    df_positions['vacancy_count'] ==
    (df_positions['required_headcount'] - df_positions['filled_positions'])
).sum()
print(
    f"✓ Vacancy count consistency: {vacancy_matches}/{len(df_positions)} rows valid")

# Check 3: Filled ≤ Required
fill_constraint = (df_positions['filled_positions']
                   <= df_positions['required_headcount']).sum()
print(
    f"✓ Filled ≤ Required constraint: {fill_constraint}/{len(df_positions)} rows valid")

# Check 4: Distribution of hiring priority
print("\n--- HIRING PRIORITY DISTRIBUTION ---")
priority_dist = df_positions['hiring_priority'].value_counts().sort_index()
for priority in ['Low', 'Medium', 'High']:
    count = priority_dist.get(priority, 0)
    pct = (count / len(df_positions)) * 100
    print(f"  {priority:10s}: {count:2d} ({pct:5.1f}%)")

# Check 5: Succession risk by grade
print("\n--- SUCCESSION RISK BY GRADE ---")
for grade in ['Analyst', 'Senior Analyst', 'Manager']:
    grade_data = df_positions[df_positions['grade'] == grade]
    risk_dist = grade_data['succession_risk'].value_counts().sort_index()
    print(f"\n  {grade}:")
    for risk in ['Low', 'Medium', 'High']:
        count = risk_dist.get(risk, 0)
        pct = (count / len(grade_data)) * 100 if len(grade_data) > 0 else 0
        print(f"    {risk:10s}: {count:2d} ({pct:5.1f}%)")

# Check 6: Critical skills alignment with priorities
print("\n--- CRITICAL SKILLS ALIGNMENT ---")
critical_high_priority = df_positions[
    (df_positions['critical_skill'] == True) &
    (df_positions['hiring_priority'] == 'High')
].shape[0]
critical_total = df_positions[df_positions['critical_skill'] == True].shape[0]
alignment_pct = (critical_high_priority / critical_total *
                 100) if critical_total > 0 else 0
print(
    f"  Critical skills with High priority: {critical_high_priority}/{critical_total} ({alignment_pct:.1f}%)")

# Check 7: Vacancy rate statistics
print("\n--- VACANCY RATE STATISTICS ---")
print(f"  Mean vacancy rate: {df_positions['vacancy_rate'].mean():.1f}%")
print(f"  Median vacancy rate: {df_positions['vacancy_rate'].median():.1f}%")
print(
    f"  Min/Max: {df_positions['vacancy_rate'].min():.1f}% / {df_positions['vacancy_rate'].max():.1f}%")

# Check 8: Vacancy rate by grade
print("\n--- AVERAGE VACANCY RATE BY GRADE ---")
for grade in ['Analyst', 'Senior Analyst', 'Manager']:
    grade_data = df_positions[df_positions['grade'] == grade]
    avg_vacancy = grade_data['vacancy_rate'].mean()
    print(f"  {grade:20s}: {avg_vacancy:5.1f}%")

# ====================================================================
# SAVE ENHANCED DATA
# ====================================================================

df_positions.to_csv('positions.csv', index=False)
print("\n" + "="*80)
print("✓ Enhanced positions.csv saved successfully")
print("="*80)

# ====================================================================
# SUMMARY STATISTICS
# ====================================================================

print("\nENHANCED DATASET SUMMARY")
print("-" * 80)
print(f"Total positions: {len(df_positions)}")
print(f"Total required headcount: {df_positions['required_headcount'].sum()}")
print(f"Total filled positions: {df_positions['filled_positions'].sum()}")
print(f"Total vacancies: {df_positions['vacancy_count'].sum()}")
print(
    f"Overall vacancy rate: {(df_positions['vacancy_count'].sum() / df_positions['required_headcount'].sum() * 100):.1f}%")

print("\nBy Department:")
dept_summary = df_positions.groupby('department').agg({
    'required_headcount': 'sum',
    'filled_positions': 'sum',
    'vacancy_count': 'sum'
}).round(0)
dept_summary['vacancy_rate'] = (
    dept_summary['vacancy_count'] / dept_summary['required_headcount'] * 100
).round(1)
print(dept_summary)

print("\n" + "="*80)
print("Dataset is now ready for advanced workforce analytics and planning!")
print("="*80)

# Display sample
print("\nSAMPLE DATA:")
print(df_positions.head(10).to_string(index=False))
