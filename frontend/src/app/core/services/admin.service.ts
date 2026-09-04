import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface EligibilityResult {
  student_id: number;
  student_name: string;
  roll_number: string;
  drive_id: number;
  drive_name: string;
  verdict: 'ELIGIBLE' | 'INELIGIBLE' | 'CONDITIONAL';
  rules_passed: any[];
  rules_failed: any[];
}

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = 'http://127.0.0.1:8000/api/admin';

  constructor(private http: HttpClient) { }

  getStudents(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/students`);
  }

  getDrives(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/drives`);
  }

  evaluateEligibility(studentId: number, driveId: number): Observable<EligibilityResult> {
    return this.http.get<EligibilityResult>(`${this.apiUrl}/eligibility/evaluate/${studentId}/${driveId}`);
  }

  getPlacements(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/api/placements/admin');
  }

  getAnalytics(): Observable<any> {
    return this.http.get<any>('http://127.0.0.1:8000/api/admin/analytics');
  }
}
