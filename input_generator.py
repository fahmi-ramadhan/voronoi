import random
import argparse

def generate_random_points(num_points, min_x=0, max_x=1400, min_y=0, max_y=720, filename="input.txt"):
    """
    Generate random points for a Voronoi diagram and save them to a file.
    
    Args:
        num_points (int): Number of points to generate
        min_x (int): Minimum x coordinate (default: 0)
        max_x (int): Maximum x coordinate (default: 500)
        min_y (int): Minimum y coordinate (default: 0)
        max_y (int): Maximum y coordinate (default: 500)
        filename (str): Output filename (default: "input.txt")
    """
    # Generate unique random points
    points = set()
    while len(points) < num_points:
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        points.add((x, y))
    
    # Sort points for consistent output
    sorted_points = sorted(points)
    
    # Write points to file
    with open(filename, 'w') as f:
        for x, y in sorted_points:
            f.write(f"{x} {y}\n")
    
    print(f"Generated {num_points} points and saved to {filename}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate random points for Voronoi diagram')
    parser.add_argument('num_points', type=int, help='Number of points to generate')
    parser.add_argument('--min-x', type=int, default=50, help='Minimum x coordinate (default: 50)')
    parser.add_argument('--max-x', type=int, default=1400, help='Maximum x coordinate (default: 1400)')
    parser.add_argument('--min-y', type=int, default=50, help='Minimum y coordinate (default: 50)')
    parser.add_argument('--max-y', type=int, default=700, help='Maximum y coordinate (default: 700)')
    parser.add_argument('--output', type=str, default='input.txt', help='Output filename (default: input.txt)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Generate points with provided arguments
    generate_random_points(
        num_points=args.num_points,
        min_x=args.min_x,
        max_x=args.max_x,
        min_y=args.min_y,
        max_y=args.max_y,
        filename=args.output
    )
