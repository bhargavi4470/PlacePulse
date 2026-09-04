import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RecruiterService } from '../../../core/services/recruiter.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-candidates',
  standalone: true,
  imports: [CommonModule, FormsModule, DatePipe],
  templateUrl: './candidates.component.html',
  styleUrl: './candidates.component.scss'
})
export class CandidatesComponent implements OnInit {
  applications: any[] = [];
  isLoading = true;
  errorMessage = '';
  isUpdating: number | null = null;

  stages = ['APPLIED', 'SHORTLISTED', 'ASSESSMENT', 'INTERVIEW', 'OFFERED', 'REJECTED'];

  constructor(private recruiterService: RecruiterService) {}

  ngOnInit(): void {
    this.loadApplications();
  }

  loadApplications() {
    this.isLoading = true;
    this.recruiterService.getApplications().subscribe({
      next: (data) => {
        this.applications = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load candidates.';
        this.isLoading = false;
      }
    });
  }

  getApplicationsByStatus(status: string) {
    return this.applications.filter(app => app.status === status);
  }

  updateStatus(appId: number, newStatus: string) {
    this.isUpdating = appId;
    this.recruiterService.updateApplicationStatus(appId, newStatus).subscribe({
      next: (res) => {
        const app = this.applications.find(a => a.id === appId);
        if (app) app.status = res.status;
        this.isUpdating = null;
      },
      error: () => {
        this.isUpdating = null;
        alert('Failed to update status');
      }
    });
  }
}
