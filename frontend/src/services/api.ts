import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
    baseURL: API_URL,
});

export async function getJobStatus(jobId: string) {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
}

export function getDownloadUrl(jobId: string) {
    return `${API_URL}/videos/download/${jobId}`;
}

export default api;