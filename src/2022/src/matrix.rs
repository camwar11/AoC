#![allow(dead_code)]
use nalgebra::{DMatrix, Scalar};

#[allow(unused_imports)]

pub fn matrix_from_vecs<T: Scalar>(vectors: Vec<Vec<T>>) -> DMatrix<T> {
    let rows = vectors.len();
    let cols = vectors.first().unwrap().len();

    DMatrix::from_fn(rows, cols, |x, y| vectors[x][y].clone())
}

pub fn add_row<T: Scalar>(matrix: DMatrix<T>, vector: Vec<T>) -> DMatrix<T> {
    let length = matrix.len();
    let mut new_row_idx = 0;
    let cols = vector.len();

    if length > 0 {
        new_row_idx = length / cols;
    }
    let mut new_matrix = matrix.insert_row(new_row_idx, vector.first().unwrap().clone());

    for col in 0..cols {
        new_matrix[(new_row_idx, col)] = vector[col].clone();
    }

    new_matrix
}