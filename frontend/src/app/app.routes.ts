import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login.component';
import { DashboardComponent as StudentDashboard } from './features/student/dashboard/dashboard.component';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent) },
  
  // Student Routes
  { 
    path: 'student/dashboard', 
    component: StudentDashboard,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['STUDENT'] }
  },
  { 
    path: 'student/profile', 
    loadComponent: () => import('./features/student/profile/profile.component').then(m => m.ProfileComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['STUDENT'] }
  },
  { 
    path: 'student/drives', 
    loadComponent: () => import('./features/student/drives/drives.component').then(m => m.DrivesComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['STUDENT'] }
  },
  { 
    path: 'student/applications', 
    loadComponent: () => import('./features/student/applications/applications.component').then(m => m.ApplicationsComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['STUDENT'] }
  },
  { 
    path: 'student/interviews', 
    loadComponent: () => import('./features/student/interviews/interviews.component').then(m => m.InterviewsComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['STUDENT'] }
  },

  // Admin Routes
  { 
    path: 'admin/eligibility', 
    loadComponent: () => import('./features/admin/eligibility/eligibility.component').then(m => m.EligibilityComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN'] }
  },
  { 
    path: 'admin/dashboard',
    loadComponent: () => import('./features/admin/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN'] }
  },
  { 
    path: 'admin/selection-board',
    loadComponent: () => import('./features/admin/selection-board/selection-board.component').then(m => m.SelectionBoardComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN'] }
  },

  // Recruiter Routes (Placeholder components for now, will map to real components as they are built)
  { 
    path: 'recruiter/dashboard',
    loadComponent: () => import('./features/recruiter/candidates/candidates.component').then(m => m.CandidatesComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['RECRUITER'] }
  },
  { 
    path: 'recruiter/drives', 
    loadComponent: () => import('./features/recruiter/drives/drives.component').then(m => m.DrivesComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['RECRUITER'] }
  },
  { 
    path: 'recruiter/candidates', 
    loadComponent: () => import('./features/recruiter/candidates/candidates.component').then(m => m.CandidatesComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['RECRUITER'] }
  },
  { 
    path: 'recruiter/interviews', 
    loadComponent: () => import('./features/recruiter/interviews/interviews.component').then(m => m.InterviewsComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['RECRUITER'] }
  },
  { 
    path: 'recruiter/offers', 
    loadComponent: () => import('./features/recruiter/offers/offers.component').then(m => m.OffersComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['RECRUITER'] }
  },

  // Default redirect
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login' }
];
