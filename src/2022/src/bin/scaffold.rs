/*
 * This file contains template code.
 * There is no need to edit this file unless you want to change template functionality.
 */
use std::{
    io::Write,
    process,
};

use advent_of_code::helpers::open_in_code;

const MODULE_TEMPLATE: &str = r###"use advent_of_code::parsers::*;

use nom::{
    self, 
     sequence::separated_pair, character::complete::{char}
};

type ParsedLine<'a> = (u32, u32);

fn parse_line(line: &str) -> Result<ParsedLine, nom::Err<nom::error::Error<&str>>>{
    let (_, pair) = separated_pair(p_str_u32, char(','), p_str_u32)(line)?;
    Ok(pair)
}

fn parse_lines(input: &str) -> Vec<ParsedLine> {
    let mut parsed = Vec::new();
    for line in input.lines() {
        parsed.push(parse_line(line).unwrap());
    }

    parsed
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut result = 0;
    let mut parsed = parse_lines(input);

    //Some(result)
    None
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut result = 0;
    let mut parsed = parse_lines(input);

    //Some(result)
    None
}

fn main() {
    let input = &advent_of_code::read_file("inputs", DAY);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", DAY);
        assert_eq!(part_one(&input), Some(0));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", DAY);
        assert_eq!(part_two(&input), Some(0));
    }
}
"###;

fn parse_args() -> Result<u8, pico_args::Error> {
    let mut args = pico_args::Arguments::from_env();
    args.free_from_str()
}

fn main() {
    let day = match parse_args() {
        Ok(day) => day,
        Err(_) => {
            eprintln!("Need to specify a day (as integer). example: `cargo scaffold 7`");
            process::exit(1);
        }
    };

    let day_padded = format!("{:02}", day);

    let input_path = format!("src/inputs/{}.txt", day_padded);
    let example_path = format!("src/examples/{}.txt", day_padded);
    let module_path = format!("src/bin/{}.rs", day_padded);

    let mut file = match advent_of_code::helpers::safe_create_file(&module_path) {
        Ok(file) => file,
        Err(e) => {
            eprintln!("Failed to create module file: {}", e);
            process::exit(1);
        }
    };

    match file.write_all(MODULE_TEMPLATE.replace("DAY", &day.to_string()).as_bytes()) {
        Ok(_) => {
            println!("Created module file \"{}\"", &module_path);
        }
        Err(e) => {
            eprintln!("Failed to write module contents: {}", e);
            process::exit(1);
        }
    }

    match advent_of_code::helpers::create_file(&input_path) {
        Ok(_) => {
            println!("Created empty input file \"{}\"", &input_path);
        }
        Err(e) => {
            eprintln!("Failed to create input file: {}", e);
            process::exit(1);
        }
    }

    match advent_of_code::helpers::create_file(&example_path) {
        Ok(_) => {
            println!("Created empty example file \"{}\"", &example_path);
        }
        Err(e) => {
            eprintln!("Failed to create example file: {}", e);
            process::exit(1);
        }
    }

    println!("---");
    println!(
        "🎄 Type `cargo solve {}` to run your solution.",
        &day_padded
    );

    open_in_code(&module_path);
    open_in_code(&example_path);
}
