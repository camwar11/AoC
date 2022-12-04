use std::{collections::HashMap, hash::Hash, borrow::Borrow};

#[derive(Eq, Hash, PartialEq, Clone, Copy)]
enum Throw {
    R,
    P,
    S
}

fn outcome_score(enemy_throw:Throw, your_throw:Throw) -> u32 {
    if enemy_throw == Throw::R {
        if your_throw == Throw::P {
            return 6;
        }
        else if your_throw == Throw::S {
            return 0;
        }
    }
    else if enemy_throw == Throw::P {
        if your_throw == Throw::S {
            return 6;
        }
        else if your_throw == Throw::R {
            return 0;
        }
    }
    else {
        if your_throw == Throw::R {
            return 6;
        }
        else if your_throw == Throw::P {
            return 0;
        }
    }
    3
}

fn calculate_score(enemy_throw:Throw, your_throw:Throw) -> u32 {
    
    let shape_score = match your_throw {
        Throw::R => 1,
        Throw::P => 2,
        Throw::S => 3,
    };

    shape_score + outcome_score(enemy_throw, your_throw)
}

fn enemy_throw_map() -> HashMap<char, Throw> {
    let mut map = HashMap::new();

    map.insert('A', Throw::R);
    map.insert('B', Throw::P);
    map.insert('C', Throw::S);

    map
}

fn my_throw_map() -> HashMap<char, Throw> {
    let mut map = HashMap::new();

    map.insert('X', Throw::R);
    map.insert('Y', Throw::P);
    map.insert('Z', Throw::S);

    map
}

fn play_game(strategy: Vec<(char, char)>, enemy_map: HashMap<char, Throw>, my_map: HashMap<char, Throw>) -> u32 {
    let mut score = 0;
    for round in strategy {
        let enemy_throw = enemy_map.get(round.0.borrow());
        let my_throw = my_map.get(round.1.borrow());

        score += calculate_score(*enemy_throw.unwrap(), *my_throw.unwrap());
    }

    score
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut strategy = Vec::new();
    for line in input.lines() {
        let split = line.split_whitespace().collect::<Vec<_>>();
        strategy.push((split[0].chars().nth(0).unwrap(), split[1].chars().nth(0).unwrap()));
    }

    let enemy_throws = enemy_throw_map();
    let my_throws  = my_throw_map();

    Some(play_game(strategy, enemy_throws, my_throws))
}

pub fn part_two(input: &str) -> Option<u32> {
    None
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 2);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 2);
        assert_eq!(part_one(&input), Some(15));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 2);
        assert_eq!(part_two(&input), Some(0));
    }
}
