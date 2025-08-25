import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-average-working-hour-employee-component',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './average-working-hour-employee-component.component.html',
  styles: [`
    .container {
  max-width: 900px;
  margin: auto;
  padding: 20px;
}
 
h2 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
}
 
.table {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
 
.table th {
  background: #34495e !important;
  color: #fff;
  font-weight: 500;
}
 
.table td {
  vertical-align: middle;
  font-size: 0.95rem;
}
 
.badge {
  font-size: 1rem;
  padding: 8px 12px;
  border-radius: 8px;
}
 
.badge.bg-primary {
  background: linear-gradient(90deg, #4e73df, #224abe);
}
 
.text-end h5 {
  font-weight: 600;
  color: #333;
}
 
tr:hover {
  background-color: #f6f9fc;
  transition: 0.2s ease-in-out;
}`]
})
export class AverageWorkingHourEmployeeComponentComponent {
// Sample employee data (replace later with API data from FastAPI + MySQL)
  employees = [
    { name: 'John Doe', totalHours: 40, workingDays: 5 },
    { name: 'Jane Smith', totalHours: 36, workingDays: 5 }
  ];
 
  constructor() {}
 
  ngOnInit(): void {
    // Later, you can fetch employee attendance data from backend API here
  }
 
  // Calculate average hours per employee
  // getAverageHours(employee: Employee): number {
  //   return employee.workingDays > 0
  //     ? employee.totalHours / employee.workingDays
  //     : 0;
  // }
 
  // Calculate overall average working hours across all employees
  // getOverallAverage(): number {
  //   if (this.employees.length === 0) return 0;
  //   const total = this.employees.reduce((sum, e) => sum + this.getAverageHours(e), 0);
  //   return total / this.employees.length;
  // }
}
