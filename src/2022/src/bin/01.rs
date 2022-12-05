use advent_of_code::parsers::*;

use nom::{
    self
};

type ParsedLine<'a> = Option<u32>;

fn parse_line(line: &str) -> Result<ParsedLine, nom::Err<nom::error::Error<&str>>>{
    match p_str_u32(line) {
        Ok(value) => Ok(Some(value.1)),
        Err(_) => Ok(None)
    }
}

fn parse_lines(input: &str) -> Vec<ParsedLine> {
    let mut parsed = Vec::new();
    for line in input.lines() {
        parsed.push(parse_line(line).unwrap());
    }

    parsed
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut current_value = 0;
    let mut largest = 0u32;
    for line in parse_lines(input) {
        match line {
            None => {
                if current_value > largest {
                    largest = current_value;
                }
                current_value = 0;
            },
            Some(calories) => {
                current_value += calories;
            }
        }
    }

    Some(largest)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut current_value = 0;
    let mut values = std::collections::BTreeSet::new();

    for line in parse_lines(input) {
        match line {
            None => {
                values.insert(current_value);
                current_value = 0;
            },
            Some(calories) => {
                current_value += calories;
            }
        }
    }

    Some(values.iter().rev().take(3).sum())
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 1);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_one(&input), Some(24000));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_two(&input), Some(45000));
    }
}
