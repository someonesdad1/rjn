'''
 
TODO
    - Remove /plib dependencies
 
Construct the rjn prototype github repository components
 
This script will enter each directory and construct the index.html file in
it from the index.txt file in the directory.  The index.txt file must have
the following form:
 
x1.pdf       # Name of PDF file
    File's description text is indented under the file name
x2.pdf       # Name of PDF file
    File's description text is indented under the file name
etc.
 
where the indentation defines the file name and description text.
Any line beginning with optional whitespace and '#' is ignored as a
comment.
'''
if 1:   # Header
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pprint import pprint as pp
        from textwrap import dedent
        from collections import deque
        from textwrap import dedent
    if 1:   # Custom imports
        #from get import GetLines
        from color import t
        from lwtest import Assert
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        t.dbg = t("skyl")

        class G:
            pass
        g = G()     # Container for global variables
        g.directories_to_process = (
            P("calculators"),
            P("components"),
            P("measurement"),
        )
        g.sep = r"^--+$"   # Regex separator for index.txt entries
        g.top_readme = P("README.md")
        g.index = "index.html"  # Directory's HTML file
        # Output variables.  The index_files variable will be a list
        # of links to the subdirectory's index file.
        g.index_files = []
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        s = dedent(f'''
        Usage:  {sys.argv[0]} [options] [cmd]
          Build the readme and html files.  cmd is:
            b   Build
            n   Dry run (show what will happen), notify about missing stuff
        Options
            -d  Debug output
        ''').strip()
        print(s)
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Debug output
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        if 1 and not args:
            Usage()
        return args
if 1:   # Classes
    class Doc:
        '''Contain a PDF document's information for HTML generation.  Print
        the instance to get a suitable HTML output form.
        '''
        def __init__(self, content, dir):
            '''content is a multiline string containing the PDF file name
            on the first line and the file's description on the remaining 
            lines.
            '''
            dq = deque(content.strip().split("\n"))
            Assert(len(dq) > 1)
            # Get PDF file's name
            self.dir = dir
            self.filename = dq.popleft().strip()
            # Make sure it exists
            self.file = P(self.filename).absolute()
            Assert(self.file.exists())
            # Remove empty or comment lines
            while dq:
                line = dq[0].strip()
                if not line or line[0] == "#":
                    dq.popleft()
                else:
                    break
            # Get file's description's lines
            Assert(dq)
            self.descr = deque()
            while dq:
                self.descr.append(dq.popleft())
            # Remove empty ending lines
            while self.descr:
                line = self.descr[-1].strip()
                if not line or line[0] == "#":
                    self.descr.pop()
                else:
                    break
            # Make sure we have at least one line
            Assert(self.descr)
            Assert(self.filename)
            Dbg(f"PDF file:  {self.filename}")
            Dbg(f"Description:")
            for i in self.descr:
                Dbg(f"{i}")
        def __str__(self):
            output = [""]
            url = g.rootdir/self.file
            output.append(f'<a href="{url}">{self.filename}</a>')
            output.append(f"<br>")
            for i in self.descr:
                if i.strip():
                    output.append(f"{i}")
                else:
                    output.append(f"<br>")
            output.append(f"<br>")
            return '\n'.join(output)

if 1:   # Core functionality
    def Dbg(line):
        if d["-d"]:
            t.print(f"{t.dbg}+ {line}")
    def HTML_header(title):
        return dedent(f'''
        <!DOCTYPE html>
        <html>
        <head><title>Directory {title}</title></head>
        <body>
        ''')
    def HTML_footer():
        return dedent(f'''
        </body>
        </html>
        ''')
    def ProcessDirectory(dir):
        # dir is a pathlib.Path
        cwd = os.getcwd()
        os.chdir(dir)
        Dbg(f"Processing '{dir}' directory")
        # Get index.txt file's content as a string
        s = open("index.txt", "rb").read().decode("UTF8")
        # Open the output file
        o = open("index.html", "w")
        o.write(HTML_header("Directory: {dir}"))
        # Separate into each PDF file's chunks
        items = re.split(g.sep, s, flags=re.M)
        for item in items:
            item = item.strip()
            if item:
                Dbg(item)
                doc = Doc(item, dir)
                o.write(str(doc))
                o.write("\n")
        o.write(HTML_footer())
        o.close()
        os.chdir(cwd)
    def MakeRootHTMLFile():
        os.chdir(basedir)
        o = open("index.html", "w")
        o.write(HTML_header("RJN's PDF documents"))
        o.write(dedent(f'''
        Click on the links to see each directory's index file<br><br>
        '''))
        for dir in g.directories_to_process:
            o.write(f'<a href="{dir}/index.html">{dir}</a><br>\n')
        o.write(HTML_footer())
        o.close()

if __name__ == "__main__":
    d = {}      # Options dictionary
    basedir = os.getcwd()
    args = ParseCommandLine(d)
    g.rootdir = P(os.getcwd())
    Dbg("Lines beginning with '+' are debug lines enabled by -d option")
    Dbg(f"rootdir = {g.rootdir}")
    for dir in g.directories_to_process:
        ProcessDirectory(dir)
    MakeRootHTMLFile()
