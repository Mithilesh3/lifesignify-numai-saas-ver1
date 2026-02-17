import { useState } from "react"
import { useAuth } from "../../context/AuthContext"

const LoginPage = () => {
  const { login } = useAuth()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = async (e: any) => {
    e.preventDefault()
    await login(email, password)
    window.location.href = "/"
  }

  return (
    <div className="h-screen flex items-center justify-center bg-black text-white">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-900 p-8 rounded-xl w-96 shadow-xl"
      >
        <h1 className="text-2xl font-bold mb-6 text-center">
          Life Signify Login
        </h1>

        <input
          type="email"
          placeholder="Email"
          className="w-full p-3 mb-4 bg-gray-800 rounded"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 mb-4 bg-gray-800 rounded"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          type="submit"
          className="w-full p-3 bg-purple-600 hover:bg-purple-700 rounded"
        >
          Login
        </button>
      </form>
    </div>
  )
}

export default LoginPage
