import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { StudentService, StudentProfile } from '../../../core/services/student.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss'
})
export class ProfileComponent implements OnInit {
  profileForm!: FormGroup;
  isLoading = true;
  isSaving = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private studentService: StudentService
  ) {
    this.createForm();
  }

  ngOnInit(): void {
    this.loadProfile();
  }

  createForm() {
    this.profileForm = this.fb.group({
      roll_number: [{value: '', disabled: true}],
      branch: [{value: '', disabled: true}],
      graduation_year: [{value: '', disabled: true}],
      cgpa: [{value: '', disabled: true}], // Often locked in real systems, but we can make it editable if needed
      active_backlogs: [{value: '', disabled: true}],
      historical_backlogs: [{value: '', disabled: true}],
      tenth_percentage: ['', [Validators.min(0), Validators.max(100)]],
      twelfth_percentage: ['', [Validators.min(0), Validators.max(100)]],
      github_username: [''],
      resume_url: ['']
    });
  }

  loadProfile() {
    this.isLoading = true;
    this.studentService.getProfile().subscribe({
      next: (profile) => {
        this.profileForm.patchValue({
          roll_number: profile.roll_number,
          branch: profile.branch,
          graduation_year: profile.graduation_year,
          cgpa: profile.cgpa,
          active_backlogs: profile.active_backlogs,
          historical_backlogs: profile.historical_backlogs,
          tenth_percentage: profile.tenth_percentage,
          twelfth_percentage: profile.twelfth_percentage,
          github_username: profile.github_username,
          resume_url: profile.resume_url
        });
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load profile data.';
        this.isLoading = false;
      }
    });
  }

  onSubmit() {
    if (this.profileForm.invalid) return;

    this.isSaving = true;
    this.errorMessage = '';
    this.successMessage = '';

    // Only send editable fields (since disabled fields aren't in .value, or we extract carefully)
    const updateData: Partial<StudentProfile> = {
      tenth_percentage: this.profileForm.get('tenth_percentage')?.value,
      twelfth_percentage: this.profileForm.get('twelfth_percentage')?.value,
      github_username: this.profileForm.get('github_username')?.value,
      resume_url: this.profileForm.get('resume_url')?.value,
      // For backend we must pass the locked fields too based on the schema, or make a separate partial endpoint
      // Let's use getRawValue() to get all fields including disabled
      ...this.profileForm.getRawValue()
    };

    this.studentService.updateProfile(updateData).subscribe({
      next: () => {
        this.isSaving = false;
        this.successMessage = 'Profile updated successfully!';
        setTimeout(() => this.successMessage = '', 3000);
      },
      error: () => {
        this.isSaving = false;
        this.errorMessage = 'Failed to update profile. Please try again.';
      }
    });
  }
}
