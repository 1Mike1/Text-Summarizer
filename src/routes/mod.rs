use actix_web::{web, HttpResponse, Scope};

pub fn init_routes(cfg: &mut web::ServiceConfig) {
    cfg.service(web::scope("/api")
        .route("/summarize", web::post().to(summarize))
        .route("/summarize/batch", web::post().to(summarize_batch)));
}

async fn summarize(req_body: web::Json<TranscriptRequest>) -> HttpResponse {
    let input_text = req_body.transcript.trim();
    if input_text.is_empty() {
        return HttpResponse::BadRequest().json("Empty transcript provided.");
    }
    let summary = summarize_transcript(input_text);
    HttpResponse::Ok().json(summary)
}

async fn summarize_batch(req_body: web::Json<BatchTranscriptRequest>) -> HttpResponse {
    let summaries = summarize_batch_transcripts(&req_body.transcripts);
    HttpResponse::Ok().json(summaries)
}

// Define the request types
#[derive(serde::Deserialize)]
struct TranscriptRequest {
    transcript: String,
}

#[derive(serde::Deserialize)]
struct BatchTranscriptRequest {
    transcripts: Vec<String>,
}

// Placeholder functions for summarization logic
fn summarize_transcript(input: &str) -> String {
    format!("Summary of: {}", input)
}

fn summarize_batch_transcripts(inputs: &[String]) -> Vec<String> {
    inputs.iter().map(|input| summarize_transcript(input)).collect()
}