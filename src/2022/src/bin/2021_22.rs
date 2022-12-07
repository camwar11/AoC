use advent_of_code::parsers::*;

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
    let input = &advent_of_code::read_file_w_year("inputs", 22, 2021);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file_w_year("examples", 22, 2021);
        assert_eq!(part_one(&input), Some(0));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file_w_year("examples", 22, 2021);
        assert_eq!(part_two(&input), Some(0));
    }
}
