use advent_of_code::parsers::*;
use petgraph::{prelude::*};

use nom::{
    self,  error::Error
};

type ParsedLine<'a> = TreeInfo;

const CD: &str = "cd";
const LS: &str = "ls";

struct TreeInfo {
    graph: DiGraph<FileItem, u32>,
    root: NodeIndex,
    current: NodeIndex
}

#[derive(Debug)]
struct FileItem {
    name: String,
    size: u32,
    is_file: bool
}

fn run_command<'a>(command: &str, arg: &str, mut tree: ParsedLine<'a>) -> ParsedLine<'a>{

    if command != CD { 
        return tree;
    }

    if arg == "/" {
        tree = TreeInfo {
            current: tree.root,
            ..tree
        };
        return tree;
    }

    if arg == ".." {
        let parent_edge = tree.graph.edges_directed(tree.current, Direction::Incoming).next().unwrap();
        let parent_idx = parent_edge.source();
        tree = TreeInfo {
            current: parent_idx,
            ..tree
        };
        return tree;
    }

    let new_dir = FileItem {
        name: arg.to_string(),
        size: 0,
        is_file: false
    };

    let new_idx = tree.graph.add_node(new_dir);

    tree.graph.add_edge(tree.current, new_idx, 1);
    
    TreeInfo 
    { 
        current: new_idx,
        ..tree
    }
}

fn parse_line<'a>(line: &'a str, mut tree: ParsedLine<'a>) -> ParsedLine<'a>{

    let result = match delimited(
        tag::<&str, &str, Error<&str>>("$ "), 
        alt((tag(CD), tag(LS))), 
        opt(tag(" ")))
        (line) {
        Ok((arg, command)) => {
            tree = run_command(command, arg, tree);
            true
        },
        Err(_) => false
    };

    if result {
        return tree;
    }

    let is_dir = match tag::<&str, &str, Error<&str>>("dir ")(line) {
        Ok((_, _)) => {
            true
        },
        _ => false
    };

    if is_dir {
        return tree;
    }

    let (name, size) = p_str_u32(line).unwrap_or(("", 0));

    let file = FileItem { 
        name: name.to_string(),
        size,
        is_file: true
    };

    let new_idx = tree.graph.add_node(file);
    tree.graph.add_edge(tree.current, new_idx, 1);

    tree
}

fn parse_lines(input: &str) -> ParsedLine {
    let root = FileItem {
        name: "/".to_string(),
        size: 0,
        is_file: false
    } ;

    let mut graph: DiGraph<FileItem, u32> = DiGraph::new();

    let idx = graph.add_node(root);
    let mut parsed = TreeInfo {
        graph,
        root: idx,
        current: idx
    };

    for line in input.lines() {
        parsed = parse_line(line, parsed);
    }
    
    parsed
}

fn populate_dir_size(mut tree: ParsedLine, idx: NodeIndex) -> (ParsedLine, u32){
    let mut sum = 0;

    let mut n2 : Vec<NodeIndex> = Vec::new();
    {
        let neighbors = tree.graph.neighbors(idx).clone();
        for neighbor in neighbors {
            n2.push(neighbor);
        }
    }

    
    for neighbor in n2 {
        let node = tree.graph.node_weight(neighbor).unwrap();
        let new_tree: TreeInfo;
        let mut size = node.size;
        
        if !node.is_file {
            let (new_tree2, new_size2) = populate_dir_size(tree, neighbor);
            new_tree = new_tree2;
            size = new_size2;
        }
        else {
            new_tree = tree;
        }

        tree = new_tree;
        let new_node = tree.graph.node_weight_mut(neighbor).unwrap();
        new_node.size = size;
        sum += size;
    }

    let current_node = tree.graph.node_weight_mut(idx).unwrap();
    current_node.size = sum;


    (tree, sum)
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut parsed = parse_lines(input);

    let root = parsed.root;

    (parsed, _) = populate_dir_size(parsed, root);

    let mut result = 0;

    for dir in parsed.graph.node_weights().filter(|d| !d.is_file && d.size <= 100000) {
        result += dir.size
    }

    Some(result)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut parsed = parse_lines(input);

    let root = parsed.root;

    (parsed, _) = populate_dir_size(parsed, root);

    let result;
    const TOTAL: u32 = 70000000;
    const NEEDED: u32 = 30000000;

    let root_size = parsed.graph.node_weight(root).unwrap().size;
    let remaining_size = TOTAL - root_size;

    let need_to_delete = NEEDED - remaining_size;


    result = parsed.graph.node_weights().filter(|d| !d.is_file && d.size > need_to_delete).map(|i| i.size).min().unwrap();

    Some(result)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 7);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 7);
        assert_eq!(part_one(&input), Some(95437));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 7);
        assert_eq!(part_two(&input), Some(24933642));
    }
}
