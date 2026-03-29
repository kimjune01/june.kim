# Jek: Jekyll Dev Server

Start `bundle exec jekyll serve --livereload` on port 4000.

## Process

1. Check if port 4000 is already in use (`lsof -ti:4000`).
   - If occupied, report the PID and ask the user before killing it.
2. Run `bundle exec jekyll serve --livereload` in the background.
3. Report that the server is running at http://localhost:4000.
