import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { User } from '@/types';
import { authApi } from '@/services/api/auth';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('t2a_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('t2a_token'));
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function initAuth() {
      const storedToken = localStorage.getItem('t2a_token');
      if (storedToken) {
        try {
          const userData = await authApi.getMe();
          setUser(userData);
          localStorage.setItem('t2a_user', JSON.stringify(userData));
        } catch {
          localStorage.removeItem('t2a_token');
          localStorage.removeItem('t2a_user');
          setUser(null);
          setToken(null);
        }
      }
      setLoading(false);
    }
    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const res = await authApi.login({ email, password });
    localStorage.setItem('t2a_token', res.token.access_token);
    localStorage.setItem('t2a_user', JSON.stringify(res.user));
    setToken(res.token.access_token);
    setUser(res.user);
  };

  const register = async (name: string, email: string, password: string) => {
    const res = await authApi.register({ name, email, password });
    localStorage.setItem('t2a_token', res.token.access_token);
    localStorage.setItem('t2a_user', JSON.stringify(res.user));
    setToken(res.token.access_token);
    setUser(res.user);
  };

  const logout = () => {
    localStorage.removeItem('t2a_token');
    localStorage.removeItem('t2a_user');
    setToken(null);
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
