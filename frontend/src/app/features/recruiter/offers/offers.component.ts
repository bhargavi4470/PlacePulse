import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { RecruiterService } from '../../../core/services/recruiter.service';

@Component({
  selector: 'app-offers',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './offers.component.html',
  styleUrl: './offers.component.scss'
})
export class OffersComponent implements OnInit {
  applications: any[] = [];
  offerForm!: FormGroup;
  showOfferForm = false;
  isLoading = true;
  isSaving = false;
  errorMessage = '';
  successMessage = '';

  constructor(private recruiterService: RecruiterService, private fb: FormBuilder) {
    this.createForm();
  }

  ngOnInit(): void {
    this.loadData();
  }

  createForm() {
    this.offerForm = this.fb.group({
      application_id: ['', Validators.required],
      ctc_offered: ['', [Validators.required, Validators.min(0)]]
    });
  }

  loadData() {
    this.isLoading = true;
    this.recruiterService.getApplications().subscribe({
      next: (apps) => {
        // Show all applications but mostly they would want to offer to INTERVIEW candidates
        this.applications = apps;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load candidates.';
        this.isLoading = false;
      }
    });
  }

  onSubmit() {
    if (this.offerForm.invalid) return;

    this.isSaving = true;
    const formValue = this.offerForm.value;

    this.recruiterService.createOffer(formValue.application_id, formValue.ctc_offered).subscribe({
      next: () => {
        this.loadData();
        this.isSaving = false;
        this.showOfferForm = false;
        this.successMessage = "Offer created successfully!";
        setTimeout(() => this.successMessage = "", 3000);
        this.offerForm.reset();
      },
      error: (err) => {
        this.isSaving = false;
        this.errorMessage = err.error?.detail || 'Failed to create offer.';
        setTimeout(() => this.errorMessage = "", 3000);
      }
    });
  }
}
