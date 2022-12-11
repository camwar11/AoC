use std::{ops::AddAssign, collections::HashSet};

use advent_of_code::parsers::*;

use nalgebra::{Point2, Vector2};
use nom::{
    self, 
     sequence::separated_pair, character::complete::{char}
};

type ParsedLine<'a> = (char, u32);

fn parse_line(line: &str) -> Result<ParsedLine, nom::Err<nom::error::Error<&str>>>{
    let (_, pair) = separated_pair(one_of("RULD"), char(' '), p_str_u32)(line)?;
    Ok(pair)
}

fn parse_lines(input: &str) -> Vec<ParsedLine> {
    let mut parsed = Vec::new();
    for line in input.lines() {
        parsed.push(parse_line(line).unwrap());
    }

    parsed
}

#[derive(PartialEq, Eq, PartialOrd, Clone, Copy)]
struct State {
    head: Point2<i64>,
    tail: Point2<i64>
}

fn make_move(mut state: State, the_move: ParsedLine, cache: &mut HashSet<(i64, i64)>) -> State {
    const UP :Vector2<i64> = Vector2::new(0, 1);
    const DOWN :Vector2<i64> = Vector2::new(0, -1);
    const LEFT :Vector2<i64> = Vector2::new(-1, 0);
    const RIGHT :Vector2<i64> = Vector2::new(1, 0);

    for _ in 0..the_move.1 {
        state.head = match the_move.0 {
            'U' => state.head + UP,
            'D' => state.head + DOWN,
            'L' => state.head + LEFT,
            'R' => state.head + RIGHT,
            _ => panic!("Bad direction")
        };

        let distance_x = ((state.head.x - state.tail.x)).abs();
        let distance_y = ((state.head.y - state.tail.y)).abs();

        if distance_x < 2 && distance_y < 2 {
            continue;
        }

        if state.head.x < state.tail.x {
            state.tail = state.tail + LEFT;
        }

        if state.head.x > state.tail.x {
            state.tail = state.tail + RIGHT;
        }

        if state.head.y < state.tail.y {
            state.tail = state.tail + DOWN;
        }

        if state.head.y > state.tail.y {
            state.tail = state.tail + UP;
        }

        cache.insert((state.tail.x, state.tail.y));
    }

    state
}

pub fn part_one(input: &str) -> Option<usize> {
    let mut result = HashSet::new();
    let parsed = parse_lines(input);

    let mut state = State {
        head: Point2::origin(),
        tail: Point2::origin(),
    };

    result.insert((state.tail.x, state.tail.y));

    for my_move in parsed {
        state = make_move(state, my_move, &mut result);
    }

    Some(result.len())
}

pub fn part_two(input: &str) -> Option<usize> {
    let mut result = 0;
    let mut parsed = parse_lines(input);

    //Some(result)
    None
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 9);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 9);
        assert_eq!(part_one(&input), Some(13));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 9);
        assert_eq!(part_two(&input), Some(0));
    }
}
