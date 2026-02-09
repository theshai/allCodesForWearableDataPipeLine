import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';
import { DashboardComponent } from './dashboard/dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,DashboardComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  data: any;
  title= 'angular-api-gateway';

  constructor(private api: ApiService) {}

  load() {
    this.api.getUser('shai').subscribe({
      next: (res) => {
        this.data = res;
        console.error('API response:', res);
      },
      error: (err) => {
        console.error('API error:', err);
      }
    });
  }
}
