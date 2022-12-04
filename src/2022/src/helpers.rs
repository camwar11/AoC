/*
 * Use this file if you want to extract helpers from your solutions.
 * Example import from this file: `use advent_of_code::helpers::example_fn;`.
 */

use std::collections::HashSet;
use std::hash::Hash;

pub fn safe_create_file(path: &str) -> Result<std::fs::File, std::io::Error> {
    let folder_path = std::path::Path::new(&path);
    if let Some(parent) = folder_path.parent() 
    { 
        std::fs::create_dir_all(parent)? 
    }
    std::fs::OpenOptions::new().write(true).create_new(true).open(path)
}

pub fn create_file(path: &str) -> Result<std::fs::File, std::io::Error> {
    let folder_path = std::path::Path::new(&path);
    if let Some(parent) = folder_path.parent() 
    { 
        std::fs::create_dir_all(parent)? 
    }
    std::fs::OpenOptions::new().write(true).create(true).open(path)
}

pub fn intersection_full<T>(values: Vec<HashSet<T>> ) -> Option<HashSet<T>> where T: Eq + Hash + Clone {

    let mut iter = values.iter();
    let first = iter.next();
    if first.is_none() {
        return None;
    }
    
    let mut intersection = first.unwrap().clone();

    for other in iter {
        intersection = intersection.intersection(other).cloned().collect();
    }

    Some(intersection)
}