use std::ops::RangeInclusive;

type ParsedLine<'a> = (RangeInclusive<u32>, RangeInclusive<u32>);

fn parse_line(line: &str) -> ParsedLine {
    let (elf1, elf2) = line.split_once(',').unwrap();
    let (min1, max1) = elf1.split_once('-').unwrap();
    let (min2, max2) = elf2.split_once('-').unwrap();

    let range1 = RangeInclusive::new(
        min1.parse().unwrap(),
        max1.parse().unwrap()
    );
    let range2 = RangeInclusive::new(
        min2.parse().unwrap(),
        max2.parse().unwrap()
    );
    (range1, range2)
}

fn parse_lines(input: &str) -> Vec<ParsedLine> {
    let mut parsed = Vec::new();
    for line in input.lines() {
        parsed.push(parse_line(line));
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
