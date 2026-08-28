import { useState } from 'react'
import { superiorResume, getJobResult, getDownloadUrl } from "./api";
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [jobDesc, setJobDesc] = useState("")
  const [jobId, setJobId] = useState(null)
  const [jobStatus, setJobStatus] = useState(null)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    const token = localStorage.getItem("access_token")
    const res = await superiorResume(file, jobDesc, token)
    setJobId(res.job_id)
    setJobStatus(res.status)
    pollJobStatus(res.job_id)
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

  return (
    <>
      <div>
        <h1>Superior Resume</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <textarea
            placeholder="Job description"
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
          />
          <button type="submit">Go</button>
        </form>
        <div id="result-section">
          {jobStatus && <p>Status: {jobStatus}</p>}
          {jobStatus === "done" && (
            <a href={getDownloadUrl(jobId)} download>Download PDF</a>
          )}
        </div>
      </div>
    </>
  )
}

export default App
