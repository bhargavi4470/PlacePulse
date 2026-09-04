import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentService } from '../../../core/services/student.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-drives',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './drives.component.html',
  styleUrl: './drives.component.scss'
})
export class DrivesComponent implements OnInit {
  drives: any[] = [];
  isLoading = true;
  errorMessage = '';
  applyingTo: number | null = null;
  applySuccess = '';

  constructor(private studentService: StudentService) {}

  ngOnInit(): void {
    this.loadDrives();
  }

  loadDrives() {
    this.isLoading = true;
    this.studentService.getDrives().subscribe({
      next: (data) => {
        this.drives = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load placement drives.';
        this.isLoading = false;
      }
    });
  }

  apply(driveId: number) {
    this.applyingTo = driveId;
    this.errorMessage = '';
    this.applySuccess = '';

    this.studentService.applyForDrive(driveId).subscribe({
      next: () => {
        this.applyingTo = null;
        this.applySuccess = 'Successfully applied!';
        setTimeout(() => this.applySuccess = '', 3000);
      },
      error: (err) => {
        this.applyingTo = null;
        this.errorMessage = err.error?.detail || 'Failed to apply.';
        setTimeout(() => this.errorMessage = '', 3000);
      }
    });
  }
}
