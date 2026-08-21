import { useRef, useState } from "react"
import { FileText, UploadCloud, X, Sparkles, Loader2 } from "lucide-react"
import { Button } from "./ui/button"

export function UploadView({ onAnalyze, loading, error }) {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState("")
  const [dragging, setDragging] = useState(false)
  const [localError, setLocalError] = useState(null)
  const inputRef = useRef(null)

  function selectFile(next) {
    if (!next) return
    if (next.type !== "application/pdf") {
      setLocalError("Please upload a PDF file.")
      return
    }
    setLocalError(null)
    setFile(next)
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    selectFile(e.dataTransfer.files?.[0] ?? null)
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (!file) {
      setLocalError("A PDF resume is required.")
      return
    }
    if (jobDescription.trim().length < 20) {
      setLocalError("Please paste a job description (at least 20 characters).")
      return
    }
    setLocalError(null)
    onAnalyze(file, jobDescription)
  }

  const shownError = localError ?? error

  return (
    <div className="mx-auto w-full max-w-3xl">
      <header className="mb-8 text-center">
        <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-sm font-medium text-primary">
          <Sparkles className="h-4 w-4" aria-hidden="true" />
          AI Resume Analyzer
        </div>
        <h1 className="text-balance font-display text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
          Match your resume to any job
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-pretty leading-relaxed text-muted-foreground">
          Upload your resume and paste a job description. Get an instant match score, the keywords
          you&apos;re missing, and tailored feedback.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="rounded-2xl border border-border bg-card p-6 shadow-sm sm:p-8">
        <div className="space-y-6">
          <div>
            <label className="mb-2 block text-sm font-semibold text-foreground">Resume (PDF)</label>
            <div
              onDragOver={(e) => {
                e.preventDefault()
                setDragging(true)
              }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleDrop}
              onClick={() => inputRef.current?.click()}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault()
                  inputRef.current?.click()
                }
              }}
              role="button"
              tabIndex={0}
              aria-label="Upload PDF resume by clicking or dragging a file"
              className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors ${
                dragging
                  ? "border-primary bg-accent"
                  : "border-input bg-secondary/40 hover:border-primary/60 hover:bg-accent/60"
              }`}
            >
              <input
                ref={inputRef}
                type="file"
                accept="application/pdf"
                className="sr-only"
                onChange={(e) => selectFile(e.target.files?.[0] ?? null)}
              />
              {file ? (
                <div className="flex w-full max-w-sm items-center gap-3 rounded-lg border border-border bg-card px-4 py-3 text-left">
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
                    <FileText className="h-5 w-5" aria-hidden="true" />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-sm font-medium text-foreground">{file.name}</span>
                    <span className="block text-xs text-muted-foreground">
                      {(file.size / 1024).toFixed(0)} KB · PDF
                    </span>
                  </span>
                  <button
                    type="button"
                    aria-label="Remove file"
                    onClick={(e) => {
                      e.stopPropagation()
                      setFile(null)
                      if (inputRef.current) inputRef.current.value = ""
                    }}
                    className="rounded-md p-1 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
                  >
                    <X className="h-4 w-4" aria-hidden="true" />
                  </button>
                </div>
              ) : (
                <>
                  <span className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                    <UploadCloud className="h-6 w-6" aria-hidden="true" />
                  </span>
                  <span className="text-sm font-medium text-foreground">
                    Drag &amp; drop your resume here
                  </span>
                  <span className="mt-1 text-sm text-muted-foreground">or click to browse · PDF only</span>
                </>
              )}
            </div>
          </div>

          <div>
            <label htmlFor="job-description" className="mb-2 block text-sm font-semibold text-foreground">
              Job description
            </label>
            <textarea
              id="job-description"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job description here…"
              rows={9}
              className="w-full resize-y rounded-xl border border-input bg-secondary/30 px-4 py-3 text-sm leading-relaxed text-foreground outline-none transition-colors placeholder:text-muted-foreground focus:border-primary focus:bg-card focus:ring-2 focus:ring-ring/30"
            />
          </div>

          {shownError ? (
            <p role="alert" className="text-sm font-medium text-destructive">
              {shownError}
            </p>
          ) : null}

          <Button type="submit" disabled={loading} size="lg" className="w-full text-base">
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
                Analyzing…
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5" aria-hidden="true" />
                Analyze match
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  )
}
