"""
Demo Script for CS631 Company Database Applications
Demonstrates HR/Payroll and Project Management functionality
"""
from database_config import initialize_connection_pool, close_connection_pool
from hr_payroll_app import (
    HRPayrollApp, print_employee_info, print_employee_list, print_payroll_report
)
from project_management_app import (
    ProjectManagementApp, print_project_info, print_project_list,
    print_project_team, print_milestones, print_project_statistics
)
from datetime import date, timedelta
from decimal import Decimal

def print_section_header(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def demo_hr_payroll():
    """Demonstrate HR/Payroll application functionality"""
    print_section_header("HR/PAYROLL APPLICATION DEMO")
    
    hr_app = HRPayrollApp()
    
    # 1. List all employees
    print("1. LISTING ALL EMPLOYEES")
    print("-" * 70)
    employees = hr_app.list_all_employees()
    print_employee_list(employees[:10])  # Show first 10
    print(f"Total employees: {len(employees)}\n")
    
    # 2. Get specific employee information
    print("2. EMPLOYEE DETAILS - Alice Johnson (ID: 1001)")
    print("-" * 70)
    emp_info = hr_app.get_employee_info(1001)
    print_employee_info(emp_info)
    
    # 3. Show salary history
    print("3. SALARY HISTORY - Alice Johnson")
    print("-" * 70)
    salary_history = hr_app.get_employee_salary_history(1001)
    if salary_history:
        print(f"{'Job ID':<10} {'Title':<30} {'Salary':<15} {'Start Date':<12} {'Current':<10}")
        print("-" * 77)
        for record in salary_history:
            job_id, title, salary, start, end, is_current = record
            current_str = "✓ Yes" if is_current else "  No"
            print(f"{job_id:<10} {title:<30} ${salary:>13,.2f} {start!s:<12} {current_str:<10}")
    print()
    
    # 4. Process Payroll
    print("4. PROCESSING PAYROLL - March 2024")
    print("-" * 70)
    pay_start = date(2025, 3, 1)
    pay_end = date(2025, 3, 31)
    payment_date = date(2025, 4, 3)
    
    payroll_records = hr_app.process_payroll(pay_start, pay_end, payment_date)
    print(f"Processed {len(payroll_records)} payroll records\n")
    
    # 5. Show Payroll Report
    print("5. PAYROLL REPORT - March 2025")
    print("-" * 70)
    payroll_data = hr_app.get_payroll_report(pay_start, pay_end)
    print_payroll_report(payroll_data[:10])  # Show first 10
    
    # 6. Employee Annual Tax Summary
    print("6. ANNUAL TAX SUMMARY - Victor Lee (CFO) - 2025")
    print("-" * 70)
    tax_summary = hr_app.get_yearly_tax_summary(7001, 2025)
    if tax_summary:
        print(f"  Employee: Victor Lee (7001)")
        print(f"  Year: 2024")
        print(f"  Pay Periods: {tax_summary['pay_periods']}")
        print(f"  Total Gross Pay: ${tax_summary['total_gross']:,.2f}")
        print(f"  Federal Tax:     ${tax_summary['total_federal']:,.2f}")
        print(f"  State Tax:       ${tax_summary['total_state']:,.2f}")
        print(f"  Other Tax:       ${tax_summary['total_other']:,.2f}")
        print(f"  Total Net Pay:   ${tax_summary['total_net']:,.2f}")
    print()
    
    # 7. Department Payroll Summary
    print("7. DEPARTMENT PAYROLL SUMMARY")
    print("-" * 70)
    dept_summary = hr_app.department_payroll_summary()
    if dept_summary:
        print(f"{'Department':<25} {'Employees':<12} {'Avg Salary':<15} {'Total Salary':<15}")
        print("-" * 67)
        for record in dept_summary:
            dept_name, emp_count, avg_sal, total_sal = record
            avg = avg_sal if avg_sal else 0
            total = total_sal if total_sal else 0
            print(f"{dept_name:<25} {emp_count:<12} ${avg:>13,.2f} ${total:>13,.2f}")
    print()
    
    # 8. Promote an Employee
    print("8. EMPLOYEE PROMOTION - Carol White")
    print("-" * 70)
    print("Promoting Carol White from Junior Developer to Software Engineer")
    hr_app.update_employee_title(1003, 'Software Engineer', 75000, date(2025, 4, 1))
    print()

def demo_project_management():
    """Demonstrate Project Management application functionality"""
    print_section_header("PROJECT MANAGEMENT APPLICATION DEMO")
    
    pm_app = ProjectManagementApp()
    
    # 1. List all projects
    print("1. LISTING ALL PROJECTS")
    print("-" * 70)
    projects = pm_app.list_all_projects()
    print_project_list(projects)
    
    # 2. Get specific project information
    print("2. PROJECT DETAILS - Customer Portal Redesign (Project 1)")
    print("-" * 70)
    proj_info = pm_app.get_project_info(1)
    print_project_info(proj_info)
    
    # 3. Show project team
    print("3. PROJECT TEAM - Customer Portal Redesign")
    print("-" * 70)
    team = pm_app.get_project_team(1, current_only=True)
    print_project_team(team)
    
    # 4. Show project milestones
    print("4. PROJECT MILESTONES - Customer Portal Redesign")
    print("-" * 70)
    milestones = pm_app.get_project_milestones(1)
    print_milestones(milestones)
    
    # 5. Project Statistics
    print("5. PROJECT STATISTICS - Customer Portal Redesign")
    print("-" * 70)
    stats = pm_app.get_project_statistics(1)
    print_project_statistics(stats)
    
    # 6. Employee's Projects
    print("6. EMPLOYEE'S PROJECT HISTORY - Alice Johnson (1001)")
    print("-" * 70)
    emp_projects = pm_app.get_employee_projects(1001, current_only=False)
    if emp_projects:
        print(f"{'Proj #':<8} {'Project Name':<30} {'Role':<20} {'Hours':<10} {'Status':<10}")
        print("-" * 78)
        for proj in emp_projects:
            proj_num, proj_name, role, hours, start, end, manager = proj
            status = "Active" if end is None else "Completed"
            print(f"{proj_num:<8} {proj_name:<30} {role:<20} {hours:>8.1f} {status:<10}")
    print()
    
    # 7. Update project hours
    print("7. UPDATING PROJECT HOURS")
    print("-" * 70)
    print("Adding 40 hours for Alice Johnson on Project 1")
    pm_app.update_employee_project_hours(1001, 1, 40)
    print()
    
    # 8. Complete a milestone
    print("8. COMPLETING A MILESTONE")
    print("-" * 70)
    print("Marking 'Backend Development' milestone as completed")
    pm_app.complete_milestone(3, date(2025, 3, 20))
    print()
    
    # 9. Department Projects Summary
    print("9. DEPARTMENT PROJECTS SUMMARY")
    print("-" * 70)
    dept_proj_summary = pm_app.get_department_projects_summary()
    if dept_proj_summary:
        print(f"{'Department':<25} {'Total':<8} {'Active':<8} {'Budget':<15} {'Avg Team':<10} {'Total Hours':<12}")
        print("-" * 78)
        for record in dept_proj_summary:
            dept, total, active, budget, avg_team, hours = record
            budget_val = budget if budget else 0
            avg_team_val = avg_team if avg_team else 0
            hours_val = hours if hours else 0
            print(f"{dept:<25} {total:<8} {active:<8} ${budget_val:>13,.2f} {avg_team_val:>8.1f} {hours_val:>10,.1f}")
    print()
    
    # 10. Employee Productivity Report
    print("10. EMPLOYEE PRODUCTIVITY REPORT (Top 10)")
    print("-" * 70)
    productivity = pm_app.get_employee_productivity_report()
    if productivity:
        print(f"{'Emp #':<8} {'Name':<25} {'Title':<20} {'Projects':<10} {'Total Hours':<12} {'Current':<10}")
        print("-" * 85)
        for record in productivity[:10]:
            emp_num, name, title, dept, proj_count, hours, current = record
            print(f"{emp_num:<8} {name:<25} {title:<20} {proj_count:<10} {hours:>10,.1f} {current:<10}")
    print()
    
    # 11. Create a new project
    print("11. CREATING A NEW PROJECT")
    print("-" * 70)
    pm_app.create_project(
        project_number=8,
        project_name='Cloud Infrastructure Upgrade',
        budget=Decimal('300000.00'),
        date_started=date(2025, 4, 1),
        manager_emp_id=3001,
        department_id=3
    )
    print()
    
    # 12. Assign employees to new project
    print("12. ASSIGNING TEAM TO NEW PROJECT")
    print("-" * 70)
    pm_app.assign_employee_to_project(3001, 8, 'Project Manager', date(2025, 4, 1), 0, True)
    pm_app.assign_employee_to_project(3002, 8, 'Systems Engineer', date(2025, 4, 1), 0, True)
    pm_app.assign_employee_to_project(3003, 8, 'Network Engineer', date(2025, 4, 1), 0, True)
    print()

def demo_combined_scenarios():
    """Demonstrate combined scenarios using both applications"""
    print_section_header("COMBINED SCENARIOS")
    
    hr_app = HRPayrollApp()
    pm_app = ProjectManagementApp()
    
    # Scenario 1: Hiring and assigning to project
    print("SCENARIO 1: Onboarding New Employee")
    print("-" * 70)
    print("Step 1: Add new employee")
    hr_app.add_employee(
        employee_number=1006,
        name='Tom Anderson',
        title='Software Engineer',
        employment_type='salaried',
        department_id=1
    )
    
    print("\nStep 2: Create job history record")
    hr_app.add_job_history(1006, 'Software Engineer', date(2025, 4, 1), 90000, is_current=True)
    
    print("\nStep 3: Assign to project")
    pm_app.assign_employee_to_project(1006, 1, 'Backend Developer', date(2025, 4, 1), 0, True)
    print()
    
    # Scenario 2: Project completion and employee reassignment
    print("SCENARIO 2: Completing Project and Reassigning Team")
    print("-" * 70)
    print("Step 1: Update project end date")
    pm_app.update_project(7, date_ended=date(2025, 3, 31))
    
    print("\nStep 2: Remove employees from completed project")
    pm_app.remove_employee_from_project(2001, 7, date(2025, 3, 31))
    pm_app.remove_employee_from_project(2003, 7, date(2025, 3, 31))
    print()

def main():
    """Main demo function"""
    print("\n" + "="*70)
    print("  CS631 COMPANY DATABASE - APPLICATION DEMONSTRATION")
    print("  HR/Payroll & Project Management Systems")
    print("="*70)
    
    try:
        # Initialize database connection
        initialize_connection_pool()
        print("\n✓ Database connection established\n")
        
        # Run demos
        demo_hr_payroll()
        demo_project_management()
        demo_combined_scenarios()
        
        # Summary
        print_section_header("DEMO COMPLETED SUCCESSFULLY")
        print("All application features demonstrated:")
        print("  ✓ Employee management and tracking")
        print("  ✓ Salary history and job changes")
        print("  ✓ Payroll processing and tax calculations")
        print("  ✓ Project creation and management")
        print("  ✓ Team assignments and tracking")
        print("  ✓ Milestone tracking and completion")
        print("  ✓ Comprehensive reporting and statistics")
        print("  ✓ Integrated HR and PM workflows")
        print()
        
    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        close_connection_pool()
        print("✓ Database connection closed\n")

if __name__ == "__main__":
    main()
