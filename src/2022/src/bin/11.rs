use std::{sync::Arc, collections::VecDeque};

use advent_of_code::parsers::*;

use nom::{
    self, 
     sequence::separated_pair, character::complete::{char, multispace1}
};

#[derive(Clone)]
struct Monkey {
    idx: usize,
    items: VecDeque<i64>,
    operation: Arc<dyn Fn(i64) -> i64>,
    throw: Arc<dyn Fn(i64) -> usize>,
}

pub fn parse_idx(s: &str) -> IResult<&str, usize> {
    delimited(tag("Monkey "), p_str_usize, pair(tag(":"), multispace1))(s)
}

pub fn parse_starting_items(s: &str) -> IResult<&str, Vec<i64>> {
    delimited(tag("Starting items:"), many1(preceded(alt((tag(", "), tag(" "))), p_str_i64)), multispace1)(s)
}

pub fn parse_operation(s: &str) -> IResult<&str, Arc<dyn Fn(i64) -> i64>> {
    let (rest, (operator, value)) = delimited(tag("Operation: new = old "), separated_pair(one_of("+-/*"), char(' '), alt((tag("old"), digit1))), multispace1)(s)?;

    let parsed_int = p_str_i64(value);

    let op: Arc<dyn Fn(i64) -> i64> =
        match parsed_int {
            Ok((_, int_value)) => match operator {
                '+' => Arc::new(move |old| old + int_value),
                '-' => Arc::new(move |old| old - int_value),
                '/' => Arc::new(move |old| old / int_value),
                '*' => Arc::new(move |old| old * int_value),
                _ => panic!("Invalid operation")
            },
            Err(_) => match operator {
                '+' => Arc::new(move |old| old + old),
                '-' => Arc::new(move |old| old - old),
                '/' => Arc::new(move |old| old / old),
                '*' => Arc::new(move |old| old * old),
                _ => panic!("Invalid operation")
            }
        };

    Ok((rest, op))
}

pub fn parse_throw(s: &str) -> IResult<&str, (Arc<dyn Fn(i64) -> usize>, i64)> {
    let (rest, divisable_by) = delimited(tag("Test: divisible by "), p_str_i64, multispace1)(s)?;
    let (rest, true_monkey) = delimited(tag("If true: throw to monkey "), p_str_usize, multispace1)(rest)?;
    let (rest, false_monkey) = delimited(tag("If false: throw to monkey "), p_str_usize, multispace1)(rest)?;


    let throw: Arc<dyn Fn(i64) -> usize> = Arc::new(move |value| match value % divisable_by {
        0 => true_monkey,
        _ => false_monkey
    } );

    Ok((rest, (throw, divisable_by)))
}

fn parse_monkey(s: &str) -> IResult<&str, (Monkey, i64)> {
    let (rest, idx) = parse_idx(s)?;
    let (rest, items) = parse_starting_items(rest)?;
    let (rest, operation) = parse_operation(rest)?;
    let (rest, (throw, div_by)) = parse_throw(rest)?;

    Ok((rest, 
        (Monkey {
            idx,
            items: VecDeque::from_iter(items),
            operation,
            throw
        }, div_by)))
}

fn parse_lines(input: &str) -> (Vec<Monkey>, i64) {
    let (_, monkeys) = many1(parse_monkey)(input).unwrap();

    let div_by = monkeys.iter().fold(1, |acc, x| acc * x.1);
    (monkeys.iter().map(|x| x.0.clone()).collect(), div_by)
}

fn reduce_worry(level: i64) -> i64 {
    level / 3
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut monkeys = parse_lines(input);
    let mut results = vec![0; monkeys.0.len()];

    for _ in 0..20 {
        let num_monkeys = monkeys.0.len();
        for i in 0..num_monkeys {
            let monkey = monkeys.0.get_mut(i).unwrap();

            let mut item = monkey.items.pop_front();

            let mut throws = Vec::new();
            while item.is_some() {
                results[i] += 1;
                let worry_level = reduce_worry((monkey.operation)(item.unwrap()));

                let throw_target = (monkey.throw)(worry_level);

                throws.push((throw_target, worry_level));

                item = monkey.items.pop_front();
            }

            for throw in throws {
                let monkey = monkeys.0.get_mut(throw.0).unwrap();
                monkey.items.push_back(throw.1);
            }
        }
    }

    results.sort_unstable_by(|a, b| b.cmp(a));

    Some(results[0] * results[1])
}

pub fn part_two(input: &str) -> Option<u64> {
    let mut monkeys = parse_lines(input);
    let mut results = vec![0u64; monkeys.0.len()];

    for _ in 0..10000 {
        let num_monkeys = monkeys.0.len();
        for i in 0..num_monkeys {
            let monkey = monkeys.0.get_mut(i).unwrap();

            let mut item = monkey.items.pop_front();

            let mut throws = Vec::new();
            while item.is_some() {
                results[i] += 1;
                let worry_level = (monkey.operation)(item.unwrap()) % monkeys.1;

                let throw_target = (monkey.throw)(worry_level);

                throws.push((throw_target, worry_level));

                item = monkey.items.pop_front();
            }

            for throw in throws {
                let monkey = monkeys.0.get_mut(throw.0).unwrap();
                monkey.items.push_back(throw.1);
            }
        }
    }

    results.sort_unstable_by(|a, b| b.cmp(a));

    Some(results[0] * results[1])
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 11);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 11);
        assert_eq!(part_one(&input), Some(10605));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 11);
        assert_eq!(part_two(&input), Some(2713310158));
    }
}
