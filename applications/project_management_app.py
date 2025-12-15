"""
Project Management Application
Handles project creation, team assignments, milestone tracking, and reporting
"""
from database_config import get_db_cursor
from datetime import datetime, date
from decimal import Decimal
import sys

class ProjectManagementApp:
    """Project Management Application"""
    
    def __init__(self):
        pass
    
    # ==================== PROJECT MANAGEMENT ====================
    
    def create_project(self, project_number, project_name, budget, date_started,
                      manager_emp_id, department_id, date_ended=None):
        """Create a new project"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Project 
                    (project_number, project_name, budget, date_started, 
                     date_ended, manager_emp_id, department_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING project_number
                """, (project_number, project_name, budget, date_started,
                      date_ended, manager_emp_id, department_id))
                
                proj_num = cursor.fetchone()[0]
                print(f"✓ Project {proj_num} ({project_name}) created successfully")
                print(f"  Manager: Employee #{manager_emp_id}")
                print(f"  Budget: ${budget:,.2f}")
                return proj_num
        except Exception as e:
            print(f"✗ Error creating project: {e}")
            return None
    
    def get_project_info(self, project_number):
        """Get detailed project information"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.project_number,
                        p.project_name,
                        p.budget,
                        p.date_started,
                        p.date_ended,
                        m.employee_name AS manager_name,
                        m.employee_number AS manager_id,
                        d.department_name,
                        d.department_id
                    FROM Project p
                    JOIN Employee m ON p.manager_emp_id = m.employee_number
                    JOIN Department d ON p.department_id = d.department_id
                    WHERE p.project_number = %s
                """, (project_number,))
                
                result = cursor.fetchone()
                if result:
                    return {
                        'project_number': result[0],
                        'project_name': result[1],
                        'budget': result[2],
                        'date_started': result[3],
                        'date_ended': result[4],
                        'manager_name': result[5],
                        'manager_id': result[6],
                        'department_name': result[7],
                        'department_id': result[8]
                    }
                return None
        except Exception as e:
            print(f"✗ Error getting project info: {e}")
            return None
    
    def update_project(self, project_number, **kwargs):
        """Update project information"""
        try:
            valid_fields = ['project_name', 'budget', 'date_ended', 'manager_emp_id']
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if field in valid_fields and value is not None:
                    updates.append(f"{field} = %s")
                    values.append(value)
            
            if not updates:
                print("No valid fields to update")
                return False
            
            values.append(project_number)
            
            with get_db_cursor() as cursor:
                query = f"UPDATE Project SET {', '.join(updates)} WHERE project_number = %s"
                cursor.execute(query, values)
                print(f"✓ Project {project_number} updated successfully")
                return True
        except Exception as e:
            print(f"✗ Error updating project: {e}")
            return False
    
    def list_all_projects(self, include_completed=True):
        """List all projects"""
        try:
            with get_db_cursor() as cursor:
                if include_completed:
                    cursor.execute("""
                        SELECT 
                            p.project_number,
                            p.project_name,
                            p.budget,
                            p.date_started,
                            p.date_ended,
                            m.employee_name AS manager_name,
                            d.department_name,
                            CASE WHEN p.date_ended IS NULL THEN 'Active' ELSE 'Completed' END AS status
                        FROM Project p
                        JOIN Employee m ON p.manager_emp_id = m.employee_number
                        JOIN Department d ON p.department_id = d.department_id
                        ORDER BY p.project_number
                    """)
                else:
                    cursor.execute("""
                        SELECT 
                            p.project_number,
                            p.project_name,
                            p.budget,
                            p.date_started,
                            p.date_ended,
                            m.employee_name AS manager_name,
                            d.department_name,
                            'Active' AS status
                        FROM Project p
                        JOIN Employee m ON p.manager_emp_id = m.employee_number
                        JOIN Department d ON p.department_id = d.department_id
                        WHERE p.date_ended IS NULL
                        ORDER BY p.project_number
                    """)
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error listing projects: {e}")
            return []
    
    # ==================== TEAM MANAGEMENT ====================
    
    def assign_employee_to_project(self, employee_number, project_number, role,
                                   start_date, hours_worked=0, is_current=True):
        """Assign an employee to a project"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO EmployeeProject 
                    (employee_number, project_number, role, hours_worked, 
                     start_date, is_current)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING employee_number, project_number
                """, (employee_number, project_number, role, hours_worked,
                      start_date, is_current))
                
                result = cursor.fetchone()
                print(f"✓ Employee {employee_number} assigned to project {project_number}")
                print(f"  Role: {role}")
                return result
        except Exception as e:
            print(f"✗ Error assigning employee to project: {e}")
            return None
    
    def update_employee_project_hours(self, employee_number, project_number, additional_hours):
        """Update hours worked by an employee on a project"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    UPDATE EmployeeProject 
                    SET hours_worked = hours_worked + %s
                    WHERE employee_number = %s AND project_number = %s
                    RETURNING hours_worked
                """, (additional_hours, employee_number, project_number))
                
                result = cursor.fetchone()
                if result:
                    print(f"✓ Hours updated for employee {employee_number} on project {project_number}")
                    print(f"  Total hours: {result[0]}")
                    return result[0]
                return None
        except Exception as e:
            print(f"✗ Error updating hours: {e}")
            return None
    
    def remove_employee_from_project(self, employee_number, project_number, end_date):
        """Remove employee from project (set end_date and is_current to False)"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    UPDATE EmployeeProject 
                    SET end_date = %s, is_current = FALSE
                    WHERE employee_number = %s AND project_number = %s
                    RETURNING employee_number
                """, (end_date, employee_number, project_number))
                
                result = cursor.fetchone()
                if result:
                    print(f"✓ Employee {employee_number} removed from project {project_number}")
                    return True
                return False
        except Exception as e:
            print(f"✗ Error removing employee from project: {e}")
            return False
    
    def get_project_team(self, project_number, current_only=True):
        """Get list of employees assigned to a project"""
        try:
            with get_db_cursor() as cursor:
                if current_only:
                    cursor.execute("""
                        SELECT 
                            e.employee_number,
                            e.employee_name,
                            e.title,
                            ep.role,
                            ep.hours_worked,
                            ep.start_date,
                            ep.end_date
                        FROM EmployeeProject ep
                        JOIN Employee e ON ep.employee_number = e.employee_number
                        WHERE ep.project_number = %s AND ep.is_current = TRUE
                        ORDER BY e.employee_name
                    """, (project_number,))
                else:
                    cursor.execute("""
                        SELECT 
                            e.employee_number,
                            e.employee_name,
                            e.title,
                            ep.role,
                            ep.hours_worked,
                            ep.start_date,
                            ep.end_date
                        FROM EmployeeProject ep
                        JOIN Employee e ON ep.employee_number = e.employee_number
                        WHERE ep.project_number = %s
                        ORDER BY e.employee_name
                    """, (project_number,))
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error getting project team: {e}")
            return []
    
    def get_employee_projects(self, employee_number, current_only=True):
        """Get list of projects an employee is/was assigned to"""
        try:
            with get_db_cursor() as cursor:
                if current_only:
                    cursor.execute("""
                        SELECT 
                            p.project_number,
                            p.project_name,
                            ep.role,
                            ep.hours_worked,
                            ep.start_date,
                            ep.end_date,
                            m.employee_name AS manager_name
                        FROM EmployeeProject ep
                        JOIN Project p ON ep.project_number = p.project_number
                        JOIN Employee m ON p.manager_emp_id = m.employee_number
                        WHERE ep.employee_number = %s AND ep.is_current = TRUE
                        ORDER BY ep.start_date DESC
                    """, (employee_number,))
                else:
                    cursor.execute("""
                        SELECT 
                            p.project_number,
                            p.project_name,
                            ep.role,
                            ep.hours_worked,
                            ep.start_date,
                            ep.end_date,
                            m.employee_name AS manager_name
                        FROM EmployeeProject ep
                        JOIN Project p ON ep.project_number = p.project_number
                        JOIN Employee m ON p.manager_emp_id = m.employee_number
                        WHERE ep.employee_number = %s
                        ORDER BY ep.start_date DESC
                    """, (employee_number,))
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error getting employee projects: {e}")
            return []
    
    # ==================== MILESTONE MANAGEMENT ====================
    
    def add_milestone(self, project_number, milestone_name, description,
                     due_date, status='pending', details_done=None, details_remaining=None):
        """Add a milestone to a project"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ProjectMilestone 
                    (project_number, milestone_name, description, due_date, 
                     status, details_done, details_remaining)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING milestone_id
                """, (project_number, milestone_name, description, due_date,
                      status, details_done, details_remaining))
                
                milestone_id = cursor.fetchone()[0]
                print(f"✓ Milestone {milestone_id} ({milestone_name}) added to project {project_number}")
                return milestone_id
        except Exception as e:
            print(f"✗ Error adding milestone: {e}")
            return None
    
    def update_milestone(self, milestone_id, **kwargs):
        """Update milestone information"""
        try:
            valid_fields = ['milestone_name', 'description', 'due_date', 
                          'completion_date', 'status', 'details_done', 'details_remaining']
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if field in valid_fields and value is not None:
                    updates.append(f"{field} = %s")
                    values.append(value)
            
            if not updates:
                print("No valid fields to update")
                return False
            
            values.append(milestone_id)
            
            with get_db_cursor() as cursor:
                query = f"UPDATE ProjectMilestone SET {', '.join(updates)} WHERE milestone_id = %s"
                cursor.execute(query, values)
                print(f"✓ Milestone {milestone_id} updated successfully")
                return True
        except Exception as e:
            print(f"✗ Error updating milestone: {e}")
            return False
    
    def complete_milestone(self, milestone_id, completion_date=None):
        """Mark a milestone as completed"""
        if completion_date is None:
            completion_date = date.today()
        
        return self.update_milestone(
            milestone_id,
            status='completed',
            completion_date=completion_date
        )
    
    def get_project_milestones(self, project_number):
        """Get all milestones for a project"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        milestone_id,
                        milestone_name,
                        description,
                        due_date,
                        completion_date,
                        status,
                        details_done,
                        details_remaining
                    FROM ProjectMilestone
                    WHERE project_number = %s
                    ORDER BY due_date
                """, (project_number,))
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error getting project milestones: {e}")
            return []
    
    # ==================== REPORTING AND STATISTICS ====================
    
    def get_project_statistics(self, project_number):
        """Get comprehensive statistics for a project"""
        try:
            with get_db_cursor() as cursor:
                # Basic project info
                project_info = self.get_project_info(project_number)
                
                # Team statistics
                cursor.execute("""
                    SELECT 
                        COUNT(DISTINCT employee_number) AS team_size,
                        SUM(hours_worked) AS total_hours
                    FROM EmployeeProject
                    WHERE project_number = %s
                """, (project_number,))
                team_stats = cursor.fetchone()
                
                # Current team size
                cursor.execute("""
                    SELECT COUNT(DISTINCT employee_number)
                    FROM EmployeeProject
                    WHERE project_number = %s AND is_current = TRUE
                """, (project_number,))
                current_team_size = cursor.fetchone()[0]
                
                # Milestone statistics
                cursor.execute("""
                    SELECT 
                        COUNT(*) AS total_milestones,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed,
                        COUNT(CASE WHEN status = 'in_progress' THEN 1 END) AS in_progress,
                        COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending
                    FROM ProjectMilestone
                    WHERE project_number = %s
                """, (project_number,))
                milestone_stats = cursor.fetchone()
                
                return {
                    'project_info': project_info,
                    'team_size': team_stats[0] or 0,
                    'current_team_size': current_team_size or 0,
                    'total_person_hours': team_stats[1] or 0,
                    'total_milestones': milestone_stats[0] or 0,
                    'completed_milestones': milestone_stats[1] or 0,
                    'in_progress_milestones': milestone_stats[2] or 0,
                    'pending_milestones': milestone_stats[3] or 0
                }
        except Exception as e:
            print(f"✗ Error getting project statistics: {e}")
            return None
    
    def get_department_projects_summary(self, department_id=None):
        """Get summary of projects by department"""
        try:
            with get_db_cursor() as cursor:
                if department_id:
                    cursor.execute("""
                        SELECT 
                            d.department_name,
                            COUNT(p.project_number) AS total_projects,
                            COUNT(CASE WHEN p.date_ended IS NULL THEN 1 END) AS active_projects,
                            SUM(p.budget) AS total_budget,
                            AVG(team_stats.team_size) AS avg_team_size,
                            SUM(team_stats.total_hours) AS total_person_hours
                        FROM Department d
                        LEFT JOIN Project p ON d.department_id = p.department_id
                        LEFT JOIN (
                            SELECT 
                                project_number,
                                COUNT(DISTINCT employee_number) AS team_size,
                                SUM(hours_worked) AS total_hours
                            FROM EmployeeProject
                            GROUP BY project_number
                        ) team_stats ON p.project_number = team_stats.project_number
                        WHERE d.department_id = %s
                        GROUP BY d.department_name
                    """, (department_id,))
                else:
                    cursor.execute("""
                        SELECT 
                            d.department_name,
                            COUNT(p.project_number) AS total_projects,
                            COUNT(CASE WHEN p.date_ended IS NULL THEN 1 END) AS active_projects,
                            SUM(p.budget) AS total_budget,
                            AVG(team_stats.team_size) AS avg_team_size,
                            SUM(team_stats.total_hours) AS total_person_hours
                        FROM Department d
                        LEFT JOIN Project p ON d.department_id = p.department_id
                        LEFT JOIN (
                            SELECT 
                                project_number,
                                COUNT(DISTINCT employee_number) AS team_size,
                                SUM(hours_worked) AS total_hours
                            FROM EmployeeProject
                            GROUP BY project_number
                        ) team_stats ON p.project_number = team_stats.project_number
                        GROUP BY d.department_name
                        ORDER BY d.department_name
                    """)
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error getting department projects summary: {e}")
            return []
    
    def get_employee_productivity_report(self):
        """Get productivity report for all employees with project assignments"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.employee_number,
                        e.employee_name,
                        e.title,
                        d.department_name,
                        COUNT(DISTINCT ep.project_number) AS projects_count,
                        SUM(ep.hours_worked) AS total_hours,
                        COUNT(CASE WHEN ep.is_current = TRUE THEN 1 END) AS current_projects
                    FROM Employee e
                    JOIN EmployeeProject ep ON e.employee_number = ep.employee_number
                    LEFT JOIN Department d ON e.department_id = d.department_id
                    GROUP BY e.employee_number, e.employee_name, e.title, d.department_name
                    ORDER BY total_hours DESC
                """)
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"✗ Error getting employee productivity report: {e}")
            return []


# ==================== DISPLAY FUNCTIONS ====================

def print_project_info(proj_info):
    """Print formatted project information"""
    if not proj_info:
        print("Project not found")
        return
    
    print("\n" + "="*60)
    print(f"PROJECT INFORMATION")
    print("="*60)
    print(f"Project Number:  {proj_info['project_number']}")
    print(f"Project Name:    {proj_info['project_name']}")
    print(f"Budget:          ${proj_info['budget']:,.2f}")
    print(f"Start Date:      {proj_info['date_started']}")
    print(f"End Date:        {proj_info['date_ended'] or 'Ongoing'}")
    print(f"Manager:         {proj_info['manager_name']} (ID: {proj_info['manager_id']})")
    print(f"Department:      {proj_info['department_name']}")
    print("="*60 + "\n")


def print_project_list(projects):
    """Print formatted list of projects"""
    print("\n" + "="*110)
    print(f"{'Proj #':<8} {'Project Name':<30} {'Budget':<15} {'Start Date':<12} {'End Date':<12} {'Manager':<20} {'Status':<10}")
    print("="*110)
    
    for proj in projects:
        proj_num, name, budget, start, end, manager, dept, status = proj
        end_str = str(end) if end else 'Ongoing'
        print(f"{proj_num:<8} {name:<30} ${budget:>13,.2f} {start!s:<12} {end_str:<12} {manager:<20} {status:<10}")
    
    print("="*110 + "\n")


def print_project_team(team_members):
    """Print formatted project team list"""
    print("\n" + "="*110)
    print(f"{'Emp #':<8} {'Name':<25} {'Title':<20} {'Role':<20} {'Hours':<10} {'Start Date':<12}")
    print("="*110)
    
    total_hours = 0
    for member in team_members:
        emp_num, name, title, role, hours, start, end = member
        print(f"{emp_num:<8} {name:<25} {title:<20} {role:<20} {hours:>8.1f} {start!s:<12}")
        total_hours += float(hours)
    
    print("="*110)
    print(f"{'Total Hours:':<74} {total_hours:>8.1f}")
    print("="*110 + "\n")


def print_milestones(milestones):
    """Print formatted milestone list"""
    print("\n" + "="*110)
    print(f"{'ID':<6} {'Milestone Name':<30} {'Due Date':<12} {'Completed':<12} {'Status':<15} {'Done/Remaining':<30}")
    print("="*110)
    
    for milestone in milestones:
        ms_id, name, desc, due, completed, status, done, remaining = milestone
        comp_str = str(completed) if completed else 'N/A'
        done_str = (done[:27] + '...') if done and len(done) > 30 else (done or 'N/A')
        print(f"{ms_id:<6} {name:<30} {due!s:<12} {comp_str:<12} {status:<15} {done_str:<30}")
    
    print("="*110 + "\n")


def print_project_statistics(stats):
    """Print formatted project statistics"""
    if not stats:
        print("No statistics available")
        return
    
    proj = stats['project_info']
    
    print("\n" + "="*70)
    print(f"PROJECT STATISTICS: {proj['project_name']}")
    print("="*70)
    print(f"Project Number:         {proj['project_number']}")
    print(f"Budget:                 ${proj['budget']:,.2f}")
    print(f"Status:                 {'Completed' if proj['date_ended'] else 'Active'}")
    print("-"*70)
    print(f"Team Members (Total):   {stats['team_size']}")
    print(f"Current Team Size:      {stats['current_team_size']}")
    print(f"Total Person-Hours:     {stats['total_person_hours']:,.1f}")
    print("-"*70)
    print(f"Total Milestones:       {stats['total_milestones']}")
    print(f"  Completed:            {stats['completed_milestones']}")
    print(f"  In Progress:          {stats['in_progress_milestones']}")
    print(f"  Pending:              {stats['pending_milestones']}")
    
    if stats['total_milestones'] > 0:
        completion_pct = (stats['completed_milestones'] / stats['total_milestones']) * 100
        print(f"  Completion Rate:      {completion_pct:.1f}%")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    print("Project Management Application Module")
    print("Import this module to use Project Management functions")
