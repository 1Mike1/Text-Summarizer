use actix_web::{App, HttpServer};
mod routes;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .configure(routes::init_routes) // Include routes
    })
    .bind("127.0.0.1:8080")? // Bind to localhost and port 8080
    .run()
    .await
}