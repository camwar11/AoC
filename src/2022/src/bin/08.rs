use std::{collections::HashSet, cmp::max};

use advent_of_code::{parsers::*, matrix::{matrix_from_vecs, items_in_direction, Direction}};

use nalgebra::DMatrix;
use nom::{
    self, 
     sequence::separated_pair, character::complete::{char}
};

fn parse_line(line: &str) -> Result<Vec<u16>, nom::Err<nom::error::Error<&str>>>{
    let (_, pair) = many1(p_char_u16)(line)?;
    Ok(pair)
}

fn parse_lines(input: &str) -> DMatrix<u16> {
    let mut parsed: Vec<Vec<u16>> = Vec::new();
    for line in input.lines() {
        match parse_line(line) {
            Ok(tree) => parsed.push(tree),
            Err(_) => ()
        };
    }

    let matrix = matrix_from_vecs(parsed);
    matrix
}

fn count_visible_trees(forest: &DMatrix<u16>) -> usize{
    let mut visible: HashSet<(usize, usize)> = HashSet::new();

    let mut i_row = 0;
    let mut j_col;
    for row in forest.row_iter() {
        let mut max_height: Option<u16> = None;
        
        j_col = 0;
        for col in row.iter() {
            let (is_visible, max) = match max_height {
                Some(h) => (*col > h, max(*col, h)),
                None => (true, *col)
            };

            max_height = Some(max);

            if is_visible{
                visible.insert((i_row, j_col));
            }

            j_col += 1;
        }

        max_height = None;
        j_col = row.len() - 1;
        for col in row.iter().rev() {
            let (is_visible, max) = match max_height {
                Some(h) => (*col > h, max(*col, h)),
                None => (true, *col)
            };

            max_height = Some(max);

            if is_visible{
                visible.insert((i_row, j_col));
            }

            if j_col > 0 {
                j_col -= 1;
            }
        }

        i_row += 1;
    }

    j_col = 0;
    for col in forest.column_iter() {
        let mut max_height: Option<u16> = None;
        
        i_row = 0;
        for row in col.iter() {
            let (is_visible, max) = match max_height {
                Some(h) => (*row > h, max(*row, h)),
                None => (true, *row)
            };

            max_height = Some(max);

            if is_visible{
                visible.insert((i_row, j_col));
            }

            i_row += 1;
        }

        max_height = None;
        i_row = col.len() - 1;
        for row in col.iter().rev() {
            let (is_visible, max) = match max_height {
                Some(h) => (*row > h, max(*row, h)),
                None => (true, *row)
            };

            max_height = Some(max);

            if is_visible{
                visible.insert((i_row, j_col));
            }

            if i_row > 0 {
                i_row -= 1;
            }
        }

        j_col += 1;
    }

    visible.len()
}

fn scenic_score(forest: &DMatrix<u16>, idx: (usize, usize)) -> usize {
    let tree_height = forest[idx];

    let mut prev_blocked = false;
    let binding = items_in_direction(forest, idx, Direction::UP);
    let up:Vec<&u16> = binding.iter().take_while(|tree| 
    {
        if prev_blocked {
            return false;
        }

        if **tree >= tree_height {
            prev_blocked = true;
        }

        true
    }).collect();

    let up_size = up.len();

    if up_size == 0 {
        return 0;
    }

    prev_blocked = false;
    let binding2 = items_in_direction(forest, idx, Direction::DOWN);
    let down:Vec<&u16> = binding2.iter().take_while(|tree| 
    {
        if prev_blocked {
            return false;
        }

        if **tree >= tree_height {
            prev_blocked = true;
        }
        true
    }).collect();

    let down_size = down.len();
    if down_size == 0 {
        return 0;
    }

    prev_blocked = false;
    let binding3 = items_in_direction(forest, idx, Direction::LEFT);
    let left:Vec<&u16> = binding3.iter().take_while(|tree| 
    {
        if prev_blocked {
            return false;
        }
        if **tree >= tree_height {
            prev_blocked = true;
        }
        true
    }).collect();

    let left_size = left.len();
    if left_size == 0 {
        return 0;
    }

    prev_blocked = false;
    let binding4 = items_in_direction(forest, idx, Direction::RIGHT);
    let right:Vec<&u16> = binding4.iter().take_while(|tree| 
    {
        if prev_blocked {
            return false;
        }

        if **tree >= tree_height {
            prev_blocked = true;
        }
        true
    }).collect();
    let right_size = right.len();

    if right_size == 0 {
        return 0;
    }

    return up_size * down_size * left_size * right_size;
}

fn max_scenic_score(forest: &DMatrix<u16>) -> usize {
    let mut max_score = 0;

    let shape = forest.shape();

    for row in 0..shape.0 {
        for col in 0..shape.1 {
            max_score = max(max_score, scenic_score(forest, (row, col)));
        }
    }

    return max_score;
}

pub fn part_one(input: &str) -> Option<usize> {
    let matrix = parse_lines(input);

    Some(count_visible_trees(&matrix))
}

pub fn part_two(input: &str) -> Option<usize> {
    let matrix = parse_lines(input);

    Some(max_scenic_score(&matrix))
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 8);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 8);
        assert_eq!(part_one(&input), Some(21));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 8);
        assert_eq!(part_two(&input), Some(8));
    }
}
