import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService } from '../../../core/services/admin.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-selection-board',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './selection-board.component.html',
  styleUrl: './selection-board.component.scss'
})
export class SelectionBoardComponent implements OnInit {
  placements: any[] = [];
  isLoading = true;
  errorMessage = '';

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData() {
    this.isLoading = true;
    this.adminService.getPlacements().subscribe({
      next: (data) => {
        this.placements = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load placement records.';
        this.isLoading = false;
      }
    });
  }
}
