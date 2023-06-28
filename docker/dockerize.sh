#!/bin/sh

DIR="$(dirname "$(readlink -f "$0")")"

build() {
  echo "Building ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME} (${CI_COMMIT_BRANCH}) at ${CI_COMMIT_SHORT_SHA}"

  docker build \
    -t ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}_${CI_COMMIT_BRANCH}:$(cat ${DIR}/version) \
    -t ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}_${CI_COMMIT_BRANCH}:latest \
    -t ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}:${CI_COMMIT_SHORT_SHA} \
    -f ${DIR}/Dockerfile ${DIR}/..
}

push() {
  echo "Pushing ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}"

  docker push ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}_${CI_COMMIT_BRANCH}:$(cat ${DIR}/version)
  docker push ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}_${CI_COMMIT_BRANCH}:latest
  docker push ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}:${CI_COMMIT_SHORT_SHA}
}

$1
