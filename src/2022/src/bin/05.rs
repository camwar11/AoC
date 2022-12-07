use std::{collections::VecDeque};

use advent_of_code::parsers::*;

use nom::{
    self, 
    character::complete::{none_of}, bytes::complete::{take}, error::{Error, ParseError}
};

type ParsedLine<'a> = (Vec<VecDeque<char>>, Vec<Move>);

struct Move {
    number: usize,
    from: usize,
    to: usize
}

fn parse_cargo<'a, 'b>(line: &'a str, stacks: &'a mut Vec<VecDeque<char>>) -> Result<bool, nom::Err<nom::error::Error<&'a str>>> where 'b: 'a{
    if !line.contains('[') {
        return Ok(false)
    }
    
    let (_, value) = many1(terminated(take(3usize),opt(none_of("["))))(line)?;
    let mut idx = 1;
    for cr in value {
        match cr.chars().nth(1) {
            Some(char) => {
                while stacks.len() <= idx {
                    stacks.push(VecDeque::new());
                }
                if char.is_alphabetic()
                {
                    stacks[idx].push_front(char);
                }
            },
            None => {
                panic!("Bad input")
            }
        }
        idx += 1;
    }
    Ok(true)
}

fn parse_move(line: &str) ->Result<Move, nom::Err<nom::error::Error<&str>>>{ 
    if !line.contains("move") {
        return Err(Err::Error(Error::from_error_kind(line, ErrorKind::AlphaNumeric)));
    }

    let (_, values) = tuple((preceded(tag("move "), p_str_usize), preceded(tag(" from "), p_str_usize), preceded(tag(" to "), p_str_usize)))(line)?;

    Ok(Move {
        number: values.0,
        from: values.1,
        to: values.2
    })
}

fn parse_lines(input: &str) -> ParsedLine {
    let mut stacks = Vec::new();
    let mut moves = Vec::new();
    let mut on_moves = false;
    for line in input.lines() {
        if on_moves {
            match parse_move(line) {
                Ok(m) => moves.push(m),
                _ => ()
            };
        }

        let result = parse_cargo(line,  &mut stacks).unwrap();
        if !result {
            on_moves = true;
        }
    }

    (stacks, moves)
}

fn make_moves_9000(parsed: &mut ParsedLine) -> String {
    for single in &parsed.1 {
        for _ in 0..single.number {
            let value = parsed.0[single.from].pop_back().unwrap();
            parsed.0[single.to].push_back(value);
        }
    }

    let top_crates = parsed.0.clone().into_iter().skip(1).map(|vect| *vect.back().unwrap());
    top_crates.collect()
}

fn make_moves_9001(parsed: &mut ParsedLine) -> String {
    for single in &parsed.1 {
        let mut moved_items = Vec::new();
        for _ in 0..single.number {
            let value = parsed.0[single.from].pop_back().unwrap();
            moved_items.push(value);
        }

        for item in moved_items.iter().rev() {
            parsed.0[single.to].push_back(*item);
        }
    }


    let top_crates = parsed.0.clone().into_iter().skip(1).map(|vect| *vect.back().unwrap());
    top_crates.collect()
}

pub fn part_one(input: &str) -> Option<String> {
    let mut parsed = parse_lines(input);

    Some(make_moves_9000(&mut parsed))
}

pub fn part_two(input: &str) -> Option<String> {
    let mut parsed = parse_lines(input);

    Some(make_moves_9001(&mut parsed))

}

fn main() {
    let input = &advent_of_code::read_file("inputs", 5);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 5);
        assert_eq!(part_one(&input), Some("CMZ".to_string()));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 5);
        assert_eq!(part_two(&input), Some("MCD".to_string()));
    }
}
