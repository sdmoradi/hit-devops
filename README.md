# DevOps Challenge

### Getting Started

To complete the challenge you should complete the following steps:

1. Clone the project in a version control system of your choice

2. Create a CI/CD pipeline that does the following
    - Bumps the version in `version.txt`
        - If there are changes in `requirements.txt` you should bump the major version
        - If there are changes in the code you should bump the minor version
        - If there are changes in `README.md` you should bump the patch version
    - Create a container image with a tag equal to the version
    - Deploy it on a Kubernetes cluster

4. Change the code to print a log with the following format to STDOUT:
    
    ```json
    {
        "url": "hit.local/version",
        "time": "2022-01-01 14:22:33",
        "client_ip": "0.0.0.0",
        "service_name": "medusa"
    }
    ```

5. Deploy a log management service (e.g. Elasticsearch)

6. Redirect logs to the log management service

7. Deploy a GUI for the log management service and create a histogram for client IPs

## Build and Test

Execute the above-mentioned steps on your desired platform and make them ready for a code review session (demo).

## Rules

There are no rules for this challenge.

You are free to use any software, tool or procedure to complete the challenge.

Happy building 🏗️


## Implementation notes

### CI/CD prerequisites

Configure these repository secrets before merging to `master`:

- `DOCKER_HUB_USERNAME` and `DOCKER_HUB_ACCESS_TOKEN`: credentials for the Docker Hub account that can push `sdmoradi/hit-app`.
- `KUBE_CONFIG`: base64-encoded kubeconfig for the target cluster.

The release workflow expects the Kubernetes namespace `test` to exist. It bumps the version once per change set, using precedence `requirements.txt` (major), application/container/deployment code (minor), and README-only changes (patch). Pull requests validate the Python application and build the container without publishing or deploying it.

### Request logs and Kibana

The app emits one compact JSON object per request to stdout. Filebeat decodes the JSON message into fields before sending events to Elasticsearch.

Apply the ELK manifests in a cluster where namespace `elk` exists and a default StorageClass is configured:

```sh
kubectl apply -f elk-manifests/elastic.yml
kubectl apply -f elk-manifests/kibana.yaml
kubectl apply -f elk-manifests/filebeat-kubernetes.yaml
kubectl apply -f elk-manifests/client-ip-histogram.yaml
kubectl -n elk wait --for=condition=complete job/client-ip-histogram-import --timeout=180s
kubectl -n elk port-forward svc/kibana 5601:5601
```

Open `http://localhost:5601` and find **Requests by client IP** in Kibana's Visualize library. The saved visualization groups requests by `client_ip` and filters for `service_name : medusa`.

**Security warning:** this challenge configuration disables Elasticsearch/Kibana authentication for a simple local demo. Kibana is intentionally ClusterIP-only; use port-forward and do not expose Elasticsearch or Kibana to the public internet. For production, enable security, TLS, and secret-managed credentials before exposing the UI.
