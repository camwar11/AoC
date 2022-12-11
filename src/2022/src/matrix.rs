#![allow(dead_code)]
use nalgebra::{DMatrix, Scalar};

#[allow(unused_imports)]

pub fn matrix_from_vecs<T: Scalar>(vectors: Vec<Vec<T>>) -> DMatrix<T> {
    let rows = vectors.len();
    let cols = vectors.first().unwrap().len();

    DMatrix::from_fn(rows, cols, |x, y| vectors[x][y].clone())
}

pub fn add_row<T: Scalar>(matrix: DMatrix<T>, vector: Vec<T>) -> DMatrix<T> {
    let (mut rows, mut cols) = matrix.shape();

    if rows > 0 {
        rows -= 1;
    }

    if cols == 0 {
        cols = vector.len();
    }
    
    let mut new_matrix = matrix.insert_row(rows, vector.first().unwrap().clone());

    for col in 0..cols {
        new_matrix[(rows, col)] = vector[col].clone();
    }

    new_matrix
}

#[derive(PartialEq, Eq, PartialOrd, Ord, Clone, Copy)]
pub enum Direction {
    UP,
    DOWN,
    LEFT,
    RIGHT
}

pub fn items_in_direction<T : Scalar>(matrix: &DMatrix<T>, start: (usize, usize), direction: Direction) -> Vec<T>{
    if direction == Direction::UP {
        matrix.column_part(start.1, start.0).iter().rev().cloned().collect()
    }
    else if direction == Direction::DOWN {
        matrix.column(start.1).iter().skip(start.0 + 1).cloned().collect()
    }
    else if direction == Direction::LEFT {
        matrix.row_part(start.0, start.1).iter().rev().cloned().collect()
    }
    else {
        matrix.row(start.0).iter().skip(start.1 + 1).cloned().collect()
    }
}