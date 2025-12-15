-- ================================================================
-- CS631 Company Personnel Database - SQL DDL Schema
-- Database Management System: PostgreSQL
-- ================================================================

-- Drop existing tables (in reverse order of dependencies)
DROP TABLE IF EXISTS EmployeeOffice CASCADE;
DROP TABLE IF EXISTS ProjectMilestone CASCADE;
DROP TABLE IF EXISTS PayrollHistory CASCADE;
DROP TABLE IF EXISTS JobHistory CASCADE;
DROP TABLE IF EXISTS EmployeeProject CASCADE;
DROP TABLE IF EXISTS Project CASCADE;
DROP TABLE IF EXISTS Phone CASCADE;
DROP TABLE IF EXISTS Office CASCADE;
DROP TABLE IF EXISTS Building CASCADE;
DROP TABLE IF EXISTS Employee CASCADE;
DROP TABLE IF EXISTS Department CASCADE;
DROP TABLE IF EXISTS Division CASCADE;

-- ================================================================
-- CREATE TABLES
-- ================================================================

-- Division Table
CREATE TABLE Division (
    division_id SERIAL PRIMARY KEY,
    division_name VARCHAR(100) NOT NULL,
    division_head_emp_id INTEGER
);

-- Department Table
CREATE TABLE Department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    budget DECIMAL(15, 2) CHECK (budget >= 0),
    department_head_emp_id INTEGER,
    division_id INTEGER NOT NULL,
    FOREIGN KEY (division_id) REFERENCES Division(division_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Employee Table
CREATE TABLE Employee (
    employee_number INTEGER PRIMARY KEY,
    employee_name VARCHAR(200) NOT NULL,
    title VARCHAR(100) NOT NULL,
    employment_type VARCHAR(20) NOT NULL CHECK (employment_type IN ('salaried', 'hourly')),
    hourly_rate DECIMAL(10, 2) CHECK (hourly_rate > 0),
    department_id INTEGER,
    division_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (division_id) REFERENCES Division(division_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CHECK (
        (employment_type = 'hourly' AND hourly_rate IS NOT NULL) OR
        (employment_type = 'salaried' AND hourly_rate IS NULL)
    )
);

-- Add foreign key constraints for division and department heads
ALTER TABLE Division
    ADD FOREIGN KEY (division_head_emp_id) REFERENCES Employee(employee_number)
        ON UPDATE CASCADE
        ON DELETE RESTRICT;

ALTER TABLE Department
    ADD FOREIGN KEY (department_head_emp_id) REFERENCES Employee(employee_number)
        ON UPDATE CASCADE
        ON DELETE RESTRICT;

-- Building Table
CREATE TABLE Building (
    building_code VARCHAR(10) PRIMARY KEY,
    building_name VARCHAR(100) NOT NULL,
    year_built_or_bought INTEGER CHECK (year_built_or_bought > 1800 AND year_built_or_bought <= EXTRACT(YEAR FROM CURRENT_DATE)),
    cost DECIMAL(15, 2) CHECK (cost >= 0)
);

-- Office Table
CREATE TABLE Office (
    office_number VARCHAR(20) PRIMARY KEY,
    area_sqft DECIMAL(10, 2) CHECK (area_sqft > 0),
    building_code VARCHAR(10) NOT NULL,
    FOREIGN KEY (building_code) REFERENCES Building(building_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Phone Table
CREATE TABLE Phone (
    phone_number VARCHAR(20) PRIMARY KEY,
    office_number VARCHAR(20) NOT NULL,
    assigned_to_emp_id INTEGER,
    FOREIGN KEY (office_number) REFERENCES Office(office_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (assigned_to_emp_id) REFERENCES Employee(employee_number)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Project Table
CREATE TABLE Project (
    project_number INTEGER PRIMARY KEY,
    project_name VARCHAR(200) NOT NULL,
    budget DECIMAL(15, 2) CHECK (budget >= 0),
    date_started DATE NOT NULL,
    date_ended DATE,
    manager_emp_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (manager_emp_id) REFERENCES Employee(employee_number)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CHECK (date_ended IS NULL OR date_ended >= date_started)
);

-- EmployeeProject Table (Many-to-Many relationship with attributes)
CREATE TABLE EmployeeProject (
    employee_number INTEGER,
    project_number INTEGER,
    role VARCHAR(100) NOT NULL,
    hours_worked DECIMAL(10, 2) DEFAULT 0 CHECK (hours_worked >= 0),
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (employee_number, project_number),
    FOREIGN KEY (employee_number) REFERENCES Employee(employee_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (project_number) REFERENCES Project(project_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CHECK (end_date IS NULL OR end_date >= start_date)
);

-- JobHistory Table
CREATE TABLE JobHistory (
    job_history_id SERIAL PRIMARY KEY,
    employee_number INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    salary DECIMAL(12, 2) NOT NULL CHECK (salary > 0),
    is_current BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (employee_number) REFERENCES Employee(employee_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CHECK (end_date IS NULL OR end_date >= start_date)
);

-- PayrollHistory Table
CREATE TABLE PayrollHistory (
    payroll_id SERIAL PRIMARY KEY,
    employee_number INTEGER NOT NULL,
    pay_period_start DATE NOT NULL,
    pay_period_end DATE NOT NULL,
    gross_pay DECIMAL(12, 2) NOT NULL CHECK (gross_pay >= 0),
    federal_tax DECIMAL(12, 2) NOT NULL CHECK (federal_tax >= 0),
    state_tax DECIMAL(12, 2) NOT NULL CHECK (state_tax >= 0),
    other_tax DECIMAL(12, 2) NOT NULL CHECK (other_tax >= 0),
    net_pay DECIMAL(12, 2) NOT NULL CHECK (net_pay >= 0),
    payment_date DATE NOT NULL,
    FOREIGN KEY (employee_number) REFERENCES Employee(employee_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CHECK (pay_period_end >= pay_period_start),
    CHECK (federal_tax = ROUND(gross_pay * 0.10, 2)),
    CHECK (state_tax = ROUND(gross_pay * 0.05, 2)),
    CHECK (other_tax = ROUND(gross_pay * 0.03, 2)),
    CHECK (net_pay = gross_pay - federal_tax - state_tax - other_tax)
);

-- ProjectMilestone Table
CREATE TABLE ProjectMilestone (
    milestone_id SERIAL PRIMARY KEY,
    project_number INTEGER NOT NULL,
    milestone_name VARCHAR(200) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    completion_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'in_progress', 'completed')),
    details_done TEXT,
    details_remaining TEXT,
    FOREIGN KEY (project_number) REFERENCES Project(project_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- EmployeeOffice Table (Many-to-Many relationship)
CREATE TABLE EmployeeOffice (
    employee_number INTEGER,
    office_number VARCHAR(20),
    assignment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (employee_number, office_number),
    FOREIGN KEY (employee_number) REFERENCES Employee(employee_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (office_number) REFERENCES Office(office_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ================================================================
-- CREATE INDEXES
-- ================================================================

-- Foreign Key Indexes
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

-- Additional Indexes for Common Queries
CREATE INDEX idx_emp_name ON Employee(employee_name);
CREATE INDEX idx_dept_name ON Department(department_name);
CREATE INDEX idx_emppro_current ON EmployeeProject(is_current) WHERE is_current = TRUE;
CREATE INDEX idx_jobhist_current ON JobHistory(is_current) WHERE is_current = TRUE;
CREATE INDEX idx_payroll_period ON PayrollHistory(pay_period_start, pay_period_end);
CREATE INDEX idx_milestone_status ON ProjectMilestone(status);
CREATE INDEX idx_project_dates ON Project(date_started, date_ended);

-- ================================================================
-- CREATE VIEWS (for convenience)
-- ================================================================

-- View: Current Employee Information with Salary
CREATE OR REPLACE VIEW v_current_employees AS
SELECT 
    e.employee_number,
    e.employee_name,
    e.title,
    e.employment_type,
    e.hourly_rate,
    jh.salary AS current_salary,
    d.department_name,
    div.division_name
FROM Employee e
LEFT JOIN JobHistory jh ON e.employee_number = jh.employee_number AND jh.is_current = TRUE
LEFT JOIN Department d ON e.department_id = d.department_id
LEFT JOIN Division div ON e.division_id = div.division_id;

-- View: Current Project Assignments
CREATE OR REPLACE VIEW v_current_project_assignments AS
SELECT 
    e.employee_number,
    e.employee_name,
    p.project_number,
    p.project_name,
    ep.role,
    ep.hours_worked,
    ep.start_date
FROM EmployeeProject ep
JOIN Employee e ON ep.employee_number = e.employee_number
JOIN Project p ON ep.project_number = p.project_number
WHERE ep.is_current = TRUE;

-- View: Project Statistics
CREATE OR REPLACE VIEW v_project_statistics AS
SELECT 
    p.project_number,
    p.project_name,
    p.budget,
    p.date_started,
    p.date_ended,
    m.employee_name AS manager_name,
    d.department_name,
    COUNT(DISTINCT ep.employee_number) AS team_size,
    SUM(ep.hours_worked) AS total_person_hours,
    COUNT(pm.milestone_id) AS total_milestones,
    COUNT(CASE WHEN pm.status = 'completed' THEN 1 END) AS completed_milestones
FROM Project p
JOIN Employee m ON p.manager_emp_id = m.employee_number
JOIN Department d ON p.department_id = d.department_id
LEFT JOIN EmployeeProject ep ON p.project_number = ep.project_number
LEFT JOIN ProjectMilestone pm ON p.project_number = pm.project_number
GROUP BY p.project_number, p.project_name, p.budget, p.date_started, 
         p.date_ended, m.employee_name, d.department_name;

-- View: Office Assignments
CREATE OR REPLACE VIEW v_office_assignments AS
SELECT 
    o.office_number,
    o.area_sqft,
    b.building_name,
    b.building_code,
    e.employee_number,
    e.employee_name,
    e.title,
    p.phone_number
FROM Office o
JOIN Building b ON o.building_code = b.building_code
LEFT JOIN EmployeeOffice eo ON o.office_number = eo.office_number
LEFT JOIN Employee e ON eo.employee_number = e.employee_number
LEFT JOIN Phone p ON o.office_number = p.office_number AND p.assigned_to_emp_id = e.employee_number;

-- ================================================================
-- FUNCTIONS AND TRIGGERS
-- ================================================================

-- Function: Ensure only one current job per employee
CREATE OR REPLACE FUNCTION check_current_job()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_current = TRUE THEN
        UPDATE JobHistory 
        SET is_current = FALSE 
        WHERE employee_number = NEW.employee_number 
          AND job_history_id != NEW.job_history_id
          AND is_current = TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_current_job
BEFORE INSERT OR UPDATE ON JobHistory
FOR EACH ROW
EXECUTE FUNCTION check_current_job();

-- Function: Ensure only one current project per employee
CREATE OR REPLACE FUNCTION check_current_project()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_current = TRUE THEN
        UPDATE EmployeeProject 
        SET is_current = FALSE 
        WHERE employee_number = NEW.employee_number 
          AND (employee_number != NEW.employee_number OR project_number != NEW.project_number)
          AND is_current = TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_current_project
BEFORE INSERT OR UPDATE ON EmployeeProject
FOR EACH ROW
EXECUTE FUNCTION check_current_project();

-- Function: Auto-update milestone status to completed when completion_date is set
CREATE OR REPLACE FUNCTION update_milestone_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.completion_date IS NOT NULL AND OLD.completion_date IS NULL THEN
        NEW.status := 'completed';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_milestone_status
BEFORE UPDATE ON ProjectMilestone
FOR EACH ROW
EXECUTE FUNCTION update_milestone_status();

-- ================================================================
-- GRANT PERMISSIONS (adjust as needed for your environment)
-- ================================================================

-- These commands assume you have different roles for different applications
-- Comment out or modify based on your actual user setup

-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO hr_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO pm_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO hr_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO pm_app_user;

-- ================================================================
-- COMMENTS (for documentation)
-- ================================================================

COMMENT ON TABLE Division IS 'Organizational divisions within the company';
COMMENT ON TABLE Department IS 'Departments within divisions';
COMMENT ON TABLE Employee IS 'All company employees (salaried and hourly)';
COMMENT ON TABLE Building IS 'Company buildings';
COMMENT ON TABLE Office IS 'Office spaces within buildings';
COMMENT ON TABLE Phone IS 'Phone numbers assigned to offices and employees';
COMMENT ON TABLE Project IS 'Company projects managed by departments';
COMMENT ON TABLE EmployeeProject IS 'Employee assignments to projects with role and hours';
COMMENT ON TABLE JobHistory IS 'Historical record of employee job titles and salaries';
COMMENT ON TABLE PayrollHistory IS 'Historical payroll records for tax reporting';
COMMENT ON TABLE ProjectMilestone IS 'Project milestones and deliverables';
COMMENT ON TABLE EmployeeOffice IS 'Office assignments for employees (many-to-many)';

-- ================================================================
-- END OF SCHEMA
-- ================================================================

COMMIT;
