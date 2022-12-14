#![allow(dead_code, unused_variables)]

use std::collections::HashMap;
use nom::{bytes::complete::{take_while1}};

use super::parsers::*;


#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum InstructionInput {
    None,
    Int(i64),
    String(String)
}

struct InstructionInfo<T> {
    name: String,
    input_type: InstructionInput,
    instruction: fn(&mut SimpleCPU<T>, InstructionInput) -> InstructionOutput
}

struct InstructionOutput {
    new_inst_pointer: usize,
    result: Option<i64>
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct ProgramStatement {
    pub call: String,
    pub input: InstructionInput
}

pub struct SimpleCPU<T> {
    registers: HashMap<char, i64>,
    cycle: u32,
    instructions: HashMap<String, InstructionInfo<T>>,
    instruction_pointer: usize,
    program: Vec<ProgramStatement>,
    interrupt_handler: fn (InterruptInfo, &mut T)-> bool
}

macro_rules! add_instruction {
    ($map: ident, $name:literal, $input_type:expr, $instruction: expr) => {
        $map.insert($name.to_string(), InstructionInfo { name: $name.to_string(), input_type: $input_type, instruction: $instruction });
    };
}

pub struct InterruptInfo<'a> {
    pub registers: &'a HashMap<char, i64>,
    pub cycle: &'a u32,
    pub next_statement: &'a ProgramStatement
}

impl<T> SimpleCPU<T> {
    pub fn new<V>(program_str: &str, interrupt_handler: fn (InterruptInfo, &mut V)-> bool, starting_state: Option<HashMap<char, i64>>) -> SimpleCPU<V> {
        let instructions = SimpleCPU::get_instructions();
        let (_, program) = SimpleCPU::parse_program(&instructions, program_str).unwrap();
        SimpleCPU { 
            registers: starting_state.unwrap_or(HashMap::new()), 
            cycle: 1, 
            instruction_pointer: 0, 
            instructions, 
            program,
            interrupt_handler
        }
    }

    pub fn run(&mut self, state : &mut T ) {
        let prog_len = self.program.len();

        loop {
            let statement = &self.program[self.instruction_pointer].clone();
            let instruction = self.instructions.get(&statement.call).unwrap();

            let result = (instruction.instruction)(self, statement.input.clone());

            self.instruction_pointer = result.new_inst_pointer;

            self.cycle += 1;

            if !(self.interrupt_handler)(InterruptInfo { registers: &self.registers, cycle: &self.cycle, next_statement: statement }, state) {
                break;
            }

            if self.instruction_pointer >= prog_len {
                self.instruction_pointer = 0;
            }
        }
    }

    fn parse_program<'a>(instructions: &'a HashMap<String, InstructionInfo<T>>, program_str: &'a str) -> IResult<&'a str, Vec<ProgramStatement>> {
        let mut program = Vec::new();

        for line in program_str.lines() {
            let (_, parsed) = separated_list0(char(' '), take_while1(|c: char| c.is_ascii_alphanumeric() || c == '-'))(line)?;

            let mut first = true;
            let mut input_type = InstructionInput::None;
            let mut name = "";

            let mut input = InstructionInput::None;

            for term in parsed {
                if first {
                    input_type =  (*&instructions[term].input_type).clone();
                    name = term;

                    first = false;
                    continue;
                }

                match input_type {
                    InstructionInput::None => input = InstructionInput::None,
                    InstructionInput::Int(_) => input = InstructionInput::Int(p_str_i64(term)?.1),
                    InstructionInput::String(_) => input = InstructionInput::String(term.to_string())
                }
            }

            if name == "addx" {
                // Add a dummy noop to make it 2 cycles
                program.push(ProgramStatement { call: "noop".to_string(), input: InstructionInput::None });
            }

            program.push(ProgramStatement { call: name.to_string(), input });
        }

        Ok(("", program))
    }

    fn get_instructions() -> HashMap<String, InstructionInfo<T>> {
        let mut map = HashMap::new();
        static NONE: InstructionInput =  InstructionInput::None;
        static INT: InstructionInput =  InstructionInput::Int(0);
        let string: InstructionInput =  InstructionInput::String("".to_string());

        add_instruction!(map, "noop", NONE.clone(), SimpleCPU::noop);
        add_instruction!(map, "addx", INT.clone(), SimpleCPU::addx);

        map
    }

    fn noop(&mut self, input: InstructionInput) -> InstructionOutput {
        InstructionOutput { new_inst_pointer: self.instruction_pointer + 1, result: None }
    }

    fn addx(&mut self, input: InstructionInput) -> InstructionOutput {
        let mut current = self.registers.get(&'x').map_or(0, |val| val.clone());

        match input {
            InstructionInput::Int(int) => current += int,
            _ => panic!("Invalid input to addx")
        }

        self.registers.insert('x', current);

        InstructionOutput { new_inst_pointer: self.instruction_pointer + 1, result: None }
    }
}