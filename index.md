---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

{{ site.url }} / 
{{ jekyll.environment }}
<div>
    <ul>
        <li><a href="{{ site.baseurl }}/gallery">Gallery</a></li>
        <li><a href="{{ site.baseurl }}/museum.json">museum.json</a></li>
    </ul>
    {% for artwork in site.data.museum.artworks %}
        <hr>
        <div>{{ artwork.artist }}</div>
        <div><i>{{ artwork.title }}, {{ artwork.year }}</i></div>
        <div>
            <img src="{{ artwork.url }}" alt="{{ artwork.title }}" width="300">
        </div>
        <div>{{ artwork.description }}</div>
    {% endfor %}
</div>