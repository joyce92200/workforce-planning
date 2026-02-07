"""
Synthetic Workforce Dataset Generator
OECD-style International Organisation
Total staff: ~1,200 employees
Generated: February 7, 2026

This script generates realistic, ethically safe synthetic data for workforce analytics.
No real personal data is included—all attributes are procedurally generated.
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

# ====================================================================
# CONFIGURATION & CONSTANTS
# ====================================================================

# Department distribution (must sum to 100%)
DEPARTMENT_DISTRIBUTION = {
    'Economics & Policy': 0.25,
    'Energy & Climate': 0.20,
    'Data & Analytics': 0.15,
    'IT & Digital': 0.15,
    'HR & Operations': 0.15,
    'Communications': 0.10,
}

# Grade distribution (must sum to 100%)
GRADE_DISTRIBUTION = {
    'Assistant': 0.25,
    'Analyst': 0.30,
    'Senior Analyst': 0.25,
    'Manager': 0.15,
    'Director': 0.05,
}

# Age ranges by grade (strict)
GRADE_AGE_RANGES = {
    'Assistant': (23, 35),
    'Analyst': (28, 40),
    'Senior Analyst': (35, 50),
    'Manager': (40, 58),
    'Director': (45, 65),
}

# Contract type distribution by grade (% fixed-term)
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

# ====================================================================
# STEP 1: GENERATE EMPLOYEES.CSV
# ====================================================================

def generate_employees(total_headcount=TOTAL_HEADCOUNT):
    """
    Generate synthetic employee records with realistic distributions.
    
    Returns:
        pd.DataFrame: Employee records with all required fields
    """
    
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
                # Generate employee attributes
                emp_id = f"EMP{employee_id_counter:05d}"
                employee_id_counter += 1
                
                age = np.random.randint(min_age, max_age + 1)
                gender = np.random.choice(['Female', 'Male'])
                
                # Contract type based on grade
                contract_type = 'Fixed-term' if np.random.random() < fixed_term_pct else 'Open-ended'
                
                # Hire date: within last 15 years
                days_ago = np.random.randint(0, YEARS_LOOKBACK * 365)
                hire_date = datetime(2011, 2, 7) + timedelta(days=days_ago)
                
                # Determine attrition (exit date)
                exit_date = None
                attrition_min, attrition_max = ATTRITION_RATES[contract_type]
                attrition_rate = np.random.uniform(attrition_min, attrition_max)
                
                if np.random.random() < attrition_rate:
                    # Employee has left; exit date is after hire date
                    max_days_employed = (datetime(2026, 2, 7) - hire_date).days
                    if max_days_employed > 1:
                        days_employed = np.random.randint(1, max_days_employed)
                        exit_date = hire_date + timedelta(days=days_employed)
                
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


# ====================================================================
# STEP 2: GENERATE POSITIONS.CSV
# ====================================================================

def generate_positions():
    """
    Generate positional requirements across departments and roles.
    
    Returns:
        pd.DataFrame: Position records with headcount and critical skills
    """
    
    positions = []
    roles = ['Analyst', 'Senior Analyst', 'Manager']
    
    for department in DEPARTMENT_DISTRIBUTION.keys():
        for role in roles:
            # Random required headcount (15-40)
            required_headcount = np.random.randint(15, 41)
            
            # ~30% of positions are critical skills
            critical_skill = True if np.random.random() < 0.30 else False
            
            positions.append({
                'department': department,
                'role': role,
                'required_headcount': required_headcount,
                'critical_skill': critical_skill,
            })
    
    df_positions = pd.DataFrame(positions)
    return df_positions


# ====================================================================
# STEP 3: GENERATE RECRUITMENT_PIPELINE.CSV
# ====================================================================

def generate_recruitment_pipeline():
    """
    Generate recruitment pipeline metrics by role and department.
    
    Returns:
        pd.DataFrame: Recruitment pipeline records
    """
    
    pipeline = []
    roles = ['Analyst', 'Senior Analyst', 'Manager']
    
    for department in DEPARTMENT_DISTRIBUTION.keys():
        for role in roles:
            # Time to fill: 60-180 days
            time_to_fill_days = np.random.randint(60, 181)
            
            # Pipeline size: 3-25 candidates
            pipeline_size = np.random.randint(3, 26)
            
            pipeline.append({
                'role': role,
                'department': department,
                'time_to_fill_days': time_to_fill_days,
                'pipeline_size': pipeline_size,
            })
    
    df_pipeline = pd.DataFrame(pipeline)
    return df_pipeline


# ====================================================================
# VALIDATION & STATISTICS
# ====================================================================

def validate_and_summarise(df_employees):
    """
    Validate distributions and print summary statistics.
    
    Args:
        df_employees (pd.DataFrame): Employee dataset
    """
    
    print("\n" + "="*70)
    print("SYNTHETIC WORKFORCE DATASET - VALIDATION & SUMMARY STATISTICS")
    print("="*70)
    
    # Overall headcount
    print(f"\nTotal Active Employees: {len(df_employees[df_employees['exit_date'].isna()])}")
    print(f"Total Employees (including exits): {len(df_employees)}")
    
    # Headcount by department
    print("\n--- HEADCOUNT BY DEPARTMENT ---")
    dept_counts = df_employees[df_employees['exit_date'].isna()]['department'].value_counts()
    for dept, count in dept_counts.items():
        pct = (count / len(df_employees[df_employees['exit_date'].isna()])) * 100
        expected_pct = DEPARTMENT_DISTRIBUTION[dept] * 100
        print(f"{dept:25s}: {count:4d} ({pct:5.1f}%) [Expected: {expected_pct:5.1f}%]")
    
    # Headcount by grade
    print("\n--- HEADCOUNT BY GRADE ---")
    grade_counts = df_employees[df_employees['exit_date'].isna()]['grade'].value_counts()
    for grade in ['Assistant', 'Analyst', 'Senior Analyst', 'Manager', 'Director']:
        count = grade_counts.get(grade, 0)
        pct = (count / len(df_employees[df_employees['exit_date'].isna()])) * 100
        expected_pct = GRADE_DISTRIBUTION[grade] * 100
        print(f"{grade:20s}: {count:4d} ({pct:5.1f}%) [Expected: {expected_pct:5.1f}%]")
    
    # Contract type distribution
    print("\n--- CONTRACT TYPE DISTRIBUTION ---")
    contract_counts = df_employees[df_employees['exit_date'].isna()]['contract_type'].value_counts()
    for contract in ['Fixed-term', 'Open-ended']:
        count = contract_counts.get(contract, 0)
        pct = (count / len(df_employees[df_employees['exit_date'].isna()])) * 100
        print(f"{contract:20s}: {count:4d} ({pct:5.1f}%)")
    
    # Attrition rates
    print("\n--- ATTRITION ANALYSIS ---")
    total_employees = len(df_employees)
    employees_with_exit = len(df_employees[df_employees['exit_date'].notna()])
    attrition_rate_overall = (employees_with_exit / total_employees) * 100
    print(f"Overall Attrition Rate: {attrition_rate_overall:.2f}% ({employees_with_exit} exits)")
    
    # Attrition by contract type
    print("\nAttrition by Contract Type:")
    for contract in ['Fixed-term', 'Open-ended']:
        total_contract = len(df_employees[df_employees['contract_type'] == contract])
        exits_contract = len(df_employees[(df_employees['contract_type'] == contract) & 
                                          (df_employees['exit_date'].notna())])
        if total_contract > 0:
            rate = (exits_contract / total_contract) * 100
            print(f"  {contract:20s}: {rate:6.2f}% ({exits_contract:3d} exits of {total_contract:4d})")
    
    # Age analysis
    print("\n--- AGE ANALYSIS ---")
    avg_age = df_employees[df_employees['exit_date'].isna()]['age'].mean()
    min_age = df_employees['age'].min()
    max_age = df_employees['age'].max()
    print(f"Average Age: {avg_age:.1f} years")
    print(f"Age Range: {min_age} – {max_age} years")
    
    # Retirement risk (age >= 55)
    retirement_risk = len(df_employees[(df_employees['exit_date'].isna()) & 
                                        (df_employees['age'] >= RETIREMENT_AGE)])
    retirement_pct = (retirement_risk / len(df_employees[df_employees['exit_date'].isna()])) * 100
    print(f"Staff Aged 55+: {retirement_risk} ({retirement_pct:.1f}%) [Retirement Risk]")
    
    # Gender distribution
    print("\n--- GENDER DISTRIBUTION ---")
    active_employees = df_employees[df_employees['exit_date'].isna()]
    gender_counts = active_employees['gender'].value_counts()
    for gender in ['Female', 'Male']:
        count = gender_counts.get(gender, 0)
        pct = (count / len(active_employees)) * 100
        print(f"{gender:20s}: {count:4d} ({pct:5.1f}%)")
    
    # Grade-age validation
    print("\n--- GRADE-AGE RANGE VALIDATION ---")
    all_valid = True
    for grade in GRADE_DISTRIBUTION.keys():
        grade_data = df_employees[df_employees['grade'] == grade]
        min_age_actual = grade_data['age'].min()
        max_age_actual = grade_data['age'].max()
        min_age_expected, max_age_expected = GRADE_AGE_RANGES[grade]
        
        valid = (min_age_actual >= min_age_expected) and (max_age_actual <= max_age_expected)
        status = "✓ VALID" if valid else "✗ INVALID"
        print(f"{grade:20s}: {min_age_actual}-{max_age_actual} years {status} (Expected: {min_age_expected}-{max_age_expected})")
        if not valid:
            all_valid = False
    
    print(f"\nOverall Validation: {'✓ ALL CHECKS PASSED' if all_valid else '✗ VALIDATION ISSUES DETECTED'}")
    print("="*70 + "\n")
    
    return all_valid


# ====================================================================
# MAIN EXECUTION
# ====================================================================

def main():
    """Generate and save all workforce datasets."""
    
    print("Generating synthetic workforce dataset...")
    
    # Generate datasets
    df_employees = generate_employees()
    df_positions = generate_positions()
    df_pipeline = generate_recruitment_pipeline()
    
    # Get current directory
    output_dir = os.getcwd()
    print(f"Output directory: {output_dir}\n")
    
    # Save to CSV
    employees_path = os.path.join(output_dir, 'employees.csv')
    positions_path = os.path.join(output_dir, 'positions.csv')
    pipeline_path = os.path.join(output_dir, 'recruitment_pipeline.csv')
    
    df_employees.to_csv(employees_path, index=False)
    df_positions.to_csv(positions_path, index=False)
    df_pipeline.to_csv(pipeline_path, index=False)
    
    print(f"✓ Saved: {employees_path}")
    print(f"✓ Saved: {positions_path}")
    print(f"✓ Saved: {pipeline_path}\n")
    
    # Validate and print statistics
    validate_and_summarise(df_employees)
    
    # Data sample
    print("SAMPLE DATA (first 10 employees):")
    print(df_employees.head(10).to_string(index=False))
    print(f"\n... and {len(df_employees) - 10} more records")


if __name__ == '__main__':
    main()
