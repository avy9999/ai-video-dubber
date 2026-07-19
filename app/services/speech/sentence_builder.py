import re


def get_speaker(start: float, end: float, speaker_segments):
    """
    Returns the speaker with the greatest overlap.
    """

    best_speaker = "UNKNOWN"
    best_overlap = 0.0

    for segment in speaker_segments:
        overlap = min(end, segment["end"]) - max(start, segment["start"])

        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = segment["speaker"]

    return best_speaker


def build_segments(whisper_segments, speaker_segments):
    """
    Builds smaller phrase segments using Whisper word timestamps.
    """

    output = []

    punctuation = {".", "?", "!", ",", "।"}

    for segment in whisper_segments:

        words = segment.get("words", [])

        if not words:
            continue

        current_words = []

        for i, word in enumerate(words):

            current_words.append(word)

            text = word["word"].strip()

            if any(text.endswith(p) for p in punctuation):

                # Remaining words after this punctuation
                remaining = words[i + 1:]

                # Don't split on commas if only a tiny fragment remains
                if (
                    text.endswith(",")
                    and len(remaining) <= 2
                ):
                    continue

                start = float(current_words[0]["start"])
                end = float(current_words[-1]["end"])

                sentence = " ".join(
                    w["word"].strip()
                    for w in current_words
                ).strip()

                sentence = (
                    sentence
                    .replace(" -", "-")
                    .replace("- ", "-")
                )

                output.append({
                    "speaker": get_speaker(start, end, speaker_segments),
                    "start": start,
                    "end": end,
                    "text": sentence,
                })

                current_words = []

        # Remaining words
        if current_words:

            start = float(current_words[0]["start"])
            end = float(current_words[-1]["end"])

            sentence = " ".join(
                w["word"].strip()
                for w in current_words
            ).strip()

            output.append({
                "speaker": get_speaker(start, end, speaker_segments),
                "start": start,
                "end": end,
                "text": sentence,
            })

    return output