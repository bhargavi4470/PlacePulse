import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-applications',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './applications.component.html',
  styleUrl: './applications.component.scss'
})
export class ApplicationsComponent implements OnInit {
  applications: any[] = [];
  isLoading = true;
  errorMessage = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadApplications();
  }

  loadApplications() {
    this.isLoading = true;
    this.http.get<any[]>('http://127.0.0.1:8000/api/applications/student').subscribe({
      next: (data) => {
        this.applications = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load applications.';
        this.isLoading = false;
      }
    });
  }
}
