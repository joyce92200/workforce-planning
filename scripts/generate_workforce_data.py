"""
Workforce Dataset Generator
Creates realistic synthetic data for workforce analytics.
Total staff: ~1,200 across 6 departments.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os

# Set fixed random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)
fake = Faker()

# Configuration

# Department distribution
DEPARTMENT_DISTRIBUTION = {
    'Economics & Policy': 0.25,
    'Energy & Climate': 0.20,
    'Data & Analytics': 0.15,
    'IT & Digital': 0.15,
    'HR & Operations': 0.15,
    'Communications': 0.10,
}

# Grade distribution
GRADE_DISTRIBUTION = {
    'Assistant': 0.25,
    'Analyst': 0.30,
    'Senior Analyst': 0.25,
    'Manager': 0.15,
    'Director': 0.05,
}

# Age ranges by grade
GRADE_AGE_RANGES = {
    'Assistant': (23, 35),
    'Analyst': (28, 40),
    'Senior Analyst': (35, 50),
    'Manager': (40, 58),
    'Director': (45, 65),
}

# Fixed-term percentage by grade
FIXED_TERM_PERCENTAGE = {
    'Assistant': 0.70,
    'Analyst': 0.50,
    'Senior Analyst': 0.30,
    'Manager': 0.15,
    'Director': 0.05,
}

# Annual attrition rates
ATTRITION_RATES = {
    'Fixed-term': (0.12, 0.15),  # min, max
    'Open-ended': (0.03, 0.05),
}

# Retirement age threshold
RETIREMENT_AGE = 55

# Total headcount target
TOTAL_HEADCOUNT = 1200

# Data generation period (years)
YEARS_LOOKBACK = 15

def generate_employees(total_headcount=TOTAL_HEADCOUNT):
    """Generate employee records with realistic distributions."""

    employees = []

    # Calculate headcount by department and grade
    dept_headcounts = {dept: int(total_headcount * pct)
                       for dept, pct in DEPARTMENT_DISTRIBUTION.items()}

    # Adjust to ensure total = target
    diff = total_headcount - sum(dept_headcounts.values())
    if diff != 0:
        largest_dept = max(dept_headcounts, key=dept_headcounts.get)
        dept_headcounts[largest_dept] += diff

    employee_id_counter = 1

    for department, dept_headcount in dept_headcounts.items():
        # Distribute headcount by grade within department
        grade_counts = {grade: int(dept_headcount * pct)
                        for grade, pct in GRADE_DISTRIBUTION.items()}

        # Adjust for rounding
        grade_diff = dept_headcount - sum(grade_counts.values())
        if grade_diff != 0:
            largest_grade = max(grade_counts, key=grade_counts.get)
            grade_counts[largest_grade] += grade_diff

        for grade, grade_count in grade_counts.items():
            min_age, max_age = GRADE_AGE_RANGES[grade]
            fixed_term_pct = FIXED_TERM_PERCENTAGE[grade]

            for _ in range(grade_count):
                emp_id = f"EMP{employee_id_counter:05d}"
                employee_id_counter += 1
                age = np.random.randint(min_age, max_age + 1)
                gender = np.random.choice(['Female', 'Male'])
                contract_type = 'Fixed-term' if np.random.random() < fixed_term_pct else 'Open-ended'
                
                # hire date within last 15 years
                days_ago = np.random.randint(0, YEARS_LOOKBACK * 365)
                hire_date = datetime(2011, 2, 7) + timedelta(days=days_ago)
                
                # some employees leave; check attrition rate
                exit_date = None
                attrition_min, attrition_max = ATTRITION_RATES[contract_type]
                if np.random.random() < np.random.uniform(attrition_min, attrition_max):
                    max_days_employed = (datetime(2026, 2, 7) - hire_date).days
                    if max_days_employed > 1:
                        exit_date = hire_date + timedelta(days=np.random.randint(1, max_days_employed))

                employees.append({
                    'employee_id': emp_id,
                    'department': department,
                    'grade': grade,
                    'contract_type': contract_type,
                    'age': age,
                    'gender': gender,
                    'hire_date': hire_date.strftime('%Y-%m-%d'),
                    'exit_date': exit_date.strftime('%Y-%m-%d') if exit_date else None,
                })

    df_employees = pd.DataFrame(employees)
    return df_employees


def generate_positions():
    """Generate position records with headcount and critical skills."""

    positions = []
    roles = ['Analyst', 'Senior Analyst', 'Manager']

    for department in DEPARTMENT_DISTRIBUTION.keys():
        for role in roles:
            required_headcount = np.random.randint(15, 41)
            critical_skill = np.random.random() < 0.30  # ~30% are critical

            positions.append({
                'department': department,
                'role': role,
                'required_headcount': required_headcount,
                'critical_skill': critical_skill,
            })

    df_positions = pd.DataFrame(positions)
    return df_positions


def generate_recruitment_pipeline():
    """Generate recruitment pipeline with time-to-fill and candidate counts."""

    pipeline = []
    roles = ['Analyst', 'Senior Analyst', 'Manager']

    for department in DEPARTMENT_DISTRIBUTION.keys():
        for role in roles:
            time_to_fill_days = np.random.randint(60, 181)
            pipeline_size = np.random.randint(3, 26)

            pipeline.append({
                'role': role,
                'department': department,
                'time_to_fill_days': time_to_fill_days,
                'pipeline_size': pipeline_size,
            })

    df_pipeline = pd.DataFrame(pipeline)
    return df_pipeline


def validate_and_summarise(df_employees):
    """Print validation checks and summary statistics."""

    print("\n" + "="*70)
    print("SYNTHETIC WORKFORCE DATASET - VALIDATION & SUMMARY STATISTICS")
    print("="*70)

    active = df_employees[df_employees['exit_date'].isna()]
    print(f"\nTotal active employees: {len(active)}")
    print(f"Total employees (including exits): {len(df_employees)}")
    print("\n--- HEADCOUNT BY DEPARTMENT ---")
    dept_counts = active['department'].value_counts()
    for dept, count in dept_counts.items():
        pct = (count / len(active)) * 100
        exp = DEPARTMENT_DISTRIBUTION[dept] * 100
        print(f"{dept:25s}: {count:4d} ({pct:5.1f}%) [Expected: {exp:5.1f}%]")

    print("\n--- HEADCOUNT BY GRADE ---")
    grade_counts = active['grade'].value_counts()
    for grade in ['Assistant', 'Analyst', 'Senior Analyst', 'Manager', 'Director']:
        count = grade_counts.get(grade, 0)
        pct = (count / len(active)) * 100
        exp = GRADE_DISTRIBUTION[grade] * 100
        print(f"{grade:20s}: {count:4d} ({pct:5.1f}%) [Expected: {exp:5.1f}%]")

    print("\n--- CONTRACT TYPE DISTRIBUTION ---")
    contract_counts = active['contract_type'].value_counts()
    for contract in ['Fixed-term', 'Open-ended']:
        count = contract_counts.get(contract, 0)
        pct = (count / len(active)) * 100
        print(f"{contract:20s}: {count:4d} ({pct:5.1f}%)")

    print("\n--- ATTRITION ANALYSIS ---")
    exited = df_employees[df_employees['exit_date'].notna()]
    attrition_overall = (len(exited) / len(df_employees)) * 100
    print(f"Overall attrition rate: {attrition_overall:.2f}% ({len(exited)} exits)")
    print("\nAttrition by Contract Type:")
    for contract in ['Fixed-term', 'Open-ended']:
        total_c = len(df_employees[df_employees['contract_type'] == contract])
        exits_c = len(df_employees[(df_employees['contract_type'] == contract) & (df_employees['exit_date'].notna())])
        if total_c > 0:
            rate = (exits_c / total_c) * 100
            print(f"  {contract:20s}: {rate:6.2f}% ({exits_c:3d} exits of {total_c:4d})")

    print("\n--- AGE ANALYSIS ---")
    print(f"Average age: {active['age'].mean():.1f} years")
    print(f"Age range: {df_employees['age'].min()} – {df_employees['age'].max()} years")
    
    retirement = len(active[active['age'] >= RETIREMENT_AGE])
    ret_pct = (retirement / len(active)) * 100
    print(f"Staff aged 55+: {retirement} ({ret_pct:.1f}%)")

    print("\n--- GENDER DISTRIBUTION ---")
    gender_counts = active['gender'].value_counts()
    for gender in ['Female', 'Male']:
        count = gender_counts.get(gender, 0)
        pct = (count / len(active)) * 100
        print(f"{gender:20s}: {count:4d} ({pct:5.1f}%)")

    print("\n--- GRADE-AGE RANGE VALIDATION ---")
    all_valid = True
    for grade in GRADE_DISTRIBUTION.keys():
        grade_data = df_employees[df_employees['grade'] == grade]
        min_a, max_a = grade_data['age'].min(), grade_data['age'].max()
        min_e, max_e = GRADE_AGE_RANGES[grade]
        valid = (min_a >= min_e and max_a <= max_e)
        status = "✓" if valid else "✗"
        print(f"{grade:20s}: {min_a}-{max_a} {status} (Expected: {min_e}-{max_e})")
        if not valid:
            all_valid = False
    
    print(f"\nValidation: {'✓ OK' if all_valid else '✗ Issues'}")
    print("="*70 + "\n")

    return all_valid


def main():
    """Generate and save all datasets."""

    print("Generating synthetic workforce dataset...")

    # Generate datasets
    df_employees = generate_employees()
    df_positions = generate_positions()
    df_pipeline = generate_recruitment_pipeline()

    output_dir = os.getcwd()
    
    # save all datasets
    df_employees.to_csv(os.path.join(output_dir, 'employees.csv'), index=False)
    df_positions.to_csv(os.path.join(output_dir, 'positions.csv'), index=False)
    df_pipeline.to_csv(os.path.join(output_dir, 'recruitment_pipeline.csv'), index=False)
    
    print("✓ Saved: employees.csv")
    print("✓ Saved: positions.csv")
    print("✓ Saved: recruitment_pipeline.csv\n")
    
    validate_and_summarise(df_employees)
    
    print("\nSAMPLE DATA (first 10):")
    print(df_employees.head(10).to_string(index=False))
    print(f"... and {len(df_employees) - 10} more records")


if __name__ == '__main__':
    main()
