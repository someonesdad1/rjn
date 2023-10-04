
'''
Construct the rjn prototype github repository components

This script will enter each directory and construct the index.html file in
it from the index.txt file in the directory.  The index.txt file must have
the following form:

x1.pdf       # Name of PDF file
    description description description description description
    description description description description description
    description description description description description
    description description description description description

    description description description description description
    description description description description description
    description description description description description
x2.pdf       # Name of PDF file
    description description description description description
    description description description description description
    description description description description description
etc.

where the indentation defines the file name and description text.
Python-style comments can be used if desired.

While make could be a more efficient tool, a python script will be fast
enough even with hundreds of PDF files, as it's elementary text processing
and the task doesn't need to be done frequently.

'''
if 1:   # Header
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import dedent
        from get import GetLines
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        class G:
            pass
        g = G()     # Container for global variables
        g.directories_to_process = (
            P("calculators"),
            P("components"),
            P("measurement"),
        )
        g.top_readme = P("README.md")
        # Output variables.  The index_files variable will be a list
        # of links to the subdirectory's index file.
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [cmd]
          Build the readme and html files.  cmd is:
              b   Build
              n   Dry run (show what will happen), notify about missing stuff
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Debug output
        d["-d"] = True  # xx
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
        if 0 and not args:
            Usage()
        return args
if 1:   # Core functionality
    def GetText(file):
        "file should be an index.txt file's contents"
        lines = GetLines(file)
        pp(lines) #xx
        exit() #xx
    def ProcessDirectory(dir):
        file = dir/"index.txt"
        output = dir/"index.html"
        if d["-d"]:
            print(f"Processing {dir}")
            print(f"  rootdir = {g.rootdir}")
            print(f"  dir = {dir}")
            print(f"  file = {file}")
            print(f"  output = {output}")
        lines = GetText(file)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    g.rootdir = P(os.getcwd())
    for dir in g.directories_to_process:
        # dir is a pathlib.Path
        ProcessDirectory(dir)
