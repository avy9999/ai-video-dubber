from dataclasses import dataclass, field
from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    id: str
    filename: str
    status: JobStatus
    progress: int
    transcript: list = field(default_factory=list)
    output_video: str | None = None