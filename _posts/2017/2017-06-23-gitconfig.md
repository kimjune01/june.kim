---
layout: post
title: "./gitconfig"
tags: coding
---

```
[alias]
l = log --graph --abbrev-commit --decorate --date=relative --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all
lg2 = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)' --all

co = checkout
s = status
# list branches sorted by last modified
b = "!git for-each-ref --sort='-authordate' --format='%(authordate)%09%(objectname:short)%09%(refname)' refs/heads | sed -e 's-refs/heads/--'"
cam = commit -a -m
d = diff
a = add
praise = blame
pom = push origin master
po = push origin
poj = push origin junedev
pod = push origin dev
pud = pull origin dev
coj = checkout junedev
cod = checkout dev
hard = !git reset HEAD --hard && git clean -df
amend = "!f(){ git add . && git commit --amend ${1}; };f"
 
[user]
	email = kimjune01@gmail.com
	name = June
[apply]
	whitespace = nowarn
[credential]
	helper = osxkeychain

```
