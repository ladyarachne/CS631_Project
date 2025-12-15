# CS631 Company Personnel Database - ER Design and Design Decisions

## 1. ENTITY-RELATIONSHIP DESIGN

### 1.1 Entities and Attributes

#### **Division**
- division_id (PK)
- division_name
- division_head_emp_id (FK to Employee)

#### **Department**
- department_id (PK)
- department_name (UNIQUE)
- budget
- department_head_emp_id (FK to Employee)
- division_id (FK to Division)

#### **Employee**
- employee_number (PK)
- employee_name
- title
- employment_type (ENUM: 'salaried', 'hourly')
- hourly_rate (nullable - for hourly employees)
- department_id (FK to Department, nullable)
- division_id (FK to Division, nullable)

#### **Building**
- building_code (PK)
- building_name
- year_built_or_bought
- cost

#### **Office**
- office_number (PK)
- area_sqft
- building_code (FK to Building)

#### **Phone**
- phone_number (PK)
- office_number (FK to Office)
- assigned_to_emp_id (FK to Employee, nullable)

#### **Project**
- project_number (PK)
- project_name
- budget
- date_started
- date_ended (nullable)
- manager_emp_id (FK to Employee)
- department_id (FK to Department)

#### **EmployeeProject** (Relationship Entity)
- employee_number (PK, FK to Employee)
- project_number (PK, FK to Project)
- role
- hours_worked
- start_date
- end_date (nullable)
- is_current (BOOLEAN)

#### **JobHistory**
- job_history_id (PK)
- employee_number (FK to Employee)
- title
- start_date
- end_date (nullable)
- salary
- is_current (BOOLEAN)

#### **PayrollHistory**
- payroll_id (PK)
- employee_number (FK to Employee)
- pay_period_start
- pay_period_end
- gross_pay
- federal_tax (10%)
- state_tax (5%)
- other_tax (3%)
- net_pay
- payment_date

#### **ProjectMilestone**
- milestone_id (PK)
- project_number (FK to Project)
- milestone_name
- description
- due_date
- completion_date (nullable)
- status (ENUM: 'pending', 'in_progress', 'completed')
- details_done
- details_remaining

#### **EmployeeOffice** (Relationship Entity for many-to-many)
- employee_number (PK, FK to Employee)
- office_number (PK, FK to Office)
- assignment_date

---

## 2. MAJOR DESIGN DECISIONS

### Decision 1: Separating Employee Types
**Problem:** The company has both salaried and hourly employees with different payment structures.

**Decision:** Use a single Employee table with an `employment_type` discriminator and an optional `hourly_rate` field.

**Justification:**
- Maintains referential integrity across all relationships
- Simplifies queries that need to access all employees regardless of type
- Avoids complex union operations
- The hourly_rate field is nullable for salaried employees
- Easy to extend with additional employee types in the future

### Decision 2: Employee-Project Relationship
**Problem:** Track current and historical project assignments with roles and hours.

**Decision:** Create an EmployeeProject associative entity with temporal tracking.

**Justification:**
- Supports the requirement to track all projects an employee has worked on
- Stores role, hours, and time period for each assignment
- The `is_current` flag enables quick queries for active assignments
- Enforces the constraint that an employee can work on only 1 project at a time (application-level enforcement)
- Historical data is preserved when employees switch projects

### Decision 3: Job History and Salary Tracking
**Problem:** Need to track all job titles and salaries an employee has held over time.

**Decision:** Create a separate JobHistory table with temporal data.

**Justification:**
- Supports IRS reporting requirements for historical salary data
- Allows tracking of promotions and salary changes
- Maintains audit trail for compliance
- Separate from Employee table to avoid redundancy and maintain 3NF
- `is_current` flag identifies the current position

### Decision 4: Payroll History
**Problem:** Need to maintain complete payroll records for tax reporting.

**Decision:** Create a dedicated PayrollHistory table storing each pay period's details.

**Justification:**
- IRS requires detailed records of all payments and withholdings
- Supports monthly payroll processing for both salaried and hourly employees
- Pre-calculated tax amounts (10%, 5%, 3%) stored for historical accuracy
- Enables year-end reporting and W-2 generation
- Immutable records for audit compliance

### Decision 5: Division-Department Hierarchy
**Problem:** Complex organizational structure with divisions containing departments.

**Decision:** Department references Division; employees can belong to either.

**Justification:**
- Accurately models the organizational hierarchy
- Allows department-level operations while maintaining division context
- Supports employees who work at division level without department affiliation (nullable department_id)
- Division and department heads maintain their department affiliations as required

### Decision 6: Office and Phone Assignment
**Problem:** Multiple employees can share offices; each needs their own phone.

**Decision:** 
- EmployeeOffice: Many-to-many relationship between Employee and Office
- Phone: Each phone belongs to an office and is optionally assigned to one employee

**Justification:**
- Flexible office sharing arrangements
- One phone per employee in shared offices
- Tracks which phones are available vs. assigned
- Office can have unassigned phones (for guests, conference calls, etc.)
- Easy to reassign phones when employees move

### Decision 7: Project Milestones
**Problem:** Need to track project progress and deliverables.

**Decision:** Create ProjectMilestone entity with status tracking and details fields.

**Justification:**
- Supports project management application requirements
- Tracks what's done and what remains
- Status field enables progress reporting
- Due date and completion date support schedule tracking
- Detailed description fields provide project transparency

### Decision 8: Building-Office Relationship
**Problem:** Offices are located in buildings; need to track building information.

**Decision:** Office references Building; Building has comprehensive attributes.

**Justification:**
- Supports asset management and space planning
- Building cost and construction year useful for facilities management
- Building code serves as natural identifier
- Can report office distribution across buildings
- Supports future requirements (maintenance, depreciation, etc.)

### Decision 9: Primary Key Choices
**Decisions:**
- Natural keys: department_name (UNIQUE), building_code, office_number, phone_number, employee_number, project_number
- Surrogate keys: division_id, job_history_id, payroll_id, milestone_id

**Justification:**
- Natural keys used when they exist and are stable (employee_number, project_number)
- Surrogate keys used for entities that lack natural identifiers (Division)
- Historical records (JobHistory, PayrollHistory) use surrogate keys for immutability
- department_name is UNIQUE but we use surrogate key for flexibility

### Decision 10: Referential Integrity and Constraints
**Decision:** Implement comprehensive foreign key constraints with appropriate cascade rules.

**Justification:**
- Prevents orphaned records
- Maintains data consistency
- Most deletes restricted (prevent data loss)
- Some updates cascade (e.g., changing employee numbers)
- Critical business rules enforced at database level

---

## 3. NORMALIZATION

The schema is designed to be in **Third Normal Form (3NF)**:

### 1NF (First Normal Form):
- All attributes contain atomic values
- No repeating groups
- Each table has a primary key

### 2NF (Second Normal Form):
- All non-key attributes fully depend on the primary key
- No partial dependencies on composite keys
- Example: In EmployeeProject, both employee_number and project_number are needed to determine role and hours

### 3NF (Third Normal Form):
- No transitive dependencies
- JobHistory separated from Employee (salary depends on job, not just employee)
- PayrollHistory separated to eliminate calculation redundancy
- Office and Phone are separate entities

---

## 4. RELATIONSHIPS

### One-to-Many:
- Division → Department (one division has many departments)
- Department → Employee (one department has many employees)
- Division → Employee (some employees work directly for division)
- Department → Project (one department oversees many projects)
- Building → Office (one building contains many offices)
- Office → Phone (one office has many phones)
- Employee → Phone (one employee assigned to one phone)
- Project → EmployeeProject (one project has many employee assignments)
- Employee → EmployeeProject (one employee has worked on many projects)
- Employee → JobHistory (one employee has multiple job records)
- Employee → PayrollHistory (one employee has many payroll records)
- Project → ProjectMilestone (one project has many milestones)

### Many-to-Many:
- Employee ↔ Office (through EmployeeOffice table)
- Employee ↔ Project (through EmployeeProject table)

### Self-Referencing:
- Department has department_head (Employee)
- Division has division_head (Employee)
- Project has manager (Employee)

---

## 5. BUSINESS RULES ENFORCED

1. **Each department must belong to exactly one division**
2. **Each department has exactly one department head (employee)**
3. **Each division has exactly one division head (employee)**
4. **An employee can work for a department OR directly for a division**
5. **Each project has exactly one manager**
6. **An employee can work on only 1 project at a time** (enforced by application logic using is_current flag)
7. **Each phone in an office is assigned to at most one employee**
8. **Tax percentages are fixed: 10% federal, 5% state, 3% other**
9. **Employment type is either 'salaried' or 'hourly'**
10. **Hourly employees must have an hourly_rate; salaried employees do not**

---

## 6. EXTENSIONS FOR APPLICATION REQUIREMENTS

### HR/Payroll Application:
- PayrollHistory table tracks all payments and taxes
- JobHistory maintains salary history for IRS reporting
- employment_type distinguishes salaried vs hourly employees
- Calculation rules embedded in application layer

### Project Management Application:
- EmployeeProject tracks team composition and person-hours
- ProjectMilestone tracks deliverables and progress
- Statistics can be computed from aggregating EmployeeProject data
- status field enables progress reporting

---

## 7. ASSUMPTIONS AND CLARIFICATIONS

1. **Employee numbers**: Assumed to be unique identifiers assigned by company
2. **Project numbers**: Assumed to be unique identifiers
3. **Department names**: Must be unique across the entire company
4. **Office numbers**: Unique across all buildings (could be changed to building_code + office_number if needed)
5. **Phone numbers**: Assumed to include extensions or full numbers
6. **Dates**: Projects can have NULL end_date if ongoing
7. **Historical data**: Never deleted, only marked as non-current
8. **Payroll frequency**: Monthly (as specified in requirements)
9. **Project assignment**: Application enforces one current project per employee
10. **Department/Division heads**: Must be employees with department affiliations

---

## 8. FUTURE ENHANCEMENTS

Potential extensions not in current scope:
- Employee benefits and insurance
- Time-off and vacation tracking
- Performance reviews
- Equipment and asset assignment
- Training and certifications
- Conference room booking system
- Building maintenance records
- Multi-currency support for international operations
