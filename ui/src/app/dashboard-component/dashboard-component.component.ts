import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-dashboard-component',
  standalone: true,
  imports: [MatCardModule, MatTableModule, CommonModule, HttpClientModule],

  templateUrl: './dashboard-component.component.html',
  styles: [`
    .dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.widget-row {
  display: flex;
  gap: 16px;
}

.dashboard-widget {
  flex: 1;
  color: white;
  font-weight: bold;
  font-size: 1.5rem;       /* slightly bigger font */
  padding: 40px 20px;      /* increase vertical padding for height */
  min-height: 150px;       /* set a fixed minimum height */
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 8px rgb(0 0 0 / 0.15);
  transition: transform 0.3s ease;
  cursor: pointer;
}
.dashboard-widget:hover {
  transform: translateY(-6px);
}

.widget1 {
  background: linear-gradient(135deg, #ff4e50 0%, #f9d423 100%); /* red to amber */
}
.widget2 {
  background: linear-gradient(135deg, #1e90ff 0%, #00bfff 100%); /* bright blue shades */
  color: #fff;
}
.widget3 {
  background: linear-gradient(135deg, #32cd32 0%, #7fff00 100%); /* lime green to light green */
}

.widget4 {
  background: linear-gradient(135deg, #f4f400ff 0%, #7fff00 100%); /* lime green to light green */
}

.list-widget {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 10px 20px rgb(0 0 0 / 0.1);
}

.list-widget h3 {
  margin-bottom: 16px;
  color: #333;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1rem;
}

.student-table thead {
  background-color: #4a90e2;
  color: #fff;
}

.student-table th,
.student-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
}

.student-table tbody tr:nth-child(even) {
  background-color: #f4f6f8;
}

.student-table tbody tr:hover {
  background-color: #dbe9ff;
  cursor: pointer;
}
.count {
  font-size: 2.5rem;
  font-weight: 700;
  margin-top: 12px;
  color: #fff;
}
h3 {
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
  position: relative;
  letter-spacing: 1px;
}
 
/* Underline accent */
h3::after {
  content: "";
  display: block;
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #4e73df, #224abe);
  margin: 10px auto 0;
  border-radius: 2px;
}
/* Container label spacing */
label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}
.weekly{
  
}

/* Style for the select dropdown */
select {
  justify-content: end;
  width: 100%;
  max-width: 320px;
  padding: 10px 14px;
  font-size: 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  border: 2px solid #4a90e2;          /* primary blue border */
  border-radius: 8px;
  background-color: #fff;
  color: #333;
  cursor: pointer;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  appearance: none;                   /* Remove default arrow in some browsers */
  background-image: url('data:image/svg+xml;utf8,<svg fill="%234a90e2" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>');
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px 16px;
}

/* Hover and focus effects */
select:hover, select:focus {
  border-color: #357ABD;
  box-shadow: 0 0 6px rgba(53, 122, 189, 0.6);
  outline: none;
}

/* Disabled state */
select:disabled {
  background-color: #eee;
  border-color: #ccc;
  color: #999;
  cursor: not-allowed;
}

`]
})
export class DashboardComponentComponent {
  data: any; 
 displayedColumns: string[] = ['name', 'date', 'in', 'out', 'hours', 'status'];
  studentList = [
    { name: 'John Doe', date: '2025-08-25', in: '9:05', out: '17:30', hours: 8.5, status: 'Late' },
    // ... more rows
  ];

  weeks = [
  { "week_no": 1, "start_date": "2024-12-30", "end_date": "2025-01-05" },
  { "week_no": 2, "start_date": "2025-01-06", "end_date": "2025-01-12" },
  { "week_no": 3, "start_date": "2025-01-13", "end_date": "2025-01-19" },
  { "week_no": 4, "start_date": "2025-01-20", "end_date": "2025-01-26" },
  { "week_no": 5, "start_date": "2025-01-27", "end_date": "2025-02-02" },
  { "week_no": 6, "start_date": "2025-02-03", "end_date": "2025-02-09" },
  { "week_no": 7, "start_date": "2025-02-10", "end_date": "2025-02-16" },
  { "week_no": 8, "start_date": "2025-02-17", "end_date": "2025-02-23" },
  { "week_no": 9, "start_date": "2025-02-24", "end_date": "2025-03-02" },
  { "week_no": 10, "start_date": "2025-03-03", "end_date": "2025-03-09" },
  { "week_no": 11, "start_date": "2025-03-10", "end_date": "2025-03-16" },
  { "week_no": 12, "start_date": "2025-03-17", "end_date": "2025-03-23" },
  { "week_no": 13, "start_date": "2025-03-24", "end_date": "2025-03-30" },
  { "week_no": 14, "start_date": "2025-03-31", "end_date": "2025-04-06" },
  { "week_no": 15, "start_date": "2025-04-07", "end_date": "2025-04-13" },
  { "week_no": 16, "start_date": "2025-04-14", "end_date": "2025-04-20" },
  { "week_no": 17, "start_date": "2025-04-21", "end_date": "2025-04-27" },
  { "week_no": 18, "start_date": "2025-04-28", "end_date": "2025-05-04" },
  { "week_no": 19, "start_date": "2025-05-05", "end_date": "2025-05-11" },
  { "week_no": 20, "start_date": "2025-05-12", "end_date": "2025-05-18" },
  { "week_no": 21, "start_date": "2025-05-19", "end_date": "2025-05-25" },
  { "week_no": 22, "start_date": "2025-05-26", "end_date": "2025-06-01" },
  { "week_no": 23, "start_date": "2025-06-02", "end_date": "2025-06-08" },
  { "week_no": 24, "start_date": "2025-06-09", "end_date": "2025-06-15" },
  { "week_no": 25, "start_date": "2025-06-16", "end_date": "2025-06-22" },
  { "week_no": 26, "start_date": "2025-06-23", "end_date": "2025-06-29" },
  { "week_no": 27, "start_date": "2025-06-30", "end_date": "2025-07-06" },
  { "week_no": 28, "start_date": "2025-07-07", "end_date": "2025-07-13" },
  { "week_no": 29, "start_date": "2025-07-14", "end_date": "2025-07-20" },
  { "week_no": 30, "start_date": "2025-07-21", "end_date": "2025-07-27" },
  { "week_no": 31, "start_date": "2025-07-28", "end_date": "2025-08-03" },
  { "week_no": 32, "start_date": "2025-08-04", "end_date": "2025-08-10" },
  { "week_no": 33, "start_date": "2025-08-11", "end_date": "2025-08-17" },
  { "week_no": 34, "start_date": "2025-08-18", "end_date": "2025-08-24" },
  { "week_no": 35, "start_date": "2025-08-25", "end_date": "2025-08-31" },
  { "week_no": 36, "start_date": "2025-09-01", "end_date": "2025-09-07" },
  { "week_no": 37, "start_date": "2025-09-08", "end_date": "2025-09-14" },
  { "week_no": 38, "start_date": "2025-09-15", "end_date": "2025-09-21" },
  { "week_no": 39, "start_date": "2025-09-22", "end_date": "2025-09-28" },
  { "week_no": 40, "start_date": "2025-09-29", "end_date": "2025-10-05" },
  { "week_no": 41, "start_date": "2025-10-06", "end_date": "2025-10-12" },
  { "week_no": 42, "start_date": "2025-10-13", "end_date": "2025-10-19" },
  { "week_no": 43, "start_date": "2025-10-20", "end_date": "2025-10-26" },
  { "week_no": 44, "start_date": "2025-10-27", "end_date": "2025-11-02" },
  { "week_no": 45, "start_date": "2025-11-03", "end_date": "2025-11-09" },
  { "week_no": 46, "start_date": "2025-11-10", "end_date": "2025-11-16" },
  { "week_no": 47, "start_date": "2025-11-17", "end_date": "2025-11-23" },
  { "week_no": 48, "start_date": "2025-11-24", "end_date": "2025-11-30" },
  { "week_no": 49, "start_date": "2025-12-01", "end_date": "2025-12-07" },
  { "week_no": 50, "start_date": "2025-12-08", "end_date": "2025-12-14" },
  { "week_no": 51, "start_date": "2025-12-15", "end_date": "2025-12-21" },
  { "week_no": 52, "start_date": "2025-12-22", "end_date": "2025-12-28" }
];
selectedWeekNo : any = null;
onWeekChange(event: any) {
  this.selectedWeekNo = +event.target.value;
  console.log('Selected Week:', this.selectedWeekNo);

  // Find week object
  const selectedWeek = this.weeks.find(w => w.week_no === this.selectedWeekNo);
  if (selectedWeek) {
    const { start_date, end_date } = selectedWeek;
    this.weekavg(start_date, end_date);
  } else {
    console.error('Selected week not found in weeks array');
  }
}



   // Properties to hold the count data
  lateArrivalCount: number = 0;
  earlyLeaverCount: number = 0;
  overtimeCount: number = 0;
constructor(private http: HttpClient) {
  
}
  ngOnInit() {
    // Simulating backend data response
    const backendData = {
      attendance_summary: {
        counts: {
          late_comers_count: 4980,
          early_comers_count: 2324,
          overtime_count: 4345,
        },
      },
    };
  
  }
   weekavg(startDate: string, endDate: string): void {
    
      // Create URL with query params
      const url = 'http://192.168.1.132:8000/attendance/weekly-average';
      const params = { start_date: startDate, end_date: endDate };
      

      this.http.get(url, { params })
        .subscribe({
          next: (response: any) => {
            this.data = response;
            console.log('Data received:', this.data);
          },
          error: (error: any) => {
            console.error('Error fetching data:', error);
          }
        });
    }


    // Assign backend data to component properties
    // this.lateArrivalCount = backendData.attendance_summary.counts.late_comers_count;
    // this.earlyLeaverCount = backendData.attendance_summary.counts.early_comers_count;
    // this.overtimeCount = backendData.attendance_summary.counts.overtime_count;

}
