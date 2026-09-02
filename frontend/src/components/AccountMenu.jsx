import { useState } from "react"

function AccountMenu({ onOpenAuth }) {
    const [menuOpen, setMenuOpen] = useState(false)
    const isLoggedIn = !!localStorage.getItem("access_token")

    function handleLogout() {
        localStorage.removeItem("access_token")
        window.location.reload()
    }

    return (
        <div className="account-menu">
            <button onClick={() => setMenuOpen(!menuOpen)}>
                {isLoggedIn ? (
                    "Account"
                ) : (
                    <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    width="24" 
                    height="24" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                    >
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                    </svg>
                )}
            </button>

            {menuOpen && (
                <div className="dropdown">
                    {isLoggedIn ? (
                        <button onClick={handleLogout}>Log out</button>
                    ) : (
                        <>
                            <button onClick={() => { onOpenAuth("login"); setMenuOpen(false) }}>
                                Log In
                            </button>
                            <button onClick={() => { onOpenAuth("signup"); setMenuOpen(false) }}>
                                Sign Up
                            </button>
                        </>
                    )}
                </div>
            )}
        </div>
    )
}

export default AccountMenu