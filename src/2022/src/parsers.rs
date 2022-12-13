#![allow(dead_code)]
use nom::{sequence::separated_pair};

pub use nom::{
    branch::alt,
    bytes::complete::tag,
    character::complete::{alpha1, alphanumeric1, anychar, char, digit1, line_ending, one_of},
    combinator::{map, map_res, opt, verify},
    error::ErrorKind,
    multi::{fold_many1, many0, many1, separated_list0, separated_list1},
    sequence::{delimited, pair, preceded, terminated, tuple},
    Err, IResult,
};
pub use std::ops::RangeInclusive;

macro_rules! unsigned_nr_str_parser {
    ($t:ident) => {
        paste::item! {
            pub fn [< p_str_ $t >](s: &str) -> IResult<&str, $t> {
                map_res(digit1, |s: &str| {
                    s.parse::<$t>()
                        .map_err(|_err| Err::Error((s, ErrorKind::Digit)))
                })(s)
            }
        }
    };
}

macro_rules! nr_char_parser {
    ($t:ident) => {
        paste::item! {
            pub fn [< p_char_ $t >](s: &str) -> IResult<&str, $t> {
                map_res(one_of("0123456789"), |c: char| {
                    match c {
                        '0' => Ok(0),
                        '1' => Ok(1),
                        '2' => Ok(2),
                        '3' => Ok(3),
                        '4' => Ok(4),
                        '5' => Ok(5),
                        '6' => Ok(6),
                        '7' => Ok(7),
                        '8' => Ok(8),
                        '9' => Ok(9),
                        _ => Err(Err::Error((s, ErrorKind::Digit)))
                    }
                })(s)
            }
        }
    };
}

macro_rules! signed_nr_str_parser {
    ($t:ident) => {
        paste::item! {
            pub fn [< p_str_ $t >](s: &str) -> IResult<&str, $t> {
                map_res(
                    pair(opt(one_of("+-")), digit1),
                    |(sign, s): (Option<char>, &str)| {
                        s.parse::<$t>()
                            .map_err(|_err| Err::Error((s, ErrorKind::Digit)))
                            .map(|v| if let Some('-') = sign { -v } else { v })
                    },
                )(s)
            }
        }
    };
}

macro_rules! p_range_inc {
    ($t:ident) => {
        paste::item! {
            pub fn [< p_range_inc_ $t >](s: &str) -> IResult<&str, RangeInclusive<$t>> {
                map_res(
                    separated_pair([< p_str_ $t >], char('-'), [< p_str_ $t >]),
                    | (first, second) | {
                        Ok::<RangeInclusive<$t>, Err<$t>>(first..=second)
                    }
                )(s)
            }
        }
    };
}

macro_rules! add_for_utype {
    ($t:ident) => {
        unsigned_nr_str_parser!($t);
        p_range_inc!($t);
        nr_char_parser!($t);
    };
}

macro_rules! add_for_itype {
    ($t:ident) => {
        signed_nr_str_parser!($t);
        p_range_inc!($t);
        nr_char_parser!($t);
    };
}

add_for_utype!(usize);
add_for_utype!(u8);
add_for_utype!(u16);
add_for_utype!(u32);
add_for_utype!(u64);

add_for_itype!(isize);
add_for_itype!(i8);
add_for_itype!(i16);
add_for_itype!(i32);
add_for_itype!(i64);