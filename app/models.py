from pydantic import BaseModel
from typing import List

class TranscriptRequest(BaseModel):
    transcript: str

class BatchTranscriptRequest(BaseModel):
    transcripts: List[str]

