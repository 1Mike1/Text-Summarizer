from fastapi import APIRouter
from models import TranscriptRequest, BatchTranscriptRequest
from summarizer import summarize_transcript, summarize_batch_transcripts

router = APIRouter()

@router.post("/summarize")
async def summarize(req: TranscriptRequest):
    input_text = req.transcript.strip()
    if not input_text:
        return {"error": "Empty transcript provided."}
    return {"summary": summarize_transcript(input_text)}

@router.post("/summarize/batch")
async def summarize_batch(req: BatchTranscriptRequest):
    summaries = summarize_batch_transcripts(req.transcripts)
    return {"summaries": summaries}
