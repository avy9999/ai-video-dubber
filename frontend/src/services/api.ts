import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});


export async function getJobStatus(jobId: string) {

    const response = await api.get(
        `/jobs/${jobId}`
    );

    return response.data;
}


export function getDownloadUrl(jobId: string) {

    return `http://localhost:8000/videos/download/${jobId}`;

}


export default api;