#### This is a fork of https://github.com/thomashacker/weaviate-magic-chat-demo.git



![Alt text](/static/screenshot.png "Screenshot")


# Local Setup

## With docker

Build the container:
```bash
docker build -t hitchhiker . 
```

Run the container:
- Ensure that a weaviate cluster is accessible at localhost:8080 (with a GRPC port on 50051)

```bash
docker run -e WEAVIATE_API_KEY='secr3tk3y' -e WEAVIATE_URL='docker.host.internal' -e OPENAI_KEY='<your-open-ai-key-here>' -it --rm -p 8501:8501 --name hitchhiker hitchhiker --network=host
```

## Building the image for running in GKE

- see './build-and-push.sh'


## Without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

(Assuming you have an accessible Weaviate cluster and have configured your WEAVIATE_URL, WEAVIATE_API_KEY, and OPENAI_KEY env vars accordingly):

```bash
python initialize_data.py
streamlit run streamlit_app.py
```

