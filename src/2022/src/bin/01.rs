pub fn part_one(input: &str) -> Option<u32> {
    let mut current_value = 0;
    let mut largest = 0u32;
    for line in input.lines() {
        if line.is_empty() {
            if current_value > largest {
                largest = current_value;
            }
            current_value = 0;
            continue;
        }

        let calories: u32 = line.parse().unwrap();
        current_value += calories;
    }

    Some(largest)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut current_value = 0;
    let mut values = std::collections::BTreeSet::new();
    for line in input.lines() {
        if line.is_empty() {
            values.insert(current_value);
            current_value = 0;
            continue;
        }

        let calories: u32 = line.parse().unwrap();
        current_value += calories;
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
