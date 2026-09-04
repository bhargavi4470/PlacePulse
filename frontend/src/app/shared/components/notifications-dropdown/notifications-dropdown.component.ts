import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificationsService } from '../../../core/services/notifications.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-notifications-dropdown',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './notifications-dropdown.component.html',
  styleUrl: './notifications-dropdown.component.scss'
})
export class NotificationsDropdownComponent implements OnInit {
  notifications: any[] = [];
  unreadCount = 0;
  isOpen = false;

  constructor(private notifService: NotificationsService) {}

  ngOnInit(): void {
    this.loadNotifications();
  }

  loadNotifications() {
    this.notifService.getNotifications().subscribe((data: any[]) => {
      this.notifications = data;
      this.unreadCount = this.notifications.filter(n => !n.is_read).length;
    });
  }

  toggleDropdown() {
    this.isOpen = !this.isOpen;
    if (this.isOpen && this.unreadCount > 0) {
      this.notifService.markAllAsRead().subscribe(() => {
        this.notifications.forEach(n => n.is_read = true);
        this.unreadCount = 0;
      });
    }
  }

  markRead(id: number, event: Event) {
    event.stopPropagation();
    const notif = this.notifications.find(n => n.id === id);
    if (notif && !notif.is_read) {
      this.notifService.markAsRead(id).subscribe(() => {
        notif.is_read = true;
        this.unreadCount = Math.max(0, this.unreadCount - 1);
      });
    }
  }
}
