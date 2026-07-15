//! Scrape rule IDs and KSI IDs for 20x classes and write them to
//! standard output as a CSV file.
//!
//! # Example
//!
//! ```sh
//! # scrape IDs, save to "ids.csv"
//! $ cargo run > ids.csv
//! ```
#![deny(unsafe_code)]
use std::error::Error;
use scraper::{Html, Selector};
use url::Url;

/// base URL
const BASE_URL: &str = "https://www.fedramp.gov/20x/";

/// CSS selectors
const CSS: [&str; 3] = [r"article.certification-card h3 a[href]", r#"table td a[href], nav.md-nav[data-md-level="3"][aria-expanded="true"] a[href$="/related/"], nav.md-nav[data-md-level="3"][aria-expanded="true"] a[href$="/key-security-indicators/"]"#, r#"summary"#];

/// ID match (class, rule/KSI ID, URL).
struct Match(char, String, Url);

/// Fetch URL, parse as HTML document.
fn get<T: AsRef<str>>(agent: &ureq::Agent, url: T) -> Result<Html, Box<dyn Error>> {
  let html = agent.get(url.as_ref()).call()?.body_mut().read_to_string()?;
  Ok(Html::parse_document(&html))
}

/// Return inner HTML of element.
fn text(e: scraper::ElementRef) -> String {
  e.text().collect()
}

/// Scrape URL, return matches.
fn scrape(base_url: &str) -> Result<Vec<Match>, Box<dyn Error>> {
  let css = CSS.map(|s| Selector::parse(s).unwrap()); // parse css selectors
  let agent = ureq::agent(); // create agent

  // find matches
  let mut matches = Vec::new();
  for a in get(&agent, base_url)?.select(&css[0]) {
    if let (Some(a_last), Some(a_href)) = (text(a).chars().last(), a.attr("href")) && let Some(a_url) = Url::parse(a_href).ok() {
      for c_url in get(&agent, &a_url)?.select(&css[1]).filter_map(|b| b.attr("href")).filter_map(|b_href| a_url.join(b_href).ok()) {
        for c_text in get(&agent, &c_url)?.select(&css[2]).map(text).filter(|c| c.len() == 11) {
          matches.push(Match(a_last, c_text, c_url.clone()));
        }
      }
    }
  }

  Ok(matches)
}

fn main() -> Result<(), Box<dyn Error>> {
  let mut w = csv::Writer::from_writer(std::io::stdout()); // create writer
  w.write_record(["class", "id", "url"])?; // write headers
  for m in scrape(BASE_URL)? {
		w.write_record([m.0.to_string(), m.1, m.2.to_string()])?; // write row
  }
  Ok(w.flush()?) // flush output
}
