# CS631 Company Personnel Database - Relational Schema

## RELATIONAL SCHEMA (Logical Database Design)

### 1. Division
```
Division(division_id, division_name, division_head_emp_id)
  PK: division_id
  FK: division_head_emp_id REFERENCES Employee(employee_number)
```

### 2. Department
```
Department(department_id, department_name, budget, department_head_emp_id, division_id)
  PK: department_id
  UNIQUE: department_name
  FK: department_head_emp_id REFERENCES Employee(employee_number)
  FK: division_id REFERENCES Division(division_id)
```

### 3. Employee
```
Employee(employee_number, employee_name, title, employment_type, hourly_rate, department_id, division_id)
  PK: employee_number
  FK: department_id REFERENCES Department(department_id) [NULLABLE]
  FK: division_id REFERENCES Division(division_id) [NULLABLE]
  CHECK: employment_type IN ('salaried', 'hourly')
  CHECK: (employment_type = 'hourly' AND hourly_rate IS NOT NULL) OR (employment_type = 'salaried' AND hourly_rate IS NULL)
  CHECK: (department_id IS NOT NULL) OR (division_id IS NOT NULL) OR (department_id IS NULL AND division_id IS NULL)
```

### 4. Building
```
Building(building_code, building_name, year_built_or_bought, cost)
  PK: building_code
```

### 5. Office
```
Office(office_number, area_sqft, building_code)
  PK: office_number
  FK: building_code REFERENCES Building(building_code)
```

### 6. Phone
```
Phone(phone_number, office_number, assigned_to_emp_id)
  PK: phone_number
  FK: office_number REFERENCES Office(office_number)
  FK: assigned_to_emp_id REFERENCES Employee(employee_number) [NULLABLE]
```

### 7. Project
```
Project(project_number, project_name, budget, date_started, date_ended, manager_emp_id, department_id)
  PK: project_number
  FK: manager_emp_id REFERENCES Employee(employee_number)
  FK: department_id REFERENCES Department(department_id)
```

### 8. EmployeeProject
```
EmployeeProject(employee_number, project_number, role, hours_worked, start_date, end_date, is_current)
  PK: (employee_number, project_number)
  FK: employee_number REFERENCES Employee(employee_number)
  FK: project_number REFERENCES Project(project_number)
  CHECK: Only one is_current = TRUE per employee (application-level enforcement)
```

### 9. JobHistory
```
JobHistory(job_history_id, employee_number, title, start_date, end_date, salary, is_current)
  PK: job_history_id
  FK: employee_number REFERENCES Employee(employee_number)
  CHECK: Only one is_current = TRUE per employee
```

### 10. PayrollHistory
```
PayrollHistory(payroll_id, employee_number, pay_period_start, pay_period_end, gross_pay, federal_tax, state_tax, other_tax, net_pay, payment_date)
  PK: payroll_id
  FK: employee_number REFERENCES Employee(employee_number)
  CHECK: federal_tax = gross_pay * 0.10
  CHECK: state_tax = gross_pay * 0.05
  CHECK: other_tax = gross_pay * 0.03
  CHECK: net_pay = gross_pay - federal_tax - state_tax - other_tax
```

### 11. ProjectMilestone
```
ProjectMilestone(milestone_id, project_number, milestone_name, description, due_date, completion_date, status, details_done, details_remaining)
  PK: milestone_id
  FK: project_number REFERENCES Project(project_number)
  CHECK: status IN ('pending', 'in_progress', 'completed')
```

### 12. EmployeeOffice
```
EmployeeOffice(employee_number, office_number, assignment_date)
  PK: (employee_number, office_number)
  FK: employee_number REFERENCES Employee(employee_number)
  FK: office_number REFERENCES Office(office_number)
```

---

## FUNCTIONAL DEPENDENCIES

### Division
- division_id → division_name, division_head_emp_id

### Department
- department_id → department_name, budget, department_head_emp_id, division_id
- department_name → department_id (UNIQUE constraint)

### Employee
- employee_number → employee_name, title, employment_type, hourly_rate, department_id, division_id

### Building
- building_code → building_name, year_built_or_bought, cost

### Office
- office_number → area_sqft, building_code

### Phone
- phone_number → office_number, assigned_to_emp_id

### Project
- project_number → project_name, budget, date_started, date_ended, manager_emp_id, department_id

### EmployeeProject
- (employee_number, project_number) → role, hours_worked, start_date, end_date, is_current

### JobHistory
- job_history_id → employee_number, title, start_date, end_date, salary, is_current

### PayrollHistory
- payroll_id → employee_number, pay_period_start, pay_period_end, gross_pay, federal_tax, state_tax, other_tax, net_pay, payment_date

### ProjectMilestone
- milestone_id → project_number, milestone_name, description, due_date, completion_date, status, details_done, details_remaining

### EmployeeOffice
- (employee_number, office_number) → assignment_date

---

## NORMALIZATION VERIFICATION

### All relations are in 3NF:

**1NF:** All attributes contain atomic values, no repeating groups exist.

**2NF:** All non-key attributes are fully functionally dependent on the primary key. No partial dependencies exist.

**3NF:** No transitive dependencies exist. All non-key attributes depend only on the primary key.

**Examples:**
- Employee's title is stored in Employee table, not derived from anywhere
- Salary information is in JobHistory (depends on job_history_id), not directly in Employee
- PayrollHistory stores calculated tax amounts (no derivable attributes in normal operations)
- EmployeeProject separates the many-to-many relationship properly

---

## REFERENTIAL INTEGRITY CONSTRAINTS

### ON DELETE and ON UPDATE Rules:

1. **Division.division_head_emp_id → Employee**
   - ON DELETE: RESTRICT (cannot delete employee who is division head)
   - ON UPDATE: CASCADE

2. **Department.department_head_emp_id → Employee**
   - ON DELETE: RESTRICT (cannot delete employee who is department head)
   - ON UPDATE: CASCADE

3. **Department.division_id → Division**
   - ON DELETE: RESTRICT (cannot delete division with departments)
   - ON UPDATE: CASCADE

4. **Employee.department_id → Department**
   - ON DELETE: SET NULL (if department deleted, employee can be reassigned)
   - ON UPDATE: CASCADE

5. **Employee.division_id → Division**
   - ON DELETE: SET NULL
   - ON UPDATE: CASCADE

6. **Office.building_code → Building**
   - ON DELETE: RESTRICT (cannot delete building with offices)
   - ON UPDATE: CASCADE

7. **Phone.office_number → Office**
   - ON DELETE: CASCADE (if office deleted, remove phones)
   - ON UPDATE: CASCADE

8. **Phone.assigned_to_emp_id → Employee**
   - ON DELETE: SET NULL (unassign phone if employee deleted)
   - ON UPDATE: CASCADE

9. **Project.manager_emp_id → Employee**
   - ON DELETE: RESTRICT (cannot delete employee who manages a project)
   - ON UPDATE: CASCADE

10. **Project.department_id → Department**
    - ON DELETE: RESTRICT (cannot delete department with projects)
    - ON UPDATE: CASCADE

11. **EmployeeProject.employee_number → Employee**
    - ON DELETE: CASCADE (remove project assignments if employee deleted)
    - ON UPDATE: CASCADE

12. **EmployeeProject.project_number → Project**
    - ON DELETE: CASCADE (remove assignments if project deleted)
    - ON UPDATE: CASCADE

13. **JobHistory.employee_number → Employee**
    - ON DELETE: CASCADE (remove job history if employee deleted)
    - ON UPDATE: CASCADE

14. **PayrollHistory.employee_number → Employee**
    - ON DELETE: CASCADE (remove payroll history if employee deleted)
    - ON UPDATE: CASCADE

15. **ProjectMilestone.project_number → Project**
    - ON DELETE: CASCADE (remove milestones if project deleted)
    - ON UPDATE: CASCADE

16. **EmployeeOffice.employee_number → Employee**
    - ON DELETE: CASCADE
    - ON UPDATE: CASCADE

17. **EmployeeOffice.office_number → Office**
    - ON DELETE: CASCADE
    - ON UPDATE: CASCADE

---

## INTEGRITY CONSTRAINTS

### Domain Constraints:
- employment_type ∈ {'salaried', 'hourly'}
- status ∈ {'pending', 'in_progress', 'completed'}
- All numeric values (budget, cost, salary, etc.) >= 0
- All dates must be valid dates
- hourly_rate > 0 when employment_type = 'hourly'

### Entity Constraints:
- All primary keys are NOT NULL and UNIQUE

### Referential Constraints:
- All foreign keys reference existing primary keys

### Business Rule Constraints:
1. An employee with employment_type = 'hourly' must have hourly_rate NOT NULL
2. An employee with employment_type = 'salaried' must have hourly_rate NULL
3. Only one JobHistory record per employee can have is_current = TRUE
4. Only one EmployeeProject record per employee can have is_current = TRUE
5. Tax calculations: federal_tax = 10%, state_tax = 5%, other_tax = 3%
6. net_pay = gross_pay - federal_tax - state_tax - other_tax
7. If project has date_ended, then completion_date must be <= date_ended for all milestones
8. An employee must belong to either a department OR a division (or neither, but not both at same time is flexible)

---

## INDEXES (for Performance Optimization)

### Primary Key Indexes (automatic):
- All primary keys automatically indexed

### Foreign Key Indexes (recommended):
```sql
CREATE INDEX idx_dept_division ON Department(division_id);
CREATE INDEX idx_emp_department ON Employee(department_id);
CREATE INDEX idx_emp_division ON Employee(division_id);
CREATE INDEX idx_office_building ON Office(building_code);
CREATE INDEX idx_phone_office ON Phone(office_number);
CREATE INDEX idx_phone_employee ON Phone(assigned_to_emp_id);
CREATE INDEX idx_project_manager ON Project(manager_emp_id);
CREATE INDEX idx_project_dept ON Project(department_id);
CREATE INDEX idx_emppro_employee ON EmployeeProject(employee_number);
CREATE INDEX idx_emppro_project ON EmployeeProject(project_number);
CREATE INDEX idx_jobhist_employee ON JobHistory(employee_number);
CREATE INDEX idx_payroll_employee ON PayrollHistory(employee_number);
CREATE INDEX idx_milestone_project ON ProjectMilestone(project_number);
```

### Additional Indexes for Common Queries:
```sql
CREATE INDEX idx_emp_name ON Employee(employee_name);
CREATE INDEX idx_dept_name ON Department(department_name);
CREATE INDEX idx_emppro_current ON EmployeeProject(is_current);
CREATE INDEX idx_jobhist_current ON JobHistory(is_current);
CREATE INDEX idx_payroll_period ON PayrollHistory(pay_period_start, pay_period_end);
CREATE INDEX idx_milestone_status ON ProjectMilestone(status);
```

---

## SAMPLE QUERIES

### 1. Get all employees in a department with their current salaries:
```sql
SELECT e.employee_number, e.employee_name, e.title, jh.salary
FROM Employee e
JOIN JobHistory jh ON e.employee_number = jh.employee_number
WHERE e.department_id = ? AND jh.is_current = TRUE;
```

### 2. Get current project assignments:
```sql
SELECT e.employee_name, p.project_name, ep.role, ep.hours_worked
FROM EmployeeProject ep
JOIN Employee e ON ep.employee_number = e.employee_number
JOIN Project p ON ep.project_number = p.project_number
WHERE ep.is_current = TRUE;
```

### 3. Calculate total person-hours per project:
```sql
SELECT p.project_number, p.project_name, SUM(ep.hours_worked) as total_hours
FROM Project p
LEFT JOIN EmployeeProject ep ON p.project_number = ep.project_number
GROUP BY p.project_number, p.project_name;
```

### 4. Get payroll for a specific period:
```sql
SELECT e.employee_number, e.employee_name, ph.gross_pay, ph.net_pay, 
       ph.federal_tax, ph.state_tax, ph.other_tax
FROM PayrollHistory ph
JOIN Employee e ON ph.employee_number = e.employee_number
WHERE ph.pay_period_start = ? AND ph.pay_period_end = ?;
```

### 5. Get project milestones with status:
```sql
SELECT pm.milestone_name, pm.status, pm.due_date, pm.completion_date,
       pm.details_done, pm.details_remaining
FROM ProjectMilestone pm
WHERE pm.project_number = ?
ORDER BY pm.due_date;
```

### 6. Find employees sharing an office:
```sql
SELECT o.office_number, e.employee_name, e.title
FROM EmployeeOffice eo
JOIN Office o ON eo.office_number = o.office_number
JOIN Employee e ON eo.employee_number = e.employee_number
ORDER BY o.office_number, e.employee_name;
```

### 7. Get organizational hierarchy:
```sql
SELECT d.department_name, div.division_name, 
       dh.employee_name as dept_head, divh.employee_name as division_head
FROM Department d
JOIN Division div ON d.division_id = div.division_id
LEFT JOIN Employee dh ON d.department_head_emp_id = dh.employee_number
LEFT JOIN Employee divh ON div.division_head_emp_id = divh.employee_number;
```

---

## CARDINALITY ESTIMATES (for test data)

Based on a medium-sized company:
- **Divisions**: 3-5
- **Departments**: 10-20 (2-4 per division)
- **Employees**: 50-100
- **Buildings**: 2-3
- **Offices**: 20-40
- **Phones**: 50-100 (one per employee + extras)
- **Projects**: 10-20
- **EmployeeProject records**: 100-200 (including historical)
- **JobHistory records**: 75-150 (1-3 per employee)
- **PayrollHistory records**: 1200-2400 (assuming 12-24 months of history)
- **ProjectMilestones**: 50-100 (3-5 per project)
- **EmployeeOffice records**: 50-100

---

## SCHEMA EVOLUTION CONSIDERATIONS

The schema is designed to be extensible:

1. **Adding new employee types**: Extend employment_type ENUM
2. **Adding new project statuses**: Extend status ENUM in relevant tables
3. **New attributes**: Can be added to existing tables without breaking existing code
4. **New entities**: Can reference existing tables via foreign keys
5. **Performance tuning**: Indexes can be added/modified without schema changes
6. **Partitioning**: PayrollHistory could be partitioned by year for better performance
7. **Archiving**: Old PayrollHistory and JobHistory records can be archived to separate tables
