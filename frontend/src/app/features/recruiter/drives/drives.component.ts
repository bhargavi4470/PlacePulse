import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { RecruiterService } from '../../../core/services/recruiter.service';

@Component({
  selector: 'app-drives',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './drives.component.html',
  styleUrl: './drives.component.scss'
})
export class DrivesComponent implements OnInit {
  drives: any[] = [];
  driveForm!: FormGroup;
  showCreateForm = false;
  isLoading = true;
  isSaving = false;
  errorMessage = '';

  constructor(private recruiterService: RecruiterService, private fb: FormBuilder) {
    this.createForm();
  }

  ngOnInit(): void {
    this.loadDrives();
  }

  createForm() {
    this.driveForm = this.fb.group({
      job_title: ['', Validators.required],
      job_description: [''],
      ctc: ['', [Validators.required, Validators.min(0)]],
      location: [''],
      job_type: ['Full Time'],
      registration_deadline: ['', Validators.required],
      min_cgpa: [0, [Validators.min(0), Validators.max(10)]],
      max_active_backlogs: [0, Validators.min(0)],
      max_historical_backlogs: [0, Validators.min(0)],
      allowed_branches: ['']
    });
  }

  loadDrives() {
    this.isLoading = true;
    this.recruiterService.getDrives().subscribe({
      next: (data) => {
        this.drives = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load drives.';
        this.isLoading = false;
      }
    });
  }

  onSubmit() {
    if (this.driveForm.invalid) return;

    this.isSaving = true;
    const formValue = this.driveForm.value;
    
    // Ensure date is properly formatted for datetime string
    formValue.registration_deadline = new Date(formValue.registration_deadline).toISOString();

    this.recruiterService.createDrive(formValue).subscribe({
      next: (newDrive) => {
        this.drives.push(newDrive);
        this.isSaving = false;
        this.showCreateForm = false;
        this.driveForm.reset({
          job_type: 'Full Time',
          min_cgpa: 0,
          max_active_backlogs: 0,
          max_historical_backlogs: 0
        });
      },
      error: (err) => {
        this.isSaving = false;
        this.errorMessage = err.error?.detail || 'Failed to create drive.';
      }
    });
  }
}
