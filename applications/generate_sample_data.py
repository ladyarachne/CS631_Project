"""
Generate Sample Data for CS631 Company Database
Populates the database with realistic test data
"""
from database_config import initialize_connection_pool, close_connection_pool, get_db_cursor
from datetime import date, timedelta
from decimal import Decimal
import random

def clear_all_tables():
    """Clear all data from tables (for testing)"""
    try:
        with get_db_cursor() as cursor:
            tables = [
                'EmployeeOffice', 'ProjectMilestone', 'PayrollHistory', 
                'JobHistory', 'EmployeeProject', 'Project', 'Phone', 
                'Office', 'Building', 'Employee', 'Department', 'Division'
            ]
            for table in tables:
                cursor.execute(f"DELETE FROM {table} CASCADE")
            print("✓ All tables cleared")
    except Exception as e:
        print(f"✗ Error clearing tables: {e}")

def generate_divisions():
    """Generate division data"""
    divisions = [
        (1, 'Technology Division'),
        (2, 'Operations Division'),
        (3, 'Corporate Division'),
        (4, 'Sales & Marketing Division')
    ]
    
    try:
        with get_db_cursor() as cursor:
            for div_id, div_name in divisions:
                cursor.execute("""
                    INSERT INTO Division (division_id, division_name)
                    VALUES (%s, %s)
                """, (div_id, div_name))
            print(f"✓ Generated {len(divisions)} divisions")
    except Exception as e:
        print(f"✗ Error generating divisions: {e}")

def generate_departments():
    """Generate department data"""
    departments = [
        (1, 'Software Development', 500000.00, 1),
        (2, 'Quality Assurance', 250000.00, 1),
        (3, 'IT Infrastructure', 350000.00, 1),
        (4, 'Manufacturing', 600000.00, 2),
        (5, 'Supply Chain', 300000.00, 2),
        (6, 'Human Resources', 200000.00, 3),
        (7, 'Finance', 400000.00, 3),
        (8, 'Legal', 350000.00, 3),
        (9, 'Sales', 450000.00, 4),
        (10, 'Marketing', 300000.00, 4)
    ]
    
    try:
        with get_db_cursor() as cursor:
            for dept_id, dept_name, budget, div_id in departments:
                cursor.execute("""
                    INSERT INTO Department (department_id, department_name, budget, division_id)
                    VALUES (%s, %s, %s, %s)
                """, (dept_id, dept_name, budget, div_id))
            print(f"✓ Generated {len(departments)} departments")
    except Exception as e:
        print(f"✗ Error generating departments: {e}")

def generate_employees():
    """Generate employee data"""
    employees = [
        # Software Development
        (1001, 'Alice Johnson', 'Senior Software Engineer', 'salaried', None, 1, None),
        (1002, 'Bob Smith', 'Software Engineer', 'salaried', None, 1, None),
        (1003, 'Carol White', 'Junior Developer', 'salaried', None, 1, None),
        (1004, 'David Brown', 'Tech Lead', 'salaried', None, 1, None),
        (1005, 'Emma Davis', 'DevOps Engineer', 'salaried', None, 1, None),
        
        # QA
        (2001, 'Frank Miller', 'QA Manager', 'salaried', None, 2, None),
        (2002, 'Grace Wilson', 'QA Engineer', 'salaried', None, 2, None),
        (2003, 'Henry Moore', 'Test Automation Engineer', 'salaried', None, 2, None),
        
        # IT Infrastructure
        (3001, 'Irene Taylor', 'IT Director', 'salaried', None, 3, None),
        (3002, 'Jack Anderson', 'Systems Administrator', 'salaried', None, 3, None),
        (3003, 'Kate Thomas', 'Network Engineer', 'salaried', None, 3, None),
        
        # Manufacturing
        (4001, 'Liam Jackson', 'Manufacturing Manager', 'salaried', None, 4, None),
        (4002, 'Mia Harris', 'Production Supervisor', 'salaried', None, 4, None),
        (4003, 'Noah Martin', 'Assembly Technician', 'hourly', 28.50, 4, None),
        (4004, 'Olivia Thompson', 'Quality Inspector', 'hourly', 25.00, 4, None),
        (4005, 'Paul Garcia', 'Machine Operator', 'hourly', 22.00, 4, None),
        
        # Supply Chain
        (5001, 'Quinn Martinez', 'Supply Chain Director', 'salaried', None, 5, None),
        (5002, 'Rachel Robinson', 'Logistics Coordinator', 'salaried', None, 5, None),
        
        # HR
        (6001, 'Samuel Clark', 'HR Director', 'salaried', None, 6, None),
        (6002, 'Tina Rodriguez', 'HR Specialist', 'salaried', None, 6, None),
        (6003, 'Uma Lewis', 'Recruiter', 'salaried', None, 6, None),
        
        # Finance
        (7001, 'Victor Lee', 'CFO', 'salaried', None, 7, None),
        (7002, 'Wendy Walker', 'Senior Accountant', 'salaried', None, 7, None),
        (7003, 'Xavier Hall', 'Financial Analyst', 'salaried', None, 7, None),
        
        # Legal
        (8001, 'Yara Allen', 'General Counsel', 'salaried', None, 8, None),
        (8002, 'Zack Young', 'Legal Assistant', 'salaried', None, 8, None),
        
        # Sales
        (9001, 'Amy King', 'VP of Sales', 'salaried', None, 9, None),
        (9002, 'Brian Wright', 'Sales Manager', 'salaried', None, 9, None),
        (9003, 'Chloe Lopez', 'Account Executive', 'salaried', None, 9, None),
        (9004, 'Derek Hill', 'Sales Representative', 'salaried', None, 9, None),
        
        # Marketing
        (10001, 'Ella Scott', 'Marketing Director', 'salaried', None, 10, None),
        (10002, 'Felix Green', 'Marketing Manager', 'salaried', None, 10, None),
        (10003, 'Gina Adams', 'Content Specialist', 'salaried', None, 10, None),
        (10004, 'Hugo Baker', 'Graphic Designer', 'hourly', 35.00, 10, None)
    ]
    
    try:
        with get_db_cursor() as cursor:
            for emp_data in employees:
                cursor.execute("""
                    INSERT INTO Employee 
                    (employee_number, employee_name, title, employment_type, 
                     hourly_rate, department_id, division_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, emp_data)
            print(f"✓ Generated {len(employees)} employees")
    except Exception as e:
        print(f"✗ Error generating employees: {e}")

def update_division_and_department_heads():
    """Update division and department heads"""
    updates = [
        # Division heads
        ('Division', 1, 1004),  # Tech Division -> David Brown
        ('Division', 2, 4001),  # Operations -> Liam Jackson
        ('Division', 3, 7001),  # Corporate -> Victor Lee
        ('Division', 4, 9001),  # Sales & Marketing -> Amy King
        
        # Department heads
        ('Department', 1, 1004),  # Software Dev -> David Brown
        ('Department', 2, 2001),  # QA -> Frank Miller
        ('Department', 3, 3001),  # IT -> Irene Taylor
        ('Department', 4, 4001),  # Manufacturing -> Liam Jackson
        ('Department', 5, 5001),  # Supply Chain -> Quinn Martinez
        ('Department', 6, 6001),  # HR -> Samuel Clark
        ('Department', 7, 7001),  # Finance -> Victor Lee
        ('Department', 8, 8001),  # Legal -> Yara Allen
        ('Department', 9, 9001),  # Sales -> Amy King
        ('Department', 10, 10001), # Marketing -> Ella Scott
    ]
    
    try:
        with get_db_cursor() as cursor:
            for table, id_val, emp_id in updates:
                if table == 'Division':
                    cursor.execute("""
                        UPDATE Division SET division_head_emp_id = %s
                        WHERE division_id = %s
                    """, (emp_id, id_val))
                else:
                    cursor.execute("""
                        UPDATE Department SET department_head_emp_id = %s
                        WHERE department_id = %s
                    """, (emp_id, id_val))
            print(f"✓ Updated {len(updates)} division and department heads")
    except Exception as e:
        print(f"✗ Error updating heads: {e}")

def generate_job_history():
    """Generate job history with salaries"""
    # (employee_number, title, start_date, salary, is_current)
    job_history = [
        # Current jobs
        (1001, 'Senior Software Engineer', date(2023, 1, 1), 110000, True),
        (1002, 'Software Engineer', date(2023, 6, 1), 85000, True),
        (1003, 'Junior Developer', date(2025, 1, 1), 65000, True),
        (1004, 'Tech Lead', date(2022, 1, 1), 130000, True),
        (1005, 'DevOps Engineer', date(2023, 3, 1), 95000, True),
        
        (2001, 'QA Manager', date(2022, 6, 1), 95000, True),
        (2002, 'QA Engineer', date(2023, 1, 1), 75000, True),
        (2003, 'Test Automation Engineer', date(2023, 9, 1), 80000, True),
        
        (3001, 'IT Director', date(2021, 1, 1), 125000, True),
        (3002, 'Systems Administrator', date(2022, 3, 1), 78000, True),
        (3003, 'Network Engineer', date(2023, 1, 1), 82000, True),
        
        (4001, 'Manufacturing Manager', date(2020, 1, 1), 105000, True),
        (4002, 'Production Supervisor', date(2022, 6, 1), 72000, True),
        
        (5001, 'Supply Chain Director', date(2021, 6, 1), 115000, True),
        (5002, 'Logistics Coordinator', date(2023, 1, 1), 68000, True),
        
        (6001, 'HR Director', date(2020, 1, 1), 120000, True),
        (6002, 'HR Specialist', date(2022, 1, 1), 65000, True),
        (6003, 'Recruiter', date(2023, 6, 1), 62000, True),
        
        (7001, 'CFO', date(2019, 1, 1), 180000, True),
        (7002, 'Senior Accountant', date(2021, 1, 1), 85000, True),
        (7003, 'Financial Analyst', date(2023, 1, 1), 72000, True),
        
        (8001, 'General Counsel', date(2020, 6, 1), 160000, True),
        (8002, 'Legal Assistant', date(2023, 1, 1), 55000, True),
        
        (9001, 'VP of Sales', date(2021, 1, 1), 140000, True),
        (9002, 'Sales Manager', date(2022, 1, 1), 95000, True),
        (9003, 'Account Executive', date(2023, 1, 1), 78000, True),
        (9004, 'Sales Representative', date(2023, 6, 1), 60000, True),
        
        (10001, 'Marketing Director', date(2021, 6, 1), 115000, True),
        (10002, 'Marketing Manager', date(2022, 6, 1), 88000, True),
        (10003, 'Content Specialist', date(2023, 1, 1), 65000, True),
        
        # Some historical records
        (1001, 'Software Engineer', date(2020, 6, 1), 75000, False),
        (1004, 'Senior Software Engineer', date(2019, 1, 1), 95000, False),
        (7001, 'Finance Director', date(2017, 1, 1), 140000, False),
    ]
    
    try:
        with get_db_cursor() as cursor:
            for emp_num, title, start, salary, is_current in job_history:
                end_date = None if is_current else date(2023, 12, 31)
                cursor.execute("""
                    INSERT INTO JobHistory 
                    (employee_number, title, start_date, end_date, salary, is_current)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (emp_num, title, start, end_date, salary, is_current))
            print(f"✓ Generated {len(job_history)} job history records")
    except Exception as e:
        print(f"✗ Error generating job history: {e}")

def generate_buildings_and_offices():
    """Generate building and office data"""
    buildings = [
        ('HQ-1', 'Headquarters Building', 1995, 5000000),
        ('TECH-2', 'Technology Center', 2010, 8000000),
        ('MFG-3', 'Manufacturing Facility', 2005, 12000000)
    ]
    
    offices = [
        ('101', 250.0, 'HQ-1'),
        ('102', 180.0, 'HQ-1'),
        ('103', 200.0, 'HQ-1'),
        ('104', 150.0, 'HQ-1'),
        ('105', 300.0, 'HQ-1'),
        ('201', 200.0, 'TECH-2'),
        ('202', 180.0, 'TECH-2'),
        ('203', 200.0, 'TECH-2'),
        ('204', 220.0, 'TECH-2'),
        ('205', 180.0, 'TECH-2'),
        ('206', 200.0, 'TECH-2'),
        ('301', 180.0, 'MFG-3'),
        ('302', 150.0, 'MFG-3'),
        ('303', 200.0, 'MFG-3'),
    ]
    
    try:
        with get_db_cursor() as cursor:
            for building_code, name, year, cost in buildings:
                cursor.execute("""
                    INSERT INTO Building (building_code, building_name, year_built_or_bought, cost)
                    VALUES (%s, %s, %s, %s)
                """, (building_code, name, year, cost))
            
            for office_num, area, building in offices:
                cursor.execute("""
                    INSERT INTO Office (office_number, area_sqft, building_code)
                    VALUES (%s, %s, %s)
                """, (office_num, area, building))
            
            print(f"✓ Generated {len(buildings)} buildings and {len(offices)} offices")
    except Exception as e:
        print(f"✗ Error generating buildings/offices: {e}")

def generate_projects():
    """Generate project data"""
    projects = [
        (1, 'Customer Portal Redesign', 250000, date(2025, 1, 15), None, 1004, 1),
        (2, 'Mobile App Development', 350000, date(2023, 9, 1), date(2025, 3, 1), 1001, 1),
        (3, 'Data Migration Project', 180000, date(2025, 2, 1), None, 3001, 3),
        (4, 'Marketing Campaign Q1', 120000, date(2025, 1, 1), date(2025, 3, 31), 10001, 10),
        (5, 'Product Line Expansion', 500000, date(2023, 11, 1), None, 4001, 4),
        (6, 'Sales CRM Implementation', 200000, date(2025, 1, 10), None, 9001, 9),
        (7, 'Automated Testing Framework', 150000, date(2023, 10, 1), None, 2001, 2),
    ]
    
    try:
        with get_db_cursor() as cursor:
            for proj_data in projects:
                cursor.execute("""
                    INSERT INTO Project 
                    (project_number, project_name, budget, date_started, date_ended, 
                     manager_emp_id, department_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, proj_data)
            print(f"✓ Generated {len(projects)} projects")
    except Exception as e:
        print(f"✗ Error generating projects: {e}")

def generate_employee_projects():
    """Generate employee-project assignments"""
    assignments = [
        # Project 1: Customer Portal Redesign (Active)
        (1004, 1, 'Project Manager', 120, date(2025, 1, 15), None, True),
        (1001, 1, 'Lead Developer', 200, date(2025, 1, 15), None, True),
        (1002, 1, 'Backend Developer', 180, date(2025, 1, 15), None, True),
        (1003, 1, 'Frontend Developer', 160, date(2025, 1, 20), None, True),
        (2002, 1, 'QA Engineer', 80, date(2025, 2, 1), None, True),
        
        # Project 2: Mobile App (Completed)
        (1001, 2, 'Technical Lead', 450, date(2023, 9, 1), date(2025, 3, 1), False),
        (1002, 2, 'Developer', 400, date(2023, 9, 1), date(2025, 3, 1), False),
        (2003, 2, 'QA Automation', 200, date(2023, 11, 1), date(2025, 3, 1), False),
        
        # Project 3: Data Migration (Active)
        (3001, 3, 'Project Lead', 150, date(2025, 2, 1), None, True),
        (3002, 3, 'Systems Admin', 180, date(2025, 2, 1), None, True),
        (3003, 3, 'Network Support', 120, date(2025, 2, 5), None, True),
        
        # Project 4: Marketing Campaign (Completed)
        (10001, 4, 'Campaign Director', 220, date(2025, 1, 1), date(2025, 3, 31), False),
        (10002, 4, 'Campaign Manager', 200, date(2025, 1, 1), date(2025, 3, 31), False),
        (10003, 4, 'Content Creator', 180, date(2025, 1, 1), date(2025, 3, 31), False),
        
        # Project 5: Product Line Expansion (Active)
        (4001, 5, 'Production Manager', 250, date(2023, 11, 1), None, True),
        (4002, 5, 'Supervisor', 220, date(2023, 11, 1), None, True),
        (5001, 5, 'Supply Chain Lead', 180, date(2023, 11, 1), None, True),
        
        # Project 6: Sales CRM (Active)
        (9001, 6, 'Executive Sponsor', 80, date(2025, 1, 10), None, True),
        (9002, 6, 'Implementation Lead', 150, date(2025, 1, 10), None, True),
        (1005, 6, 'Technical Consultant', 120, date(2025, 1, 15), None, True),
        
        # Project 7: Testing Framework (Active)
        (2001, 7, 'Project Manager', 140, date(2023, 10, 1), None, True),
        (2003, 7, 'Lead Engineer', 220, date(2023, 10, 1), None, True),
    ]
    
    try:
        with get_db_cursor() as cursor:
            for assignment in assignments:
                cursor.execute("""
                    INSERT INTO EmployeeProject 
                    (employee_number, project_number, role, hours_worked, 
                     start_date, end_date, is_current)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, assignment)
            print(f"✓ Generated {len(assignments)} employee-project assignments")
    except Exception as e:
        print(f"✗ Error generating assignments: {e}")

def generate_milestones():
    """Generate project milestones"""
    milestones = [
        # Project 1
        (1, 'Requirements Analysis', 'Gather and document requirements', date(2025, 2, 1), date(2025, 2, 5), 'completed', 'Requirements documented', 'None'),
        (1, 'UI/UX Design', 'Create mockups and prototypes', date(2025, 2, 15), date(2025, 2, 20), 'completed', 'Designs approved', 'None'),
        (1, 'Backend Development', 'Implement backend APIs', date(2025, 3, 15), None, 'in_progress', 'API endpoints 60% complete', 'Authentication and admin APIs'),
        (1, 'Frontend Development', 'Build user interface', date(2025, 3, 20), None, 'in_progress', 'Core components built', 'Admin dashboard and reports'),
        (1, 'Testing & QA', 'Quality assurance testing', date(2025, 4, 1), None, 'pending', 'None', 'Full test coverage needed'),
        
        # Project 3
        (3, 'Data Assessment', 'Assess current data structure', date(2025, 2, 15), date(2025, 2, 18), 'completed', 'Assessment complete', 'None'),
        (3, 'Migration Script Development', 'Develop migration scripts', date(2025, 3, 1), None, 'in_progress', 'Scripts 70% complete', 'Error handling and logging'),
        (3, 'Test Migration', 'Run test migration', date(2025, 3, 25), None, 'pending', 'None', 'Waiting for scripts completion'),
        
        # Project 5
        (5, 'Market Research', 'Research target markets', date(2023, 12, 1), date(2023, 12, 15), 'completed', 'Research complete', 'None'),
        (5, 'Product Design', 'Design new product variations', date(2025, 1, 15), date(2025, 1, 30), 'completed', 'Designs approved', 'None'),
        (5, 'Prototype Development', 'Build prototypes', date(2025, 2, 28), None, 'in_progress', 'First prototypes built', 'Final iteration needed'),
        
        # Project 6
        (6, 'Requirements Gathering', 'Define CRM requirements', date(2025, 1, 25), date(2025, 1, 28), 'completed', 'Requirements defined', 'None'),
        (6, 'System Configuration', 'Configure CRM system', date(2025, 2, 15), None, 'in_progress', 'Basic config done', 'Custom fields and workflows'),
        (6, 'User Training', 'Train sales team', date(2025, 3, 15), None, 'pending', 'None', 'Training materials to be created'),
    ]
    
    try:
        with get_db_cursor() as cursor:
            for milestone in milestones:
                cursor.execute("""
                    INSERT INTO ProjectMilestone 
                    (project_number, milestone_name, description, due_date, 
                     completion_date, status, details_done, details_remaining)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, milestone)
            print(f"✓ Generated {len(milestones)} project milestones")
    except Exception as e:
        print(f"✗ Error generating milestones: {e}")

def main():
    """Main function to generate all sample data"""
    print("\n" + "="*60)
    print("CS631 Company Database - Sample Data Generation")
    print("="*60 + "\n")
    
    try:
        initialize_connection_pool()
        
        print("Clearing existing data...")
        clear_all_tables()
        print()
        
        print("Generating organizational structure...")
        generate_divisions()
        generate_departments()
        print()
        
        print("Generating employee data...")
        generate_employees()
        update_division_and_department_heads()
        generate_job_history()
        print()
        
        print("Generating facilities data...")
        generate_buildings_and_offices()
        print()
        
        print("Generating project data...")
        generate_projects()
        generate_employee_projects()
        generate_milestones()
        print()
        
        print("="*60)
        print("✓ Sample data generation completed successfully!")
        print("="*60 + "\n")
        
        print("Summary:")
        with get_db_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Division")
            print(f"  Divisions: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM Department")
            print(f"  Departments: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM Employee")
            print(f"  Employees: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM Building")
            print(f"  Buildings: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM Office")
            print(f"  Offices: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM Project")
            print(f"  Projects: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM EmployeeProject")
            print(f"  Employee-Project Assignments: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM ProjectMilestone")
            print(f"  Milestones: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM JobHistory")
            print(f"  Job History Records: {cursor.fetchone()[0]}")
        print()
        
    except Exception as e:
        print(f"\n✗ Error during data generation: {e}")
    finally:
        close_connection_pool()

if __name__ == "__main__":
    main()
