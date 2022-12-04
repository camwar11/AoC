use std::collections::HashSet;

type ParsedLine = RuckSack;

struct RuckSack {
    first: Compartment,
    second: Compartment
}

impl RuckSack {
    fn priority(item: char) -> u32 {
        let lower = 'a' as u32 - 1;
        let upper = 'A' as u32 - 27;
        match item.is_uppercase() {
            true => item as u32 - upper,
            false => item as u32 - lower
        }
    }

    fn common(&self) -> u32 {
        let mut total = 0;
        for value in self.first.contents.intersection(&self.second.contents) {
            total += Self::priority(*value);
        }
        total
    }

    fn find_badge(&self, two: &RuckSack, three: &RuckSack) -> u32 {
        let mut total = 0;
        let sets = vec![self.all_items(), two.all_items(), three.all_items()];

        let badge_set = advent_of_code::helpers::intersection_full(sets).unwrap();

        for value in badge_set{
            total += Self::priority(value);
        }
        total
    }

    fn all_items(&self) -> HashSet<char> {
        let mut set = HashSet::new();
        set.extend(self.first.contents.clone());
        set.extend(self.second.contents.clone());
        set
    }
}

struct Compartment {
    contents: HashSet<char>
}

fn parse_line(line: &str) -> ParsedLine {
    let chars: Vec<char> = line.chars().collect();
    let half = chars.len() / 2;
    let first_half = &chars[..half];
    let second_half = &chars[half..];

    let mut first = Compartment {
        contents: HashSet::new()
    };

    first.contents.extend(first_half);

    let mut second = Compartment {
        contents: HashSet::new()
    };
    second.contents.extend(second_half);

    RuckSack {
        first: first,
        second: second
    }
}

fn parse_lines(input: &str) -> Vec<ParsedLine> {
    let mut parsed = Vec::new();
    for line in input.lines() {
        parsed.push(parse_line(line));
    }

    parsed
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut result = 0;
    let parsed = parse_lines(input);

    for rucksack in parsed {
        result += rucksack.common()
    }

    Some(result)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut result = 0;
    let parsed = parse_lines(input);

    for rucksacks in parsed.chunks_exact(3) {
        result += rucksacks[0].find_badge(&rucksacks[1], &rucksacks[2]);
    }
    Some(result)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 3);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 3);
        assert_eq!(part_one(&input), Some(157));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 3);
        assert_eq!(part_two(&input), Some(70));
    }
}
