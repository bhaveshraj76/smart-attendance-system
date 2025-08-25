import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponentComponent } from './dashboard-component/dashboard-component.component';
import { AverageWorkingHourEmployeeComponentComponent } from './average-working-hour-employee-component/average-working-hour-employee-component.component';

export  const routes: Routes = [
  { path: 'dashboard', component: DashboardComponentComponent },  
  {path: 'employee', component: AverageWorkingHourEmployeeComponentComponent },
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
