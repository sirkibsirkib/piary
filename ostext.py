import git

git_dir = "C:\Git\piary"
g = git.cmd.Git(git_dir)
x = g.diff()
print(x)