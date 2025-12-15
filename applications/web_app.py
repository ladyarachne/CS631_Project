"""
Flask Web Application for HR/Payroll and Project Management
Minimal web interface demonstrating CRUD operations
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from database_config import initialize_connection_pool, close_connection_pool
from hr_payroll_app import HRPayrollApp
from project_management_app import ProjectManagementApp
from datetime import date, datetime
from decimal import Decimal
import atexit

app = Flask(__name__)
app.secret_key = 'cs631_demo_key_change_in_production'

# Initialize database connection pool on startup
initialize_connection_pool()

# Close connection pool on shutdown
atexit.register(close_connection_pool)

# Initialize app instances
hr_app = HRPayrollApp()
pm_app = ProjectManagementApp()


# ============================================================================
# HOME PAGE
# ============================================================================

@app.route('/')
def home():
    """Home page with links to HR and Project Management"""
    return render_template('home.html')


# ============================================================================
# HUMAN RESOURCE MANAGEMENT ROUTES
# ============================================================================

@app.route('/hr')
def hr_dashboard():
    """HR Dashboard with links to all HR functions"""
    return render_template('hr_dashboard.html')


@app.route('/hr/add_employee', methods=['GET', 'POST'])
def add_employee():
    """Add a new employee (CREATE)"""
    if request.method == 'POST':
        try:
            # Get form data
            emp_number = int(request.form['employee_number'])
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            name = f"{first_name} {last_name}"
            employment_type = request.form['employment_type']
            dept_id = int(request.form['department_id'])
            title = request.form['title']
            
            # Handle salary/hourly rate
            if employment_type == 'salaried':
                salary = Decimal(request.form['salary'])
            else:
                salary = Decimal(request.form['hourly_rate'])
            
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            
            # Add employee
            hr_app.add_employee(emp_number, name, title, employment_type, dept_id)
            
            # Add job history
            hr_app.add_job_history(emp_number, title, start_date, salary, is_current=True)
            
            flash(f'Successfully added employee {name} (ID: {emp_number})', 'success')
            return redirect(url_for('view_employees'))
            
        except Exception as e:
            flash(f'Error adding employee: {str(e)}', 'error')
            return redirect(url_for('add_employee'))
    
    return render_template('add_employee.html')


@app.route('/hr/employees')
def view_employees():
    """View all employees (READ)"""
    try:
        employees = hr_app.list_all_employees()
        return render_template('view_employees.html', employees=employees)
    except Exception as e:
        flash(f'Error loading employees: {str(e)}', 'error')
        return render_template('view_employees.html', employees=[])


@app.route('/hr/promote', methods=['GET', 'POST'])
def promote_employee():
    """Promote an employee (UPDATE)"""
    if request.method == 'POST':
        try:
            emp_number = int(request.form['employee_number'])
            new_title = request.form['new_title']
            new_salary = Decimal(request.form['new_salary'])
            effective_date = datetime.strptime(request.form['effective_date'], '%Y-%m-%d').date()
            
            hr_app.update_employee_title(emp_number, new_title, new_salary, effective_date)
            
            flash(f'Successfully promoted employee {emp_number}', 'success')
            return redirect(url_for('view_employees'))
            
        except Exception as e:
            flash(f'Error promoting employee: {str(e)}', 'error')
            return redirect(url_for('promote_employee'))
    
    return render_template('promote_employee.html')


@app.route('/hr/payroll', methods=['GET', 'POST'])
def payroll_report():
    """View and process payroll (READ)"""
    if request.method == 'POST':
        try:
            year = int(request.form['year'])
            month = int(request.form['month'])
            
            # Create date range for the month
            pay_start = date(year, month, 1)
            if month == 12:
                pay_end = date(year, 12, 31)
            else:
                pay_end = date(year, month + 1, 1)
                pay_end = date(pay_end.year, pay_end.month, 1)
                from datetime import timedelta
                pay_end = pay_end - timedelta(days=1)
            
            # Process payroll
            payment_date = pay_end
            hr_app.process_payroll(pay_start, pay_end, payment_date)
            
            # Get payroll report
            payroll_data = hr_app.get_payroll_report(pay_start, pay_end)
            
            return render_template('payroll_report.html', 
                                 payroll_data=payroll_data,
                                 month=month,
                                 year=year,
                                 processed=True)
        except Exception as e:
            flash(f'Error processing payroll: {str(e)}', 'error')
            return render_template('payroll_report.html', payroll_data=[], processed=False)
    
    return render_template('payroll_report.html', payroll_data=[], processed=False)


# ============================================================================
# PROJECT MANAGEMENT ROUTES
# ============================================================================

@app.route('/projects')
def project_dashboard():
    """Project Management Dashboard"""
    return render_template('project_dashboard.html')


@app.route('/projects/create', methods=['GET', 'POST'])
def create_project():
    """Create a new project (CREATE)"""
    if request.method == 'POST':
        try:
            proj_number = int(request.form['project_number'])
            proj_name = request.form['project_name']
            budget = Decimal(request.form['budget'])
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            manager_id = int(request.form['manager_id'])
            dept_id = int(request.form['department_id'])
            
            pm_app.create_project(proj_number, proj_name, budget, start_date, manager_id, dept_id)
            
            flash(f'Successfully created project: {proj_name}', 'success')
            return redirect(url_for('view_projects'))
            
        except Exception as e:
            flash(f'Error creating project: {str(e)}', 'error')
            return redirect(url_for('create_project'))
    
    return render_template('create_project.html')


@app.route('/projects/list')
def view_projects():
    """View all projects (READ)"""
    try:
        projects = pm_app.list_all_projects()
        return render_template('view_projects.html', projects=projects)
    except Exception as e:
        flash(f'Error loading projects: {str(e)}', 'error')
        return render_template('view_projects.html', projects=[])


@app.route('/projects/assign', methods=['GET', 'POST'])
def assign_employee():
    """Assign employee to project (CREATE)"""
    if request.method == 'POST':
        try:
            emp_id = int(request.form['employee_id'])
            proj_number = int(request.form['project_number'])
            role = request.form['role']
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            
            pm_app.assign_employee_to_project(emp_id, proj_number, role, start_date, 0, True)
            
            flash(f'Successfully assigned employee {emp_id} to project {proj_number}', 'success')
            return redirect(url_for('view_projects'))
            
        except Exception as e:
            flash(f'Error assigning employee: {str(e)}', 'error')
            return redirect(url_for('assign_employee'))
    
    return render_template('assign_employee.html')


@app.route('/projects/hours', methods=['GET', 'POST'])
def update_hours():
    """Update project hours (UPDATE)"""
    if request.method == 'POST':
        try:
            emp_id = int(request.form['employee_id'])
            proj_number = int(request.form['project_number'])
            hours = Decimal(request.form['hours'])
            
            pm_app.update_employee_project_hours(emp_id, proj_number, hours)
            
            flash(f'Successfully updated hours for employee {emp_id}', 'success')
            return redirect(url_for('view_projects'))
            
        except Exception as e:
            flash(f'Error updating hours: {str(e)}', 'error')
            return redirect(url_for('update_hours'))
    
    return render_template('update_hours.html')


@app.route('/projects/complete_milestone', methods=['GET', 'POST'])
def complete_milestone():
    """Complete a milestone (UPDATE/DEACTIVATE)"""
    if request.method == 'POST':
        try:
            milestone_id = int(request.form['milestone_id'])
            completion_date = datetime.strptime(request.form['completion_date'], '%Y-%m-%d').date()
            
            pm_app.complete_milestone(milestone_id, completion_date)
            
            flash(f'Successfully completed milestone {milestone_id}', 'success')
            return redirect(url_for('view_projects'))
            
        except Exception as e:
            flash(f'Error completing milestone: {str(e)}', 'error')
            return redirect(url_for('complete_milestone'))
    
    # Get list of pending milestones
    try:
        from database_config import get_db_cursor
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT milestone_id, project_number, milestone_name, status
                FROM ProjectMilestone
                WHERE status IN ('pending', 'in_progress')
                ORDER BY project_number, milestone_id
            """)
            milestones = cursor.fetchall()
    except:
        milestones = []
    
    return render_template('complete_milestone.html', milestones=milestones)


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("CS631 Company Database - Web Application")
    print("="*70)
    print("\nStarting Flask server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress CTRL+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
