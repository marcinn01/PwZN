import argparse
import collections
from collections import Counter
from ascii_graph import Pyasciigraph
from rich.progress import Progress
import rich

rich.get_console().clear()

collections.Iterable = collections.abc.Iterable

parser = argparse.ArgumentParser(description='Generate histogram of word frequency from a text file')
parser.add_argument('file_path', help='Path to the text file')
parser.add_argument('--top', '-t', type=int, default=10, help='Number of top words to display in the histogram')
parser.add_argument('--min_length', '-m', type=int, default=0, help='Minimum length of words to include in the histogram')
args = parser.parse_args()

try:
    with open(args.file_path, 'r', encoding='utf-8') as file:
        text = file.read()
except FileNotFoundError:
    print(f"Error: File not found at {args.file_path}")
    exit()

word_counts = Counter()
total_words = len(text.split())

with Progress() as progress:
    task = progress.add_task("Processing file...", total=total_words)
    for word in text.split():
        progress.update(task, advance=1)
        if (len(word) >= args.min_length):
            word_counts[word] += 1

top_word_counts = word_counts.most_common(args.top)

graph = Pyasciigraph()
for line in graph.graph(f'Word Frequency (Min Length: {args.min_length})', top_word_counts):
    print(line)


