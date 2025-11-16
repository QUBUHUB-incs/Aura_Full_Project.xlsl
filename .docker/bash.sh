docker push kubuverse/aura:ghcr.io
docker push kubuverse/aura:app.docker.com
docker tag localhost.dev[:aura] kubuverse/aura:ghcr.io
docker push kubuverse/aura:ghcr.io
 docker tag my-app my-namespace/my-repo:v1.0
 docker push my-namespace/my-repo:v1.0
