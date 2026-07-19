import { useState, useEffect } from "react";
import { Download } from "lucide-react";

import Header from "./components/Header";
import UploadCard from "./components/UploadCard";
import LanguageSelect from "./components/LanguageSelect";
import api, { getJobStatus, getDownloadUrl } from "./services/api";

export default function App() {

    const [file, setFile] = useState<File | null>(null);
    console.log("VITE_API_URL =", import.meta.env.VITE_API_URL);
    const [sourceLanguage, setSourceLanguage] = useState("english");
    const [targetLanguage, setTargetLanguage] = useState("hindi");

    const [loading, setLoading] = useState(false);

    const [jobId, setJobId] = useState("");
    const [progress, setProgress] = useState(0);
    const [status, setStatus] = useState("");


    const startDubbing = async () => {
        if (!file) {
            alert("Please choose a video.");
            return;
        }

        // reset previous job
        setJobId("");
        setProgress(0);
        setStatus("uploading");


        const formData = new FormData();

        formData.append("file", file);
        formData.append("source_language", sourceLanguage);
        formData.append("target_language", targetLanguage);


        try {
            setLoading(true);

            const response = await api.post(
                "/videos/upload",
                formData
            );

            setJobId(response.data.job_id);

        } catch (error) {
            console.error(error);
            setStatus("failed");
            alert("Upload failed.");

        } finally {
            setLoading(false);
        }
    };


    // Poll job status
    useEffect(() => {

        if (!jobId) return;


        const interval = setInterval(async () => {

            try {

                const data = await getJobStatus(jobId);

                setProgress(data.progress);
                setStatus(data.status);


                if (
                    data.status === "completed" ||
                    data.status === "failed"
                ) {
                    clearInterval(interval);
                }

            } catch (error) {
                console.error(error);
            }

        }, 2000);


        return () => clearInterval(interval);

    }, [jobId]);


    return (
        <main className="min-h-screen bg-slate-900 text-slate-100">

            <div className="mx-auto flex max-w-3xl flex-col gap-8 p-8">

                <Header />

                <UploadCard
                    file={file}
                    onFileChange={setFile}
                />


                <LanguageSelect
                    sourceLanguage={sourceLanguage}
                    targetLanguage={targetLanguage}
                    onSourceChange={setSourceLanguage}
                    onTargetChange={setTargetLanguage}
                />


                <button
                    onClick={startDubbing}
                    disabled={loading}
                    className="rounded-lg bg-blue-600 px-6 py-3 font-semibold transition hover:bg-blue-700 disabled:opacity-50"
                >
                    {
                        loading
                            ? "Uploading..."
                            : status === "processing"
                            ? "Processing..."
                            : "Start Dubbing"
                    }
                </button>


                {jobId && (

                    <div className="rounded-xl bg-slate-800 p-6">

                        <p className="text-green-400">
                            Job ID: {jobId}
                        </p>


                        <div className="mt-4 flex items-center gap-2">

                            <span className="font-medium">
                                Status:
                            </span>


                            <span
                                className={`
                                    rounded-full px-3 py-1 text-sm font-semibold
                                    ${
                                        status === "completed"
                                            ? "bg-green-600"
                                            : status === "failed"
                                            ? "bg-red-600"
                                            : "bg-blue-600"
                                    }
                                `}
                            >
                                {
                                    status.charAt(0).toUpperCase()
                                    + status.slice(1)
                                }
                            </span>

                        </div>


                        <div className="mt-4 h-5 w-full overflow-hidden rounded-full bg-slate-700">

                            <div
                                className="flex h-full items-center justify-center bg-blue-500 text-xs font-semibold transition-all duration-300"
                                style={{
                                    width: `${progress}%`
                                }}
                            >
                                {progress}%
                            </div>

                        </div>


                        {
                            status === "completed" && (

                                <div className="mt-5 rounded-lg border border-green-700 bg-green-900/30 p-4 text-green-300">
                                    ✅ Your dubbed video is ready!
                                </div>

                            )
                        }


                        {
                            status === "failed" && (

                                <div className="mt-5 rounded-lg border border-red-700 bg-red-900/30 p-4 text-red-300">
                                    ❌ Processing failed. Please try again.
                                </div>

                            )
                        }


                        {
                            status === "completed" && (

                                <a
                                    href={getDownloadUrl(jobId)}
                                    className="mt-6 flex items-center justify-center gap-2 rounded-lg bg-green-600 px-6 py-3 font-semibold hover:bg-green-700"
                                >
                                    <Download size={18} />
                                    Download Dubbed Video
                                </a>

                            )
                        }

                    </div>

                )}

            </div>

        </main>
    );
}