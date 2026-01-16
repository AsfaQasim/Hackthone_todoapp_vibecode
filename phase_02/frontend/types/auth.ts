// types/auth.ts
export interface User {
  id: string;
  email: string;
  name: string;
}

export interface BetterAuthSession {
  user: User;
  token: string;
  expiresAt: Date;
}

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  signIn: (email: string, password: string) => Promise<boolean>;
  signUp: (email: string, password: string) => Promise<boolean>;
  signOut: () => Promise<void>;
  getSession: () => Promise<BetterAuthSession | null>;
}

export interface SignupData {
  email: string;
  password: string;
  name: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface TokenData {
  accessToken: string;
  refreshToken: string;
  expiresAt: Date;
}