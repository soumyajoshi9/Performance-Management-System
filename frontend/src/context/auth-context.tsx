"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { User, UserRole } from "@/types";
import { apiClient } from "@/lib/api-client";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, role?: UserRole) => Promise<void>;
  logout: () => void;
  switchRole: (role: UserRole) => Promise<void>;
}

const DEMO_USERS: Record<UserRole, { email: string; pass: string }> = {
  EMPLOYEE: { email: "employee@vyora.local", pass: "EmployeePass123!" },
  MANAGER: { email: "manager@vyora.local", pass: "ManagerPass123!" },
  HR: { email: "hr@vyora.local", pass: "HrPass123!" },
  ADMIN: { email: "admin@vyora.local", pass: "AdminPass123!" },
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  isLoading: true,
  login: async () => {},
  logout: () => {},
  switchRole: async () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("vyora_access_token");
    const savedUser = localStorage.getItem("vyora_user");
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    } else {
      // Auto-load demo employee if first visit
      login("employee@vyora.local", "EMPLOYEE").catch(() => {});
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, role?: UserRole) => {
    setIsLoading(true);
    try {
      const targetRole = role || "EMPLOYEE";
      const pass = DEMO_USERS[targetRole]?.pass || "EmployeePass123!";
      const res = await apiClient.post("/auth/login", { email, password: pass });
      const { access_token, user: userData } = res.data;
      
      setToken(access_token);
      setUser(userData);
      localStorage.setItem("vyora_access_token", access_token);
      localStorage.setItem("vyora_user", JSON.stringify(userData));
    } catch (err) {
      console.error("Login failed:", err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("vyora_access_token");
    localStorage.removeItem("vyora_user");
  };

  const switchRole = async (newRole: UserRole) => {
    const demo = DEMO_USERS[newRole];
    if (demo) {
      await login(demo.email, newRole);
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout, switchRole }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
