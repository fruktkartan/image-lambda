AWS lambda function for validating, cropping and re-scaling incoming images to fruktkartan.se.

## Installation

```sh
cp .env.sample .env
pip install -r requirements/dev.txt
```

The `.env.sample` file contains defaults for the environment variables used. You need to set these variables somehow, e.g. by copying them to a `.env` file.

You will also need to setup credentials for AWS S3 access (see https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html for various ways to do this)

Not that the `requirements/prod.txt` file does _not_ contain `boto3`, as this is preinstalled in our production environment, AWS Lambda.

## Running

```sh
./resize.py --help
```

## Licences

Test images, see description pages at Wikimedia Commons:

- Körsbärsträd.jpg: https://commons.wikimedia.org/wiki/File:Fr%C3%BChling_bl%C3%BChender_Kirschenbaum.jpg
