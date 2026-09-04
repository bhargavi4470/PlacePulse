import { Component, OnInit } from '@angular/core';
import { AuthService, User } from '../../../core/auth/auth.service';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { NotificationsDropdownComponent } from '../notifications-dropdown/notifications-dropdown.component';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule, NotificationsDropdownComponent],
  templateUrl: './topbar.component.html',
  styleUrl: './topbar.component.scss'
})
export class TopbarComponent implements OnInit {
  user$: Observable<User | null>;

  constructor(private authService: AuthService) {
    this.user$ = this.authService.currentUser$;
  }

  ngOnInit(): void {}

  logout() {
    this.authService.logout();
  }
}
