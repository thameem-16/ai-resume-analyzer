import { useState } from "react"
import { login, register } from "../api"
import { Button } from "./ui/button"

export function LoginView({ onAuthenticated }) {
  const [isRegister, setIsRegister] = useState(false)
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [email, setEmail] = useState("")
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const token = isRegister
        ? await register(username, password, email)
        : await login(username, password)

      localStorage.setItem("token", token)
      onAuthenticated()
    } catch (err) {
      const message =
        err.response?.data?.error ||
        err.message ||
        "Something went wrong. Please try again."
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto w-full max-w-sm">
      <h1 className="mb-6 text-center text-2xl font-bold text-foreground">
        {isRegister ? "Create an account" : "Log in"}
      </h1>

      <form onSubmit={handleSubmit} className="space-y-4 rounded-2xl border border-border bg-card p-6 shadow-sm">
        <div>
          <label className="mb-1 block text-sm font-medium text-foreground">Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="w-full rounded-lg border border-input bg-secondary/30 px-3 py-2 text-sm outline-none focus:border-primary"
          />
        </div>

        {isRegister && (
          <div>
            <label className="mb-1 block text-sm font-medium text-foreground">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-input bg-secondary/30 px-3 py-2 text-sm outline-none focus:border-primary"
            />
          </div>
        )}

        <div>
          <label className="mb-1 block text-sm font-medium text-foreground">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full rounded-lg border border-input bg-secondary/30 px-3 py-2 text-sm outline-none focus:border-primary"
          />
        </div>

        {error && <p className="text-sm font-medium text-destructive">{error}</p>}

        <Button type="submit" disabled={loading} className="w-full">
          {loading ? "Please wait…" : isRegister ? "Register" : "Log in"}
        </Button>

        <button
          type="button"
          onClick={() => setIsRegister(!isRegister)}
          className="w-full text-center text-sm text-muted-foreground underline"
        >
          {isRegister ? "Already have an account? Log in" : "Need an account? Register"}
        </button>
      </form>
    </div>
  )
}