use std::collections::HashMap;

use advent_of_code::simple_cpu::*;

fn check_sig_strength(info: InterruptInfo, total: &mut i64) -> bool{
    let next_cycles = match info.next_statement.call.as_str() {
        "noop" => 2,
        "addx" => 3,
        _ => 0
    };

    for i in 1..next_cycles {
        let cycle = (*info.cycle as i64) + i - 20;
        if cycle < 0 || cycle % 40 != 0{
            continue;
        }  

        let cycle = (*info.cycle as i64) + i;

        let add = match info.next_statement.input {
            InstructionInput::Int(int) => match i {
                2 => int,
                _ => 0
            },
            _ => 0
        };

        let value = cycle * (info.registers[&'x'] + add);

        println!("Cycle {}: {}", cycle, value);

        *total = *total + value;
    }

    *info.cycle < 220
}

pub fn part_one(input: &str) -> Option<i64> {
    let mut state = HashMap::new();

    state.insert('x', 1);

    let mut total = 0;

    let mut cpu = SimpleCPU::<i64>::new(input, check_sig_strength, Some(state));

    cpu.run(&mut total);

    Some(total)
}

pub fn part_two(input: &str) -> Option<u32> {



    //Some(result)
    None
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 10);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 10);
        assert_eq!(part_one(&input), Some(13140));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 10);
        assert_eq!(part_two(&input), Some(0));
    }
}
