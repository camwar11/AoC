use std::{collections::HashMap, hash::Hash, borrow::Borrow};

use advent_of_code::parsers::*;

use nom::{
    self, 
     sequence::separated_pair, character::complete::{char}
};

type ParsedLine<'a> = (char, char);

fn parse_line(line: &str) -> Result<ParsedLine, nom::Err<nom::error::Error<&str>>>{
    let (_, pair) = separated_pair(anychar, char(' '), anychar)(line)?;
    Ok(pair)
}

fn parse_lines(input: &str) -> Vec<ParsedLine> {
    let mut parsed = Vec::new();
    for line in input.lines() {
        parsed.push(parse_line(line).unwrap());
    }

    parsed
}

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

fn get_my_throw(enemy_throw: Throw, my_strat: char, part1: bool) -> Throw {
    if part1 {
        match my_strat {
            'X' => Throw::R,
            'Y' => Throw::P,
            _ => Throw::S,
        }
    }
    else {
        match my_strat {
            'X' => match enemy_throw {
                Throw::R => Throw::S,
                Throw::P => Throw::R,
                Throw::S => Throw::P,
            },
            'Z' => match enemy_throw {
                Throw::R => Throw::P,
                Throw::P => Throw::S,
                Throw::S => Throw::R,
            },
            _ => enemy_throw,
        }
    }
}

fn enemy_throw_map() -> HashMap<char, Throw> {
    let mut map = HashMap::new();

    map.insert('A', Throw::R);
    map.insert('B', Throw::P);
    map.insert('C', Throw::S);

    map
}

fn play_game(strategy: Vec<(char, char)>, enemy_map: HashMap<char, Throw>, is_part1: bool) -> u32 {
    let mut score = 0;
    for round in strategy {
        let enemy_throw = *enemy_map.get(round.0.borrow()).unwrap();
        let my_throw = get_my_throw(enemy_throw, round.1, is_part1);

        score += calculate_score(enemy_throw, my_throw);
    }

    score
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut strategy = Vec::new();
    for line in parse_lines(input){
        strategy.push(line);
    }

    let enemy_throws = enemy_throw_map();

    Some(play_game(strategy, enemy_throws, true))
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut strategy = Vec::new();
    for line in parse_lines(input){
        strategy.push(line);
    }

    let enemy_throws = enemy_throw_map();

    Some(play_game(strategy, enemy_throws, false))
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
        assert_eq!(part_two(&input), Some(12));
    }
}
