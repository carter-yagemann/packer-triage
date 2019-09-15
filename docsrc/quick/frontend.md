# Frontend

The frontend container hosts the HTTP API for submitting samples and getting results.
It also coordinates all the worker container instances.

## Starting a frontend instance

Simply run the script: `./run/frontend.sh`

## Submitting samples

Files can be submitted via the `/api/submit` API:

    $ curl -X POST -F file=@test/samples/hello-upx.exe http://localhost:9000/api/submit
    {
      "response": {
        "code": 0,
        "description": "OK"
      },
      "data": "6d5f014693090970c6b0b6052913e2e41c2258f8dd7820bc1da93a648d308351"
    }

Note the value returned in the `data` field. You'll need this to get the result.

## Getting results

Use the `/api/results/<hash>` API:

    $ curl http://localhost:9000/api/results/6d5f014693090970c6b0b6052913e2e41c2258f8dd7820bc1da93a648d308351
    {
      "response": {
        "code": 0,
        "description": "OK"
      },
      "data": { . . . }
    }
