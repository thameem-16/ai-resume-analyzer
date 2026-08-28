import { ArrowLeft, CheckCircle2, MessageSquareText, TriangleAlert } from "lucide-react"
import { Button } from "./ui/button"
import { ScoreGauge } from "./score-gauge"

export function ResultsView({ analysis, onReset }) {
  const { matchScore, missingKeywords, feedback } = analysis

  return (
    <div className="mx-auto w-full max-w-4xl">
      <div className="mb-6 flex items-center justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-bold tracking-tight text-foreground">Analysis results</h1>
          <p className="mt-1 text-sm text-muted-foreground">How your resume stacks up against the role.</p>
        </div>
        <Button variant="outline" onClick={onReset}>
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          New analysis
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-5">
        <section
          aria-label="Match score"
          className="flex flex-col items-center justify-center rounded-2xl border border-border bg-card p-8 shadow-sm lg:col-span-2"
        >
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
            Match score
          </h2>
          <ScoreGauge score={matchScore} />
        </section>

        <section
          aria-label="Missing keywords"
          className="rounded-2xl border border-border bg-card p-6 shadow-sm sm:p-8 lg:col-span-3"
        >
          <div className="mb-4 flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-md bg-destructive/10 text-destructive">
              <TriangleAlert className="h-4 w-4" aria-hidden="true" />
            </span>
            <h2 className="font-display text-lg font-semibold text-foreground">Missing keywords</h2>
          </div>

          {missingKeywords.length > 0 ? (
            <ul className="flex flex-wrap gap-2">
              {missingKeywords.map((keyword, i) => (
                <li
                  key={`${keyword}-${i}`}
                  className="rounded-full border border-destructive/30 bg-destructive/10 px-3 py-1 text-sm font-medium text-destructive"
                >
                  {keyword}
                </li>
              ))}
            </ul>
          ) : (
            <p className="flex items-center gap-2 text-sm text-muted-foreground">
              <CheckCircle2 className="h-4 w-4 text-primary" aria-hidden="true" />
              No critical keywords missing — great coverage.
            </p>
          )}
        </section>
      </div>

      <section
        aria-label="AI feedback"
        className="mt-6 rounded-2xl border border-border bg-card p-6 shadow-sm sm:p-8"
      >
        <div className="mb-4 flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-md bg-primary/10 text-primary">
            <MessageSquareText className="h-4 w-4" aria-hidden="true" />
          </span>
          <h2 className="font-display text-lg font-semibold text-foreground">What to Do!</h2>
        </div>
        <div className="space-y-4">
          {feedback.map((paragraph, i) => (
            <p key={i} className="text-pretty leading-relaxed text-foreground/90">
              {paragraph}
            </p>
          ))}
        </div>
      </section>
    </div>
  )
}
