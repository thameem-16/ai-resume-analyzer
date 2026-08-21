import axios from "axios"

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
})

export async function uploadResume(file) {
  const formData = new FormData()
  formData.append("file", file)

  const { data } = await api.post("/api/resumes/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  })

  return data.id
}

export async function submitJobDescription(text) {
  const { data } = await api.post("/api/job-descriptions/", {
    title: "Job Description",
    raw_text: text,
  })

  return data.id
}

export async function runAnalysis(resumeId, jdId) {
  const { data } = await api.post("/api/analyses/", {
    resume_id: resumeId,
    job_description_id: jdId,
  })

  return data
}
