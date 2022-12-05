use std::ops::RangeInclusive;
use advent_of_code::parsers::p_range_inc_u32;

use nom::{
    self, 
     sequence::separated_pair, character::complete::{char}
};

type ParsedLine<'a> = (RangeInclusive<u32>, RangeInclusive<u32>);

fn parse_line(line: &str) -> Result<ParsedLine, nom::Err<nom::error::Error<&str>>>{
    let (_, pair) = separated_pair(p_range_inc_u32, char(','), p_range_inc_u32)(line)?;
    Ok(pair)
}

fn parse_lines(input: &str) -> Vec<ParsedLine> {
    let mut parsed = Vec::new();
    for line in input.lines() {
        parsed.push(parse_line(line).unwrap());
    }

    parsed
}

fn full_contained_by_other<T>(first: RangeInclusive<T>, second: RangeInclusive<T>) -> bool where T: PartialOrd{
    if first.contains(second.start()) && first.contains(second.end()) {
        true
    }
    else if second.contains(first.start()) && second.contains(first.end()){
        true
    }
    else {
        false
    }
}

fn overlap<T>(first: RangeInclusive<T>, second: RangeInclusive<T>) -> bool where T: PartialOrd{
    if first.contains(second.start()) || first.contains(second.end()) {
        true
    }
    else if second.contains(first.start()) || second.contains(first.end()){
        true
    }
    else {
        false
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut result = 0;
    let parsed = parse_lines(input);

    for pair in parsed {
        if full_contained_by_other(pair.0, pair.1) {
            result += 1;
        }
    }

    Some(result)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut result = 0;
    let parsed = parse_lines(input);

    for pair in parsed {
        if overlap(pair.0, pair.1) {
            result += 1;
        }
    }
    Some(result)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 4);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 4);
        assert_eq!(part_one(&input), Some(2));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 4);
        assert_eq!(part_two(&input), Some(4));
    }
}
