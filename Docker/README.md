# OmniDB Docker Image

## Build

		$ docker build --tag my-omnidb .
		
## Run

Run detached (`-d`) and link Hostport `9000` to Containerport `9000`.

		$ docker run -p 9000:9000 -d my-omnidb

