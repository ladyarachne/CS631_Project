# CS631 Company Personnel Database Project

A complete database system implementation for managing company personnel, projects, and payroll operations. This project demonstrates end-to-end database design from ER modeling to fully functional applications.

## 📋 Project Overview

This project implements a comprehensive database system for a company with:
- **Organizational structure**: Divisions, departments, employees
- **HR & Payroll management**: Salary tracking, payroll processing, tax calculations
- **Project management**: Project assignments, team tracking, milestone management
- **Facilities management**: Buildings, offices, phone assignments

## 🗂️ Project Structure

```
CS631_Project/
├── database/
│   └── schema.sql                 # Complete PostgreSQL DDL schema
├── documentation/
│   ├── ER_Design_and_Decisions.md # ER diagram and design decisions
│   └── Relational_Schema.md       # Relational schema documentation
├── applications/
│   ├── database_config.py         # Database connection management
│   ├── hr_payroll_app.py          # HR/Payroll application
│   ├── project_management_app.py  # Project management application
│   ├── generate_sample_data.py    # Sample data generator
│   └── demo.py                    # Comprehensive demo script
└── README.md                      # This file
```

## 🎯 Key Features

### HR/Payroll Application
- ✅ Employee management (salaried and hourly)
- ✅ Job title and salary history tracking
- ✅ Monthly payroll processing
- ✅ Automatic tax calculations (10% federal, 5% state, 3% other)
- ✅ Annual tax summaries (W-2 style)
- ✅ Department payroll reports
- ✅ Employee promotions and salary adjustments

### Project Management Application
- ✅ Project creation and tracking
- ✅ Team member assignments with roles
- ✅ Hours tracking per employee/project
- ✅ Milestone management (pending/in_progress/completed)
- ✅ Project statistics and person-hours reporting
- ✅ Department project summaries
- ✅ Employee productivity reports

## 🚀 Getting Started

### Prerequisites

- **PostgreSQL** 12+ installed and running
- **Python** 3.8+ installed
- **psycopg2** library for Python-PostgreSQL connectivity

### Installation

1. **Install PostgreSQL** (if not already installed):
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database credentials**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your actual database credentials
   # The .env file is in .gitignore and won't be committed to git
   ```
   
   Edit `.env` and update with your credentials:
   ```
   DB_HOST=localhost
   DB_NAME=cs631_company_db
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_PORT=5432
   ```

4. **Create the database**:
   ```bash
   # Connect to PostgreSQL
   psql postgres
   
   # Create database
   CREATE DATABASE cs631_company_db;
   \q
   ```

5. **Load the schema**:
   ```bash
   psql cs631_company_db < database/schema.sql
   ```

### Loading Sample Data

Generate realistic sample data to populate the database:

```bash
cd applications
python generate_sample_data.py
```

This will create:
- 4 divisions
- 10 departments
- 34 employees (salaried and hourly)
- 3 buildings with 14 offices
- 7 projects with team assignments
- 14 project milestones
- Complete job history records

## 💻 Running the Applications

### Quick Demo

Run the comprehensive demo to see all features in action:

```bash
cd applications
python demo.py
```

The demo demonstrates:
1. **HR/Payroll features**: Employee listings, salary history, payroll processing
2. **Project Management features**: Project tracking, team assignments, milestones
3. **Combined scenarios**: Onboarding new employees and assigning to projects

### Using the Applications in Your Code

#### HR/Payroll Application

```python
from database_config import initialize_connection_pool, close_connection_pool
from hr_payroll_app import HRPayrollApp, print_employee_info
from datetime import date

# Initialize
initialize_connection_pool()
hr_app = HRPayrollApp()

# Get employee information
emp_info = hr_app.get_employee_info(1001)
print_employee_info(emp_info)

# Process payroll for March 2025
payroll = hr_app.process_payroll(
    pay_period_start=date(2025, 3, 1),
    pay_period_end=date(2025, 3, 31)
)

# Promote an employee
hr_app.update_employee_title(
    employee_number=1003,
    new_title='Senior Developer',
    new_salary=95000,
    effective_date=date(2025, 4, 1)
)

# Get annual tax summary
tax_summary = hr_app.get_yearly_tax_summary(1001, 2025)

# Cleanup
close_connection_pool()
```

#### Project Management Application

```python
from database_config import initialize_connection_pool, close_connection_pool
from project_management_app import ProjectManagementApp, print_project_statistics
from datetime import date
from decimal import Decimal

# Initialize
initialize_connection_pool()
pm_app = ProjectManagementApp()

# Create a new project
proj_num = pm_app.create_project(
    project_number=10,
    project_name='Website Redesign',
    budget=Decimal('150000.00'),
    date_started=date(2025, 4, 1),
    manager_emp_id=1004,
    department_id=1
)

# Assign team members
pm_app.assign_employee_to_project(1001, 10, 'Lead Developer', date(2025, 4, 1))
pm_app.assign_employee_to_project(1002, 10, 'Backend Dev', date(2025, 4, 1))

# Add a milestone
milestone_id = pm_app.add_milestone(
    project_number=10,
    milestone_name='Requirements Gathering',
    description='Collect and document all requirements',
    due_date=date(2025, 4, 15),
    status='in_progress'
)

# Update hours worked
pm_app.update_employee_project_hours(1001, 10, 40)

# Get project statistics
stats = pm_app.get_project_statistics(10)
print_project_statistics(stats)

# Cleanup
close_connection_pool()
```

## 📊 Database Schema Highlights

### Core Tables
- **Division** & **Department**: Organizational hierarchy
- **Employee**: Supports both salaried and hourly employees
- **JobHistory**: Tracks all salary changes and promotions
- **PayrollHistory**: Maintains complete payroll records with tax breakdowns
- **Project**: Tracks projects with budgets and timelines
- **EmployeeProject**: Many-to-many relationship with role and hours tracking
- **ProjectMilestone**: Tracks project deliverables and progress

### Key Design Features
- ✅ **3NF Normalization**: No redundancy, proper functional dependencies
- ✅ **Referential Integrity**: Comprehensive foreign key constraints
- ✅ **Historical Tracking**: Preserves salary and project assignment history
- ✅ **Temporal Data**: Tracks current vs historical records with is_current flags
- ✅ **Database Triggers**: Ensures only one current job/project per employee
- ✅ **Check Constraints**: Validates tax calculations and business rules

## 📝 Key Reports and Queries

The applications support various reports:

### HR/Payroll Reports
- Current employee roster with salaries
- Salary history by employee
- Monthly payroll reports with tax breakdowns
- Annual W-2 style tax summaries
- Department payroll summaries

### Project Management Reports
- Active and completed projects list
- Project team compositions
- Person-hours per project
- Milestone status and completion rates
- Employee productivity reports
- Department project portfolios

## 🧪 Testing

The project includes:
- **Sample data generator**: Creates realistic test data
- **Demo script**: Comprehensive tests of all features
- **Validation**: Built-in checks for data integrity

Run tests:
```bash
# Generate fresh test data
python generate_sample_data.py

# Run comprehensive demo
python demo.py
```

## 📚 Documentation

Detailed documentation is available in the `/documentation` folder:

1. **ER_Design_and_Decisions.md**: 
   - Complete ER diagram specification
   - Design decisions and justifications
   - Business rules and constraints

2. **Relational_Schema.md**:
   - Formal relational schema  
   - Functional dependencies
   - Normalization verification
   - Sample queries

## 🎓 Academic Context

This project fulfills the requirements for CS631 Database Management Systems:

### Deliverables
- ✅ **ER Diagram**: Entities, attributes, relationships, cardinalities
- ✅ **Relational Schema**: Proper ER-to-relational mapping with keys
- ✅ **Database Implementation**: Working PostgreSQL database
- ✅ **Applications**: Two functional applications (HR & PM)
- ✅ **Documentation**: Design decisions and justifications

### What Makes This Design Strong
1. **Correct modeling**: Proper identification of entities and relationships
2. **Clean mapping**: ER diagram correctly converted to relational schema
3. **Proper keys**: Primary and foreign keys correctly identified
4. **Normalization**: Schema in 3NF with no anomalies
5. **Real-world applicability**: Supports actual business processes
6. **Justified decisions**: Every design choice is explained and defended

## 🔧 Customization

### Modifying Tax Rates

Edit `applications/hr_payroll_app.py`:
```python
self.TAX_RATES = {
    'federal': Decimal('0.10'),  # Change as needed
    'state': Decimal('0.05'),
    'other': Decimal('0.03')
}
```

### Adding New Features

The modular design makes it easy to extend:
- Add new methods to `HRPayrollApp` or `ProjectManagementApp` classes
- Create new tables in `schema.sql`
- Add new sample data in `generate_sample_data.py`

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
brew services list | grep postgresql  # macOS
systemctl status postgresql           # Linux

# Test connection
psql -h localhost -U your_username -d cs631_company_db
```

### Python Import Errors
```bash
# Ensure you're in the applications directory
cd CS631_Project/applications

# Run scripts from this directory
python demo.py
```

### "Role does not exist" Error
```bash
# Create PostgreSQL user
psql postgres
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER USER your_username CREATEDB;
\q
```

## 📄 License

This project is created for academic purposes as part of CS631 coursework.

## 👥 Authors

Created for CS631 Database Management Systems course.

## 🙏 Acknowledgments

- CS631 course staff for project requirements
- PostgreSQL documentation
- Python psycopg2 documentation

---

**Note**: This project demonstrates a complete database system from conceptual design (ER diagram) through implementation (working applications). It showcases proper database design principles, normalization, and real-world application development.
