require 'yaml'

Dir.glob('_posts/*.md') do |file|
  content = File.read(file)
  
  # Split the file into front matter and body
  if content =~ /\A(---\s*\n.*?\n?)^(---\s*$\n?)/m
    front_matter = YAML.load($1)
    body = $'
  else
    front_matter = {}
    body = content
  end
  
  # If there's no image in the front matter, find the first image in the body
  if !front_matter.key?('image')
    match = body.match(/!\[.*?\]\((.*?)\)/)
    if match
      front_matter['image'] = match[1]
      
      # Update the file
      File.write(file, YAML.dump(front_matter) + "---\n" + body)
      puts "Updated #{file} with image: #{front_matter['image']}"
    else
      puts "No image found in #{file}"
    end
  else
    puts "Image already exists in front matter for #{file}"
  end
end

