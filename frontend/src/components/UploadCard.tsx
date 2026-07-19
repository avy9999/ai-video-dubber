import { Upload } from "lucide-react";

interface UploadCardProps {
    file: File | null;
    onFileChange: (file: File | null) => void;
}

export default function UploadCard({
    file,
    onFileChange,
}: UploadCardProps) {
    return (
        <div className="rounded-xl bg-slate-800 p-6 shadow-lg">

            <h2 className="text-xl font-semibold">
                Upload Video
            </h2>

            <label className="mt-4 flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-600 p-8 transition hover:border-blue-500">

                <Upload className="mb-4 h-10 w-10 text-blue-400" />

                <span className="text-slate-300">
                    {file
                        ? file.name
                        : "Choose a video"}
                </span>

                <input
                    type="file"
                    accept="video/*"
                    className="hidden"
                    onChange={(e) =>
                        onFileChange(
                            e.target.files?.[0] ?? null
                        )
                    }
                />
            </label>

        </div>
    );
}