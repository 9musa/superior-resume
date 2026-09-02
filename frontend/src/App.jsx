import { useState } from 'react'
import { superiorResume, getJobResult, getDownloadUrl } from "./api";
import AuthForm from "./components/AuthForm"
import AuthModal from "./components/AuthModal"
import AccountMenu from "./components/AccountMenu"
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [jobDesc, setJobDesc] = useState("")
  const [jobId, setJobId] = useState(null)
  const [jobStatus, setJobStatus] = useState(null)
  const [error, setError] = useState(null)
  const [authModal, setAuthModal] = useState(false)
  const [authMode, setAuthMode] = useState("login")

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)

    if (!file) {
      setError("Please select a resume file to upload.")
      return
    }

    if (!jobDesc) {
      setError("Please enter a job description.")
      return
    }

    try {
      const token = localStorage.getItem("access_token")
      const res = await superiorResume(file, jobDesc, token)
      setJobId(res.job_id)
      setJobStatus(res.status)
      pollJobStatus(res.job_id)
    } catch (err) {
      setError(err.message)
    }
  }

  async function pollJobStatus(jobId) {
    const interval = setInterval(async () => {
      const job = await getJobResult(jobId)
      setJobStatus(job.status)
      if (job.status === "done" || job.status === "failed") {
        clearInterval(interval);
      }
    }, 2000)
  }

  function openAuth(mode) {
    setAuthMode(mode)
    setAuthModal(true)
  }

  return (
    <div className="app-container">
      <div>
        <h1>Superior Resume</h1>
        <AccountMenu onOpenAuth={openAuth} />
        {authModal && (
          <AuthModal mode={authMode} onClose={() => setAuthModal(false)} />
        )}
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <textarea
            placeholder="Job description"
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
          />
          <p className={`error-slot ${error ? "visible" : ""}`}>{error}</p>
          <button type="submit">Go</button>
        </form>
        <div id="result-section">
          {jobStatus && <p>Status: {jobStatus}</p>}
          {jobStatus === "done" && (
            <a href={getDownloadUrl(jobId)} download>Download PDF</a>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
