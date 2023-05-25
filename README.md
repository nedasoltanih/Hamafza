This is a Blog project which includes API's for the below:
- An API for getting token:
```curl
curl -X POST -H "Content-Type: application/json" -d '{
    "username": "your_username",
    "password": "your_password"
}' http://127.0.0.1:8000/token/
```

  
- An API for the authors to view and edit profile: 
```curl
curl -X GET -H "Authorization: Token your_token" http://127.0.0.1:8000/profile/
```

```curl
curl -X PUT -H "Authorization: Token your_token" -d '{
    "age": "Your age",
    "about": "Your about in text",
    "image": "Your profile image path"
}' http://127.0.0.1:8000/profile/
```

- An API for the authors to view articles or create an article: 
```curl
curl -X GET -H "Authorization: Token your_token" http://127.0.0.1:8000/my_articles/
```

```curl
curl -X POST -H "Authorization: Token your_token"  -d '{
        "title": "Article title",
        "content": "Article content",
        "published": "true or false",
        "publish_date": "Date to publish article",
        "badge": ["list of predefined badges"],
        "images": ["list of image pathes"]
}' http://127.0.0.1:8000/my_articles/
```

- An API for the authors to view an article, edit or delete it: 

```curl
curl -X GET -H "Authorization: Token your_token" http://127.0.0.1:8000/my_articles/<article_id>
```

```curl
curl -X POST -H "Authorization: Token your_token"  -d '{
        "title": "Article title",
        "content": "Article content",
        "published": "true or false",
        "publish_date": "Date to publish article",
        "badge": ["list of predefined badges"],
        "images": ["list of image pathes"]
}' http://127.0.0.1:8000/my_articles/<article_id>/
```

- A public API to view badges:
```curl
curl -X GET http://127.0.0.1:8000/badges/
```

- A public API to view authors, search by firstname and lastname, 
  or filter based on badges, articles count:
```curl
curl -X GET http://127.0.0.1:8000/authors/
```

```curl
curl -X GET http://127.0.0.1:8000/authors/?search="your search query here"
&?count="number of articles here"
&?article__badge="your desired badge here"
```

- A public API to view articles, search by title and content, 
  or filter based on publish date, username or badge
  
```curl
curl -X GET http://127.0.0.1:8000/articles/?search="your search query here"
&?publish_date="publish date here"
&?author__user__username="author's username here"
&?badge__text="your desired badge here"
```