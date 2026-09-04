import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService, EligibilityResult } from '../../../core/services/admin.service';

@Component({
  selector: 'app-eligibility',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './eligibility.component.html',
  styleUrl: './eligibility.component.scss'
})
export class EligibilityComponent implements OnInit {
  students: any[] = [];
  drives: any[] = [];
  
  selectedStudentId: number | null = null;
  selectedDriveId: number | null = null;
  
  evaluationResult: EligibilityResult | null = null;
  isLoading = false;
  errorMessage = '';

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.adminService.getStudents().subscribe(res => this.students = res);
    this.adminService.getDrives().subscribe(res => this.drives = res);
  }

  evaluate() {
    if (!this.selectedStudentId || !this.selectedDriveId) {
      this.errorMessage = "Please select both a student and a drive.";
      return;
    }
    
    this.isLoading = true;
    this.errorMessage = '';
    this.evaluationResult = null;

    this.adminService.evaluateEligibility(this.selectedStudentId, this.selectedDriveId).subscribe({
      next: (result) => {
        this.evaluationResult = result;
        this.isLoading = false;
      },
      error: (err) => {
        this.errorMessage = "Evaluation failed. " + (err.error?.detail || err.message);
        this.isLoading = false;
      }
    });
  }
}
