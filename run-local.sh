docker stop tomatoai-django-demo-local

docker run --rm -it -d \
    --name tomatoai-django-demo-local \
    -v ./app:/app \
    tomatoai-django-demo