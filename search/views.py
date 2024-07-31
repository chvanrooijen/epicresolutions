import os
import re
from django.shortcuts import render
from django.db.models import Q, CharField, TextField
from posts.models import Post

def search(request):
    query = request.GET.get('q')
    results = []

    # Search in Post model
    fields = [field.name for field in Post._meta.fields if isinstance(field, (CharField, TextField))]
    q_objects = Q()
    for field in fields:
        q_objects |= Q(**{f"{field}__icontains": query})
    post_results = Post.objects.filter(q_objects)
    for post in post_results:
        # Assuming each post has a 'get_absolute_url' method to generate its URL
        post_url = post.get_absolute_url()
        results.append(f'<a href="{post_url}">{post.title}</a>')

    # Search in static content (templates)
    template_results = search_templates(query)
    results.extend(template_results)

    return render(request, 'search/search-results.html', {'query': query, 'results': results})

def search_templates(query):
    # Adjust the path to the pages app's templates directory
    template_dir = os.path.join(os.path.dirname(__file__), '../pages/templates')
    results = []

    # Compile a regex pattern for partial word match
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    # Compile a regex pattern to remove HTML tags
    tag_re = re.compile(r'<[^>]+>')

    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Remove HTML tags from the content
                    text_content = tag_re.sub('', content)
                    if pattern.search(text_content):
                        # Remove the .html extension from the file name and capitalize it
                        file_name = file.replace('.html', '').capitalize()
                        # Generate a URL based on the file name
                        if file == 'home.html':
                            url = '/'
                            file_name = 'Home'
                        else:
                            url = f"/{file.replace('.html', '')}/"
                        results.append(f'<a href="{url}">{file_name}</a>')

    return results