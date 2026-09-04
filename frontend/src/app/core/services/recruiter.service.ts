import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RecruiterService {
  private apiUrl = 'http://127.0.0.1:8000/api/recruiter';

  constructor(private http: HttpClient) { }

  getDrives(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/drives`);
  }

  createDrive(driveData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/drives`, driveData);
  }

  getApplications(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/api/applications/recruiter');
  }

  updateApplicationStatus(appId: number, status: string): Observable<any> {
    return this.http.put<any>(`http://127.0.0.1:8000/api/applications/${appId}/status`, { status });
  }

  getInterviews(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/api/interviews/recruiter');
  }

  scheduleInterview(interviewData: any): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:8000/api/interviews', interviewData);
  }

  updateInterview(interviewId: number, updates: any): Observable<any> {
    return this.http.put<any>(`http://127.0.0.1:8000/api/interviews/${interviewId}`, updates);
  }

  createOffer(applicationId: number, ctcOffered: number): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:8000/api/placements', { application_id: applicationId, ctc_offered: ctcOffered });
  }
}
