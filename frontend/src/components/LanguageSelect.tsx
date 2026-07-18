interface LanguageSelectProps {
    sourceLanguage: string;
    targetLanguage: string;
    onSourceChange: (value: string) => void;
    onTargetChange: (value: string) => void;
}

const languages = [
    { value: "english", label: "English" },
    { value: "spanish", label: "Spanish" },
    { value: "hindi", label: "Hindi" },
    { value: "french", label: "French" },
];

export default function LanguageSelect({
    sourceLanguage,
    targetLanguage,
    onSourceChange,
    onTargetChange,
}: LanguageSelectProps) {
    return (
        <div className="rounded-xl bg-slate-800 p-6 shadow-lg">
            <h2 className="text-xl font-semibold mb-6">
                Language Settings
            </h2>

            <div className="grid gap-6 md:grid-cols-2">
                <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                        Source Language
                    </label>

                    <select
                        value={sourceLanguage}
                        onChange={(e) => onSourceChange(e.target.value)}
                        className="w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    >
                        {languages.map((language) => (
                            <option
                                key={language.value}
                                value={language.value}
                            >
                                {language.label}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                        Target Language
                    </label>

                    <select
                        value={targetLanguage}
                        onChange={(e) => onTargetChange(e.target.value)}
                        className="w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    >
                        {languages.map((language) => (
                            <option
                                key={language.value}
                                value={language.value}
                            >
                                {language.label}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
        </div>
    );
}