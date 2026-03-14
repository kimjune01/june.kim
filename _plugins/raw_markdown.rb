Jekyll::Hooks.register :site, :post_write do |site|
  site.posts.docs.each do |post|
    content = File.read(post.path, encoding: 'utf-8')
    # Strip YAML front matter, keep raw markdown body
    markdown = content.sub(/\A---\s*\n.*?\n?---\s*\n/m, '')

    dest = File.join(site.dest, "#{post.url}.md")
    FileUtils.mkdir_p(File.dirname(dest))
    File.write(dest, markdown, encoding: 'utf-8')
  end
end
