import { useState } from "react"
import { login, signup } from "../api"


function AuthForm({ mode, onClose }) {
    const [email, setEmail] = useState("")
    const [pass, setPass] = useState("")
    const [authorized, setAuthorized] = useState(false)
    const [error, setError] = useState("")
    const modeLabels = {
        login: "Log In",
        signup: "Sign Up",
    }

    async function handleSubmit(e) {
        e.preventDefault()
        let res
        try {
            if (mode == "login") {
                res = await login(email, pass)
            } else {
                res = await signup(email, pass)
            }
            localStorage.setItem("access_token", res.access_token)
            setAuthorized(true)
            onClose()
        } catch (err) {
            setError(err.message)
        }
        
    }

    return (
        <>
        <form id="auth-form" onSubmit={handleSubmit}>
            <div className="auth-form">
                <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="johndoe@example.com" required></input>
                <input type="password" id="pass" value={pass} onChange={(e) => setPass(e.target.value)} placeholder="password" required></input>
                <button type="submit">{modeLabels[mode]}</button>
            </div>
        </form>
        {error && <p style={{ color: "red" }}>{error}</p>}
        </>
    )
}

export default AuthForm