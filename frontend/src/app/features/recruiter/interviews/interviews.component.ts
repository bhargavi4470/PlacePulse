import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { RecruiterService } from '../../../core/services/recruiter.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-interviews',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, DatePipe],
  templateUrl: './interviews.component.html',
  styleUrl: './interviews.component.scss'
})
export class InterviewsComponent implements OnInit {
  interviews: any[] = [];
  applications: any[] = []; // To populate dropdown for scheduling
  scheduleForm!: FormGroup;
  showScheduleForm = false;
  isLoading = true;
  isSaving = false;
  errorMessage = '';

  constructor(private recruiterService: RecruiterService, private fb: FormBuilder) {
    this.createForm();
  }

  ngOnInit(): void {
    this.loadData();
  }

  createForm() {
    this.scheduleForm = this.fb.group({
      application_id: ['', Validators.required],
      round_name: ['Technical Round 1', Validators.required],
      scheduled_time: ['', Validators.required],
      meeting_link: ['']
    });
  }

  loadData() {
    this.isLoading = true;
    // Load interviews
    this.recruiterService.getInterviews().subscribe({
      next: (data) => {
        this.interviews = data;
        
        // Also load applications for the dropdown
        this.recruiterService.getApplications().subscribe({
          next: (apps) => {
            // Only show shortlisted/assessment/interview candidates for scheduling
            this.applications = apps.filter(a => ['SHORTLISTED', 'ASSESSMENT', 'INTERVIEW'].includes(a.status));
            this.isLoading = false;
          }
        });
      },
      error: () => {
        this.errorMessage = 'Failed to load interviews.';
        this.isLoading = false;
      }
    });
  }

  onSubmit() {
    if (this.scheduleForm.invalid) return;

    this.isSaving = true;
    const formValue = this.scheduleForm.value;
    formValue.scheduled_time = new Date(formValue.scheduled_time).toISOString();

    this.recruiterService.scheduleInterview(formValue).subscribe({
      next: (newInterview) => {
        // Refresh data
        this.loadData();
        this.isSaving = false;
        this.showScheduleForm = false;
        this.scheduleForm.reset({ round_name: 'Technical Round 1' });
      },
      error: (err) => {
        this.isSaving = false;
        this.errorMessage = err.error?.detail || 'Failed to schedule interview.';
      }
    });
  }

  updateVerdict(interviewId: number, verdict: string) {
    this.recruiterService.updateInterview(interviewId, { verdict }).subscribe({
      next: () => {
        const i = this.interviews.find(x => x.id === interviewId);
        if (i) i.verdict = verdict;
      }
    });
  }
}
