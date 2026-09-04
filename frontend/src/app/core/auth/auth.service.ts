import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';

export interface AuthResponse {
  access_token: string;
  token_type: string;
  role: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000/api/auth';
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  private currentRoleSubject = new BehaviorSubject<string | null>(null);
  public currentRole$ = this.currentRoleSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) { 
    this.loadUserFromStorage();
  }

  private loadUserFromStorage() {
    const token = localStorage.getItem('access_token');
    const role = localStorage.getItem('user_role');
    if (token && role) {
      this.currentRoleSubject.next(role);
      this.fetchCurrentUser().subscribe({
        error: () => this.logout() // If token invalid, logout
      });
    }
  }

  login(username: string, password: string): Observable<AuthResponse> {
    const body = new URLSearchParams();
    body.set('username', username);
    body.set('password', password);
    
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, body.toString(), {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    }).pipe(
      tap(response => {
        localStorage.setItem('access_token', response.access_token);
        localStorage.setItem('user_role', response.role);
        this.currentRoleSubject.next(response.role);
        this.fetchCurrentUser().subscribe();
      })
    );
  }

  register(studentData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, studentData);
  }

  fetchCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/me`).pipe(
      tap(user => {
        this.currentUserSubject.next(user);
        this.currentRoleSubject.next(user.role);
        localStorage.setItem('user_role', user.role);
      })
    );
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    this.currentUserSubject.next(null);
    this.currentRoleSubject.next(null);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getRole(): string | null {
    return this.currentRoleSubject.value || localStorage.getItem('user_role');
  }
}
