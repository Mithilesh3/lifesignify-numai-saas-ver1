import { createContext, useContext, useState } from "react"
import api from "../api/axios"

const AuthContext = createContext<any>(null)

export const AuthProvider = ({ children }: any) => {
  const [user, setUser] = useState<any>(null)

  const login = async (email: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append("username", email)
    formData.append("password", password)

    const response = await api.post("/users/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    })

    localStorage.setItem("access_token", response.data.access_token)

    const userRes = await api.get("/users/me")
    setUser(userRes.data)
  }

  const logout = () => {
    localStorage.removeItem("access_token")
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// 🚨 THIS MUST EXIST
export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider")
  }
  return context
}
