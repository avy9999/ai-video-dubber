def merge_speakers(speakers, whisper_segments):
    merged = []

    for segment in whisper_segments:
        best_speaker = None
        max_overlap = 0

        seg_start = segment["start"]
        seg_end = segment["end"]

        for speaker in speakers:
            overlap = min(seg_end, speaker["end"]) - max(seg_start, speaker["start"])

            if overlap > max_overlap:
                max_overlap = overlap
                best_speaker = speaker["speaker"]

        merged.append(
            {
                "speaker": best_speaker,
                "start": seg_start,
                "end": seg_end,
                "text": segment["text"].strip(),
            }
        )

    return merged