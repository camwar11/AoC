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

fn make_move(knots: Vec<Point2<i64>>, the_move: ParsedLine, cache: &mut HashSet<(i64, i64)>) -> Vec<Point2<i64>> {
    const UP :Vector2<i64> = Vector2::new(0, 1);
    const DOWN :Vector2<i64> = Vector2::new(0, -1);
    const LEFT :Vector2<i64> = Vector2::new(-1, 0);
    const RIGHT :Vector2<i64> = Vector2::new(1, 0);

    let mut current_knots = knots;

    for _ in 0..the_move.1 {
        let translation = match the_move.0 {
            'U' => UP,
            'D' => DOWN,
            'L' => LEFT,
            'R' => RIGHT,
            _ => panic!("Bad direction")
        };

        let mut prev: Option<Point2<i64>> = None;
        let mut new_knots = Vec::new();

        for knot in &current_knots {
            let mut new_knot = knot.to_owned(); 

            if prev.is_none() {
                new_knot = new_knot + translation;
                prev = Some(new_knot);
                new_knots.push(new_knot);
                //println!("H {}, {}", new_knot.x, new_knot.y);
                continue;
            }

            let distance_x = ((prev.unwrap().x - knot.x)).abs();
            let distance_y = ((prev.unwrap().y - knot.y)).abs();

            if distance_x < 2 && distance_y < 2 {
                prev = Some(new_knot);
                new_knots.push(new_knot);
                continue;
            }
    
            if prev.unwrap().x < knot.x {
                new_knot = new_knot + LEFT;
            }
    
            if prev.unwrap().x > knot.x {
                new_knot = new_knot + RIGHT;
            }
    
            if prev.unwrap().y < knot.y {
                new_knot = new_knot + DOWN;
            }
    
            if prev.unwrap().y > knot.y {
                new_knot = new_knot + UP;
            }

            new_knots.push(new_knot);
            prev = Some(new_knot);
        }

        cache.insert((prev.unwrap().x, prev.unwrap().y));
        //println!("T {}, {}", prev.unwrap().x, prev.unwrap().y);

        current_knots = new_knots;
    }

    current_knots
}

pub fn part_one(input: &str) -> Option<usize> {
    let mut result = HashSet::new();
    let parsed = parse_lines(input);

    let mut state = vec![Point2::origin(), Point2::origin()];

    result.insert((0, 0));

    for my_move in parsed {
        state = make_move(state, my_move, &mut result);
    }

    Some(result.len())
}

pub fn part_two(input: &str) -> Option<usize> {
    let mut result = HashSet::new();
    let parsed = parse_lines(input);

    let mut state = vec![Point2::origin(), Point2::origin(), Point2::origin(), Point2::origin(), Point2::origin(), Point2::origin(), Point2::origin(), Point2::origin(), Point2::origin(), Point2::origin()];

    result.insert((0, 0));

    for my_move in parsed {
        state = make_move(state, my_move, &mut result);
    }

    Some(result.len())
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
        assert_eq!(part_two(&input), Some(36));
    }
}
