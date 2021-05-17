# greenpeace_blog_ptbr_crawler

## This is a python script for scraping the [Brazilian Greenpeace Blog](https://www.greenpeace.org/brasil/blog/)

This spider crawls the blog and returns the posts released officialy by the Greenpeace team.

The solution is Dokerized and can be run by building the container immage in a linux terminal, from the Dockerfile, with:

```shell
docker build -t gp_scraper:1.0 ./
```

then run the container with:

```shell
docker run --rm --name teste1 -v $(pwd)/data:/usr/src/app/data/ gp_scraper:1.0
```

The textfile is returned in the ./data folder
