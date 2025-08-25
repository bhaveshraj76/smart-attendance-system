import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { DashboardComponentComponent } from './app/dashboard-component/dashboard-component.component';

bootstrapApplication(DashboardComponentComponent, appConfig)
  .catch((err) => console.error(err));
