import { createContext, useContext, useState, useEffect } from "react"
import API from "../services/api"

const AuthContext = createContext<any>(null)

export const AuthProvider = ({ children }: any) => {
  const [user, setUser] = useState<any>(null)

  const fetchUser = async () => {
    try {
      const res = await API.get("/users/me")
      setUser(res.data)
    } catch {
      setUser(null)
    }
  }

  const login = async (email: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append("username", email)
    formData.append("password", password)

    const response = await API.post("/users/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })

    localStorage.setItem("access_token", response.data.access_token)

    await fetchUser()
  }

  const logout = () => {
    localStorage.removeItem("access_token")
    setUser(null)
  }

  useEffect(() => {
    if (localStorage.getItem("access_token")) {
      fetchUser()
    }
  }, [])

  return (
    <AuthContext.Provider value={{ user, login, logout, fetchUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error("useAuth must be used inside AuthProvider")
  return context
}