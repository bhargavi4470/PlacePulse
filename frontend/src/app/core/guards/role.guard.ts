import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from '../auth/auth.service';

export const roleGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  const expectedRoles: string[] = route.data['roles'] || [];
  const currentRole = authService.getRole();

  if (currentRole && expectedRoles.includes(currentRole)) {
    return true;
  }

  // Not authorized, maybe redirect to an unauthorized page or dashboard based on role
  if (currentRole === 'STUDENT') {
    return router.parseUrl('/student/dashboard');
  } else if (currentRole === 'ADMIN') {
    return router.parseUrl('/admin/dashboard');
  } else if (currentRole === 'RECRUITER') {
    return router.parseUrl('/recruiter/dashboard');
  }

  return router.parseUrl('/login');
};
