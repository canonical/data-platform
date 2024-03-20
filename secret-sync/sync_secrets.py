from base64 import b64encode

import requests
from nacl import encoding, public


def encrypt(public_key_: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key_ = public.PublicKey(public_key_.encode("utf-8"), encoding.Base64Encoder)
    sealed_box = public.SealedBox(public_key_)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


REPOS = [
    "charm-rolling-ops",
    "charmed-kafka-rock",
    "charmed-kafka-snap",
    "charmed-mongodb-rock",
    "charmed-mongodb-snap",
    "charmed-mysql-rock",
    "charmed-mysql-snap",
    "charmed-opensearch-rock",
    "charmed-postgresql-rock",
    "charmed-postgresql-snap",
    "charmed-redis-rock",
    "charmed-spark-rock",
    "charmed-zookeeper-rock",
    "charmed-zookeeper-snap",
    "data-integrator",
    "data-platform",
    "data-platform-libs",
    "data-platform-workflows",
    "kafka-bundle",
    "kafka-k8s-bundle",
    "kafka-k8s-operator",
    "kafka-operator",
    "kafka-test-app",
    "mongodb-k8s-operator",
    "mongodb-operator",
    "mysql-bundle",
    "mysql-k8s-bundle",
    "mysql-k8s-operator",
    "mysql-operator",
    "mysql-router-container",
    "mysql-router-k8s-operator",
    "mysql-router-operator",
    "mysql-router-snap",
    "mysql-test-app",
    "opensearch-operator",
    "opensearch-snap",
    "pgbouncer-container",
    "pgbouncer-k8s-operator",
    "pgbouncer-operator",
    "postgresql-bundle",
    "postgresql-k8s-bundle",
    "postgresql-k8s-operator",
    "postgresql-operator",
    "postgresql-patroni-container",
    "redis-k8s-operator",
    "redis-operator",
    "s3-integrator",
    "snap-mysqld-exporter",
    "spark-client-snap",
    "spark-history-server-k8s-operator",
    "xtrabackup-snap",
    "zookeeper-k8s-operator",
    "zookeeper-operator",
]
GITHUB_USERNAME = "carlcsaposs-canonical"
# create classic personal access token with "repo" scope
GITHUB_TOKEN = "foo"

# TODO: use github ci workflow to grab secrets from this repo & copy to other repos
SECRETS = {
    "JIRA_API_TOKEN": "foo",
    "JIRA_USER_EMAIL": "foo",
}

REQUEST_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

for repo in REPOS:
    request = requests.get(
        f"https://api.github.com/repos/canonical/{repo}/actions/secrets/public-key",
        headers=REQUEST_HEADERS,
        auth=(GITHUB_USERNAME, GITHUB_TOKEN),
    )
    request.raise_for_status()
    response = request.json()
    public_key = response["key"]
    public_key_id = response["key_id"]
    for name, secret in SECRETS.items():
        request = requests.put(
            f"https://api.github.com/repos/canonical/{repo}/actions/secrets/{name}",
            headers=REQUEST_HEADERS,
            auth=(GITHUB_USERNAME, GITHUB_TOKEN),
            json={"encrypted_value": encrypt(public_key, secret), "key_id": public_key_id},
        )
        request.raise_for_status()
