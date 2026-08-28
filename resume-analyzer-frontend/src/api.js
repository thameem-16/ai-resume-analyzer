import axios from "axios"

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export async function register(username, password, email) {
  const { data } = await api.post("/api/auth/register/", {
    username,
    password,
    email,
  })
  return data.token
}

export async function login(username, password) {
  const { data } = await api.post("/api/auth/login/", {
    username,
    password,
  })
  return data.token
}

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