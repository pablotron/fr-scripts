//! t
//! Fetch FedRAMP trivia (fedramp.gov/trivia) questions and answers,
//! then print them to standard output as a CSV.
//!
//! # Example
//!
//! ```sh
//! # save answers to answers.csv
//! cargo run > answers.csv
//! ```
#![deny(unsafe_code)]
use std::error::Error;
use serde::Deserialize;
use regex::Regex;
use url::Url;
use ureq::Agent;

/// Base URL
const BASE_URL: &str = "https://www.fedramp.gov/";

/// Regular expressions.
const RS: [&str; 3] = [r#"(?ms)^.+<link href="(([^"]+)/10\d\.([^"]+).js)" rel="modulepreload">.+$"#, r#"(?ms)^.+JSON.parse\(`(.+?)`\).+$"#, r#"(?ms)\\\\"#];

#[derive(Deserialize)]
struct Clue {
  value: u32,
  clue: String,
  response: String,
}

#[derive(Deserialize)]
struct Section {
  name: String,
  // description: String,
  clues: Vec<Clue>,
}

/// Fetch URL, then return matching text
fn grab(agent: &Agent, base_url: &Url, path: &str, re: &Regex) -> Result<String, Box<dyn Error>> {
  let url = base_url.join(path)?;
  let body = agent.get(url.as_ref()).call()?.body_mut().read_to_string()?;
  Ok(re.captures(&body).unwrap()[1].to_string())
}

/// Scrape questions and answers from FedRAMP trivia page.
fn scrape() -> Result<Vec<Section>, Box<dyn Error>> {
  let rs = RS.map(|s| Regex::new(s).unwrap()); // parse regexes
  let base_url = Url::parse(BASE_URL)?; // parse base URL
  let agent = ureq::agent(); // create agent
  let raw_data = grab(&agent, &base_url, &grab(&agent, &base_url, "/trivia/", &rs[0])?, &rs[1])?;
  let data = rs[2].replace_all(&raw_data, "\\");

  let sections: Vec<Section> = serde_json::from_str(&data)?;
  Ok(sections)
}

fn main() -> Result<(), Box<dyn Error>> {
  let mut w = csv::Writer::from_writer(std::io::stdout()); // create csv writer
  w.write_record(["topic", "score", "clue", "response"])?; // write headers
  for s in scrape()? {
    for c in s.clues {
		  w.write_record([&s.name, &c.value.to_string(), &c.clue, &c.response])?; // write row
    }
  }
  w.flush()?; // flush output
  Ok(()) 
}
