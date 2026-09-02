const API_URL = import.meta.env.VITE_API_URL


export async function signup(email, password) {
    const res = await fetch(`${API_URL}/auth/signup`, { // why res?
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    })
    if (!res.ok) throw new Error("Signup failed")
    return res.json()
}

export async function login(email, password) {
    const res = await fetch(`${API_URL}/auth/login`, { // why res?
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    })
    if (!res.ok) throw new Error("Login failed")
    return res.json()
}

export async function superiorResume(file, jobDesc, token) {
    const formData = new FormData()
    formData.append("resume_file", file)
    formData.append("job_desc", jobDesc)

    const headers = {}
    if (token) headers["Authorization"] = `Bearer ${token}`

    const res = await fetch(`${API_URL}/superior`, {
        method: "POST",
        headers,
        body: formData,
    })

    if (!res.ok) {
        const errorBody = await res.json().catch(() => null);
        throw new Error(errorBody?.message || "Upload failed");
    }

    return res.json()
}

export async function getJobResult(jobId) {
    const res = await fetch(`${API_URL}/superior/${jobId}`)
    if (!res.ok) throw new Error("Failed to fetch job status")
    return res.json()
}

export function getDownloadUrl(jobId, template="classic") {
    return `${API_URL}/superior/${jobId}/download?template=${template}`
}