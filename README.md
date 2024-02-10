# Social Networks Analyzer

## Local Deployment

### Docker startup

Inside of the repository directory run the following commands:
```shell
export REDDIT_CLIENT_KEY=<REDDIT_CLIENT_KEY>
export REDDIT_CLIENT_SECRET=<REDDIT_CLIENT_SECRET>
export YOUTUBE_API_KEY=<YOUTUBE_API_KEY>

docker build --tag social-network-analyzer .
docker-compose up --build
```

### Docker shutdown

```shell
docker-compose down
```

### Direct app startup
You also can locally start the app even without docker:
```shell
panel serve src/app.py --autoreload --port 5008
```