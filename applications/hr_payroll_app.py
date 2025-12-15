"""
HR/Payroll Application
Handles employee management, salary tracking, and payroll processing
"""
from database_config import get_db_cursor
from datetime import datetime, timedelta
from decimal import Decimal
import sys

class HRPayrollApp:
    """HR and Payroll Management Application"""
    
    def __init__(self):
        self.TAX_RATES = {
            'federal': Decimal('0.10'),
            'state': Decimal('0.05'),
            'other': Decimal('0.03')
        }
    
    # ==================== EMPLOYEE MANAGEMENT ====================
    
    def add_employee(self, employee_number, name, title, employment_type, 
                     department_id=None, division_id=None, hourly_rate=None):
        """Add a new employee to the system"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Employee 
                    (employee_number, employee_name, title, employment_type, 
                     hourly_rate, department_id, division_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING employee_number
                """, (employee_number, name, title, employment_type, 
                      hourly_rate, department_id, division_id))
                
                emp_id = cursor.fetchone()[0]
                print(f"✓ Employee {emp_id} ({name}) added successfully")
                return emp_id
        except Exception as e:
            print(f"✗ Error adding employee: {e}")
            return None
    
    def add_job_history(self, employee_number, title, start_date, salary, 
                       end_date=None, is_current=True):
        """Add job history record for an employee"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO JobHistory 
                    (employee_number, title, start_date, end_date, salary, is_current)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING job_history_id
                """, (employee_number, title, start_date, end_date, salary, is_current))
                
                job_id = cursor.fetchone()[0]
                print(f"✓ Job history record {job_id} created for employee {employee_number}")
                return job_id
        except Exception as e:
            print(f"✗ Error adding job history: {e}")
            return None
    
    def update_employee_title(self, employee_number, new_title, new_salary, effective_date):
        """Update employee title and create new job history record"""
        try:
            with get_db_cursor() as cursor:
                # End current job history
                cursor.execute("""
                    UPDATE JobHistory 
                    SET end_date = %s, is_current = FALSE
                    WHERE employee_number = %s AND is_current = TRUE
                """, (effective_date, employee_number))
                
                # Update employee title
                cursor.execute("""
                    UPDATE Employee 
                    SET title = %s
                    WHERE employee_number = %s
                """, (new_title, employee_number))
                
                # Create new job history record
                cursor.execute("""
                    INSERT INTO JobHistory 
                    (employee_number, title, start_date, salary, is_current)
                    VALUES (%s, %s, %s, %s, TRUE)
                    RETURNING job_history_id
                """, (employee_number, new_title, effective_date, new_salary))
                
                job_id = cursor.fetchone()[0]
                print(f"✓ Employee {employee_number} promoted to {new_title}")
                print(f"  New salary: ${new_salary:,.2f}")
                return job_id
        except Exception as e:
            print(f"✗ Error updating employee title: {e}")
            return None
    
    def get_employee_info(self, employee_number):
        """Get detailed employee information"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.employee_number,
                        e.employee_name,
                        e.title,
                        e.employment_type,
                        e.hourly_rate,
                        jh.salary AS current_salary,
                        d.department_name,
                        div.division_name,
                        jh.start_date AS current_job_start
                    FROM Employee e
                    LEFT JOIN JobHistory jh ON e.employee_number = jh.employee_number 
                        AND jh.is_current = TRUE
                    LEFT JOIN Department d ON e.department_id = d.department_id
                    LEFT JOIN Division div ON e.division_id = div.division_id
                    WHERE e.employee_number = %s
                """, (employee_number,))
                
                result = cursor.fetchone()
                if result:
                    return {
                        'employee_number': result[0],
                        'name': result[1],
                        'title': result[2],
                        'employment_type': result[3],
                        'hourly_rate': result[4],
                        'current_salary': result[5],
                        'department': result[6],
                        'division': result[7],
                        'current_job_start': result[8]
                    }
                return None
        except Exception as e:
            print(f"✗ Error getting employee info: {e}")
            return None
    
    def list_all_employees(self):
        """List all employees with current information"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.employee_number,
                        e.employee_name,
                        e.title,
                        e.employment_type,
                        COALESCE(jh.salary, 0) AS salary,
                        COALESCE(e.hourly_rate, 0) AS hourly_rate,
                        COALESCE(d.department_name, div.division_name, 'Unassigned') AS org_unit
                    FROM Employee e
                    LEFT JOIN JobHistory jh ON e.employee_number = jh.employee_number 
                        AND jh.is_current = TRUE
                    LEFT JOIN Department d ON e.department_id = d.department_id
                    LEFT JOIN Division div ON e.division_id = div.division_id
                    ORDER BY e.employee_number
                """)
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error listing employees: {e}")
            return []
    
    def get_employee_salary_history(self, employee_number):
        """Get complete salary history for an employee"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        job_history_id,
                        title,
                        salary,
                        start_date,
                        end_date,
                        is_current
                    FROM JobHistory
                    WHERE employee_number = %s
                    ORDER BY start_date DESC
                """, (employee_number,))
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error getting salary history: {e}")
            return []
    
    # ==================== PAYROLL PROCESSING ====================
    
    def calculate_salaried_pay(self, annual_salary):
        """Calculate monthly pay for salaried employee"""
        monthly_gross = annual_salary / Decimal('12')
        return monthly_gross
    
    def calculate_hourly_pay(self, hourly_rate, hours_worked):
        """Calculate pay for hourly employee"""
        return hourly_rate * Decimal(str(hours_worked))
    
    def calculate_taxes(self, gross_pay):
        """Calculate federal, state, and other taxes"""
        federal_tax = (gross_pay * self.TAX_RATES['federal']).quantize(Decimal('0.01'))
        state_tax = (gross_pay * self.TAX_RATES['state']).quantize(Decimal('0.01'))
        other_tax = (gross_pay * self.TAX_RATES['other']).quantize(Decimal('0.01'))
        net_pay = gross_pay - federal_tax - state_tax - other_tax
        
        return {
            'federal_tax': federal_tax,
            'state_tax': state_tax,
            'other_tax': other_tax,
            'net_pay': net_pay
        }
    
    def process_payroll(self, pay_period_start, pay_period_end, payment_date=None):
        """Process payroll for all employees for a given pay period"""
        if payment_date is None:
            payment_date = pay_period_end + timedelta(days=3)
        
        try:
            with get_db_cursor() as cursor:
                # Get all employees with current salary or hourly rate
                cursor.execute("""
                    SELECT 
                        e.employee_number,
                        e.employee_name,
                        e.employment_type,
                        jh.salary,
                        e.hourly_rate
                    FROM Employee e
                    LEFT JOIN JobHistory jh ON e.employee_number = jh.employee_number 
                        AND jh.is_current = TRUE
                    WHERE e.employment_type = 'salaried' OR e.hourly_rate IS NOT NULL
                """)
                
                employees = cursor.fetchall()
                payroll_records = []
                
                for emp in employees:
                    emp_num, emp_name, emp_type, salary, hourly_rate = emp
                    
                    # Calculate gross pay
                    if emp_type == 'salaried' and salary:
                        gross_pay = self.calculate_salaried_pay(salary)
                    elif emp_type == 'hourly' and hourly_rate:
                        # Get hours worked from EmployeeProject for this period
                        cursor.execute("""
                            SELECT COALESCE(SUM(hours_worked), 0)
                            FROM EmployeeProject
                            WHERE employee_number = %s 
                            AND start_date <= %s 
                            AND (end_date IS NULL OR end_date >= %s)
                        """, (emp_num, pay_period_end, pay_period_start))
                        
                        hours = cursor.fetchone()[0]
                        # For monthly payroll, assume standard hours if no project time
                        if hours == 0:
                            hours = 160  # Standard monthly hours (40 hrs/week * 4 weeks)
                        gross_pay = self.calculate_hourly_pay(hourly_rate, hours)
                    else:
                        continue
                    
                    # Calculate taxes
                    taxes = self.calculate_taxes(gross_pay)
                    
                    # Insert payroll record
                    cursor.execute("""
                        INSERT INTO PayrollHistory 
                        (employee_number, pay_period_start, pay_period_end, 
                         gross_pay, federal_tax, state_tax, other_tax, net_pay, payment_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING payroll_id
                    """, (emp_num, pay_period_start, pay_period_end, 
                          gross_pay, taxes['federal_tax'], taxes['state_tax'],
                          taxes['other_tax'], taxes['net_pay'], payment_date))
                    
                    payroll_id = cursor.fetchone()[0]
                    payroll_records.append({
                        'payroll_id': payroll_id,
                        'employee_number': emp_num,
                        'employee_name': emp_name,
                        'gross_pay': gross_pay,
                        'net_pay': taxes['net_pay']
                    })
                
                print(f"✓ Payroll processed for {len(payroll_records)} employees")
                print(f"  Period: {pay_period_start} to {pay_period_end}")
                print(f"  Payment Date: {payment_date}")
                return payroll_records
        except Exception as e:
            print(f"✗ Error processing payroll: {e}")
            return []
    
    def get_payroll_report(self, pay_period_start, pay_period_end):
        """Generate payroll report for a specific period"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.payroll_id,
                        e.employee_number,
                        e.employee_name,
                        e.employment_type,
                        p.gross_pay,
                        p.federal_tax,
                        p.state_tax,
                        p.other_tax,
                        p.net_pay,
                        p.payment_date
                    FROM PayrollHistory p
                    JOIN Employee e ON p.employee_number = e.employee_number
                    WHERE p.pay_period_start = %s AND p.pay_period_end = %s
                    ORDER BY e.employee_number
                """, (pay_period_start, pay_period_end))
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error generating payroll report: {e}")
            return []
    
    def get_employee_payroll_history(self, employee_number, year=None):
        """Get payroll history for a specific employee"""
        try:
            with get_db_cursor() as cursor:
                if year:
                    cursor.execute("""
                        SELECT 
                            payroll_id,
                            pay_period_start,
                            pay_period_end,
                            gross_pay,
                            federal_tax,
                            state_tax,
                            other_tax,
                            net_pay,
                            payment_date
                        FROM PayrollHistory
                        WHERE employee_number = %s 
                        AND EXTRACT(YEAR FROM pay_period_start) = %s
                        ORDER BY pay_period_start DESC
                    """, (employee_number, year))
                else:
                    cursor.execute("""
                        SELECT 
                            payroll_id,
                            pay_period_start,
                            pay_period_end,
                            gross_pay,
                            federal_tax,
                            state_tax,
                            other_tax,
                            net_pay,
                            payment_date
                        FROM PayrollHistory
                        WHERE employee_number = %s
                        ORDER BY pay_period_start DESC
                    """, (employee_number,))
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error getting payroll history: {e}")
            return []
    
    def get_yearly_tax_summary(self, employee_number, year):
        """Generate W-2 style summary for an employee"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        SUM(gross_pay) AS total_gross,
                        SUM(federal_tax) AS total_federal,
                        SUM(state_tax) AS total_state,
                        SUM(other_tax) AS total_other,
                        SUM(net_pay) AS total_net,
                        COUNT(*) AS pay_periods
                    FROM PayrollHistory
                    WHERE employee_number = %s 
                    AND EXTRACT(YEAR FROM pay_period_start) = %s
                """, (employee_number, year))
                
                result = cursor.fetchone()
                if result and result[0]:
                    return {
                        'total_gross': result[0],
                        'total_federal': result[1],
                        'total_state': result[2],
                        'total_other': result[3],
                        'total_net': result[4],
                        'pay_periods': result[5]
                    }
                return None
        except Exception as e:
            print(f"✗ Error generating tax summary: {e}")
            return None
    
    # ==================== REPORTING ====================
    
    def department_payroll_summary(self, department_id=None):
        """Get payroll summary by department"""
        try:
            with get_db_cursor() as cursor:
                if department_id:
                    cursor.execute("""
                        SELECT 
                            d.department_name,
                            COUNT(DISTINCT e.employee_number) AS employee_count,
                            AVG(jh.salary) AS avg_salary,
                            SUM(jh.salary) AS total_salary
                        FROM Department d
                        LEFT JOIN Employee e ON d.department_id = e.department_id
                        LEFT JOIN JobHistory jh ON e.employee_number = jh.employee_number 
                            AND jh.is_current = TRUE
                        WHERE d.department_id = %s
                        GROUP BY d.department_name
                    """, (department_id,))
                else:
                    cursor.execute("""
                        SELECT 
                            d.department_name,
                            COUNT(DISTINCT e.employee_number) AS employee_count,
                            AVG(jh.salary) AS avg_salary,
                            SUM(jh.salary) AS total_salary
                        FROM Department d
                        LEFT JOIN Employee e ON d.department_id = e.department_id
                        LEFT JOIN JobHistory jh ON e.employee_number = jh.employee_number 
                            AND jh.is_current = TRUE
                        GROUP BY d.department_name
                        ORDER BY d.department_name
                    """)
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error generating department payroll summary: {e}")
            return []


def print_employee_info(emp_info):
    """Print formatted employee information"""
    if not emp_info:
        print("Employee not found")
        return
    
    print("\n" + "="*60)
    print(f"EMPLOYEE INFORMATION")
    print("="*60)
    print(f"Employee Number: {emp_info['employee_number']}")
    print(f"Name:            {emp_info['name']}")
    print(f"Title:           {emp_info['title']}")
    print(f"Employment Type: {emp_info['employment_type']}")
    
    if emp_info['employment_type'] == 'salaried':
        print(f"Annual Salary:   ${emp_info['current_salary']:,.2f}" if emp_info['current_salary'] else "Annual Salary:   N/A")
    else:
        print(f"Hourly Rate:     ${emp_info['hourly_rate']:.2f}" if emp_info['hourly_rate'] else "Hourly Rate:     N/A")
    
    print(f"Department:      {emp_info['department'] or 'N/A'}")
    print(f"Division:        {emp_info['division'] or 'N/A'}")
    print(f"Job Start Date:  {emp_info['current_job_start'] or 'N/A'}")
    print("="*60 + "\n")


def print_employee_list(employees):
    """Print formatted list of employees"""
    print("\n" + "="*100)
    print(f"{'Emp #':<8} {'Name':<25} {'Title':<20} {'Type':<10} {'Salary/Rate':<15} {'Organization':<20}")
    print("="*100)
    
    for emp in employees:
        emp_num, name, title, emp_type, salary, hourly_rate, org = emp
        
        if emp_type == 'salaried':
            pay_str = f"${salary:,.2f}/year"
        else:
            pay_str = f"${hourly_rate:.2f}/hour"
        
        print(f"{emp_num:<8} {name:<25} {title:<20} {emp_type:<10} {pay_str:<15} {org:<20}")
    
    print("="*100 + "\n")


def print_payroll_report(payroll_data):
    """Print formatted payroll report"""
    print("\n" + "="*110)
    print(f"{'ID':<6} {'Emp #':<8} {'Name':<25} {'Type':<10} {'Gross':<12} {'Fed Tax':<10} {'State':<10} {'Other':<10} {'Net Pay':<12}")
    print("="*110)
    
    total_gross = Decimal('0')
    total_net = Decimal('0')
    
    for record in payroll_data:
        payroll_id, emp_num, name, emp_type, gross, fed, state, other, net, payment_date = record
        print(f"{payroll_id:<6} {emp_num:<8} {name:<25} {emp_type:<10} ${gross:>10,.2f} ${fed:>8,.2f} ${state:>8,.2f} ${other:>8,.2f} ${net:>10,.2f}")
        total_gross += gross
        total_net += net
    
    print("="*110)
    print(f"{'TOTALS':<49} ${total_gross:>10,.2f} {'':<30} ${total_net:>10,.2f}")
    print("="*110 + "\n")


if __name__ == "__main__":
    print("HR/Payroll Application Module")
    print("Import this module to use HR/Payroll functions")
