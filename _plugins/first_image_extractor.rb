module Jekyll
  class FirstImageExtractor < Generator
    safe true
    priority :low

    def generate(site)
      site.posts.docs.each do |post|
        if post.data['image'].nil?
          content = post.content
          match = content.match(/<img.*?src=["'](.*?)["']/)
          if match
            post.data['image'] = match[1]
          end
        end
      end
    end
  end
end