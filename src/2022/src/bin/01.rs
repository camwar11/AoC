pub fn part_one(input: &str) -> Option<u32> {
    let mut current_value = 0;
    let mut largest = (0u32 ,0u32);
    let mut index = 0;
    for line in input.lines() {
        if line.is_empty() {
            if current_value > largest.0 {
                largest = (current_value, index)
            }
            index += 1;
            current_value = 0;
            continue;
        }

        let calories: u32 = line.parse().unwrap();
        current_value += calories;
    }

    Some(largest.0)
}

pub fn part_two(input: &str) -> Option<u32> {
    None
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
        assert_eq!(part_two(&input), None);
    }
}
