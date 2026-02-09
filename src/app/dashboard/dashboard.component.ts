import { Component, OnInit, OnDestroy } from '@angular/core';
import { ApiService } from '../services/api.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Subscription, interval } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-dashboard',
  standalone: true,       // ← makes this a standalone component
  imports: [CommonModule, HttpClientModule], // modules it needs
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit, OnDestroy {

  data: any;
  private subscription!: Subscription;

  constructor(private api: ApiService) {}

  ngOnInit() {
    // Poll API every 5 seconds
    this.subscription = interval(5000)
      .pipe(switchMap(() => this.api.getUser('shai')))
      .subscribe({
        next: (res) => this.data = res,
        error: (err) => console.error('API error:', err)
      });
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}