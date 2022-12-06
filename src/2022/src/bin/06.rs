use std::collections::HashSet;

use advent_of_code::parsers::*;

use nom::{
    self, 
     sequence::separated_pair, character::{complete::{char}, is_alphabetic}, bytes::complete::take_while
};
use queue::Queue;

type ParsedLine<'a> = u32;

fn parse_line(line: &str, length: usize) -> Result<ParsedLine, nom::Err<nom::error::Error<&str>>>{
    let mut queue = Queue::new();
    let mut idx = 0;
    for char in line.chars() {
        idx += 1;
        if queue.len() == length {
            queue.dequeue();
        }
        queue.queue(char).unwrap();
        
        if queue.len() < length {
            continue;
        }

        let mut found = HashSet::new();
        let mut is_marker = true;
        for item in queue.vec() {
            if found.contains(item) {
                is_marker = false;
                break;
            }
            found.insert(*item);
        }

        if is_marker {
            return Ok(idx);
        }
    };

    Ok(0)
}

fn parse_lines(input: &str, length: usize) -> Vec<ParsedLine> {
    let mut parsed = Vec::new();
    for line in input.lines() {
        parsed.push(parse_line(line, length).unwrap());
    }

    parsed
}

pub fn part_one(input: &str) -> Option<u32> {
    let parsed = parse_lines(input, 4);

    Some(*parsed.first().unwrap())
}

pub fn part_two(input: &str) -> Option<u32> {
    let parsed = parse_lines(input, 14);

    Some(*parsed.first().unwrap())
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 6);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 6);
        assert_eq!(part_one(&input), Some(7));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 6);
        assert_eq!(part_two(&input), Some(19));
    }
}
