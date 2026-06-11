# Delfos

Delfos is a service developed by OpenNova that scans high demand information topics and assings them a risk score.

## How it works

Delfos runs as a Celery worker and is triggered through asynchronous tasks.

When a task is received:

1. Google trends is scrapped for todays hot topics.
2. Todays news are retrieved from paper defined in config.json
3. A LLM is used to analize those news related to retrieved topics
4. Information voids score is calculated using that information
5. Results are uploaded back to S3, notified to an external API and an email is sended

## Dependencies

In order to run this service, you need.

1. An AzureOpenAI api key
2. A gpt-4o-mini model deployed
3. A serpapi api key to scrap google trends
4. AWS S3 bucket
5. A config.json file either in S3 for production or in root file for local execution

## Config

Config .json file must have this form:
```javascript
{
  "1": {
      "description": "Some description",
      "news_origin": [
        {
          "name": "Paper Name",
          "url": "https://paperurl.com/",
          "lang": "lang"
        }
      ],
      "skip_urls": [],
      "trend_filter": ["filters", "from", "google", "trends"]
    }
}
```

The config id to use should be indicated as env var.

## Running with Docker

Build the image:

```bash
docker build -t delfos .
```

Run the container:

```bash
docker run delfos
```

Configuration is provided through environment variables and access to the corresponding S3 buckets, OAI and Serpapi

## Organization

This project is maintained by **OpenNova**.

---

# License
Licensed under LGPL-2.1. See [LICENSE](./LICENSE) and [NOTICE](./NOTICE.md) for details.
