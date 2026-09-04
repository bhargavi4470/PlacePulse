import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentService } from '../../../core/services/student.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-interviews',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './interviews.component.html',
  styleUrl: './interviews.component.scss'
})
export class InterviewsComponent implements OnInit {
  interviews: any[] = [];
  isLoading = true;
  errorMessage = '';

  constructor(private studentService: StudentService) {}

  ngOnInit(): void {
    this.loadInterviews();
  }

  loadInterviews() {
    this.isLoading = true;
    this.studentService.getInterviews().subscribe({
      next: (data) => {
        this.interviews = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load interviews.';
        this.isLoading = false;
      }
    });
  }
}
