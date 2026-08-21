import { useState } from "react"
import { uploadResume, submitJobDescription, runAnalysis } from "./api"
import { UploadView } from "./components/upload-view"
import { ResultsView } from "./components/results-view"

function mapAnalysis(data) {
  const feedbackText = data.ai_feedback || ""
  const feedback = feedbackText
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)

  return {
    matchScore: data.match_score ?? 0,
    missingKeywords: data.missing_keywords ?? [],
    feedback: feedback.length > 0 ? feedback : ["No feedback available."],
  }
}

function App() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [analysis, setAnalysis] = useState(null)

  async function onAnalyze(file, jobDescription) {
    setError(null)
    setLoading(true)

    try {
      const resumeId = await uploadResume(file)
      const jdId = await submitJobDescription(jobDescription)
      const result = await runAnalysis(resumeId, jdId)
      setAnalysis(mapAnalysis(result))
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.response?.data?.file?.[0] ||
        err.message ||
        "Something went wrong. Please try again."
      setError(typeof message === "string" ? message : "Something went wrong. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  function handleReset() {
    setAnalysis(null)
    setError(null)
  }

  return (
    <main className="min-h-screen px-4 py-10 sm:px-6 sm:py-16">
      {analysis ? (
        <ResultsView analysis={analysis} onReset={handleReset} />
      ) : (
        <UploadView onAnalyze={onAnalyze} loading={loading} error={error} />
      )}
    </main>
  )
}

export default App
