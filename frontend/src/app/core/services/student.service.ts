import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DashboardData {
  profile: {
    full_name: string;
    roll_number: string;
    branch: string;
    graduation_year: number;
    cgpa: number;
    active_backlogs: number;
    profile_readiness: number;
  };
  metrics: {
    eligible_drives_count: number;
    active_pipeline_count: number;
    offers_count: number;
  };
}

export interface StudentProfile {
  id?: number;
  roll_number: string;
  branch: string;
  graduation_year: number;
  cgpa: number;
  active_backlogs: number;
  historical_backlogs: number;
  tenth_percentage?: number;
  twelfth_percentage?: number;
  github_username?: string;
  resume_url?: string;
  profile_readiness?: number;
}

@Injectable({
  providedIn: 'root'
})
export class StudentService {
  private apiUrl = 'http://127.0.0.1:8000/api/students';

  constructor(private http: HttpClient) { }

  getDashboardData(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.apiUrl}/me/dashboard`);
  }

  getProfile(): Observable<StudentProfile> {
    return this.http.get<StudentProfile>(`${this.apiUrl}/me`);
  }

  updateProfile(profileData: Partial<StudentProfile>): Observable<StudentProfile> {
    return this.http.put<StudentProfile>(`${this.apiUrl}/me`, profileData);
  }

  getDrives(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/api/drives');
  }

  applyForDrive(driveId: number): Observable<any> {
    return this.http.post<any>(`http://127.0.0.1:8000/api/drives/${driveId}/apply`, {});
  }

  getInterviews(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/api/interviews/student');
  }
}
