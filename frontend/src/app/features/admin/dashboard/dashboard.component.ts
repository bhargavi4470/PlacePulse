import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService } from '../../../core/services/admin.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  analytics: any = null;
  isLoading = true;
  errorMessage = '';

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.adminService.getAnalytics().subscribe({
      next: (data) => {
        this.analytics = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load analytics data.';
        this.isLoading = false;
      }
    });
  }
}
