# Voting App

A simple two-tier voting application where users can vote for either Cat or Dog. Votes are stored in a database. This project demonstrates DevOps practices such as containerization, orchestration, and deployment on a local Kubernetes cluster using Kind.

## Clone the Repository

```sh
git clone https://github.com/selimaynigul/voting-app.git
cd voting-app
```

## Prerequisites

Before starting, ensure you have the following tools installed:

- **Docker & Docker Compose**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **kubectl**: [kubectl Installation Guide](https://kubernetes.io/docs/tasks/tools/)
- **Kind** (Kubernetes IN Docker): [Kind Installation Guide](https://kind.sigs.k8s.io/docs/user/quick-start/)

## Initial Configuration

Create a `.env` file in the project root to store database environment variables:

```sh
touch .env
```

Add the following to `.env`:

```env
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_HOST=db
```

Replace `your_username`, `your_password`, and `your_database` with your desired values.

## Running with Docker Compose

1. **Start the application stack**:

   ```sh
   docker-compose up --build
   ```

   This will start both the web and database containers. The web service waits for the database to be ready.

2. **Access the app**:  
   Open [http://localhost:5000](http://localhost:5000) in your browser to vote.

3. **Test data persistence**:  
   Stop and restart the containers:

   ```sh
   docker-compose down
   docker-compose up
   ```

   Refresh the browser; previous votes should remain.

## Deploying to Kubernetes with Kind

1. **Create a Kind cluster**:

   ```sh
   kind create cluster --name voting-app-cluster --config kind-config.yaml
   ```

2. **Build and load the Docker image**:

   ```sh
   docker build -t voting-app-web:latest ./app
   kind load docker-image voting-app-web:latest --name voting-app-cluster
   ```

3. **Deploy Kubernetes manifests**:

   ```sh
   kubectl apply -f k8s/
   ```

4. **Verify deployment**:

   ```sh
   kubectl get pods
   ```

   Ensure all pods are running.

5. **Access the application**:  
   The web service is exposed via a NodePort. Open [http://localhost:30000](http://localhost:30000) (or your configured NodePort) in your browser.

## Testing Helm Chart (feature/helm branch)

To try out the Helm-based deployment, switch to the Helm feature branch:

```sh
git checkout feature/helm
```

- **Dry-run install** (test templates without deploying):

  ```sh
  helm install voting-app ./voting-app-chart --dry-run --debug
  ```

- **Install Helm chart**:

  ```sh
  helm install voting-app ./voting-app-chart
  ```

  > After installing the Helm chart, the web application is exposed via a NodePort service.  
  > You can access it in your browser at [http://localhost:30000](http://localhost:30000).

- **Uninstall Helm release**:

  ```sh
  helm uninstall voting-app
  ```

- **Package Helm chart** (create a `.tgz` distributable):

  ```sh
  helm package voting-app-chart
  ```

This branch contains the Helm chart templates and allows you to test the deployment in a more configurable way than static manifests.

## Continuous Integration (CI)

The project includes a GitHub Actions workflow at `.github/workflows/ci.yml` that automatically builds and pushes the Docker image to Docker Hub whenever changes are pushed to the main branch.

**Key steps in the workflow:**

- **Checkout code:**

  ```yaml
  - uses: actions/checkout@v3
  ```

- **Set up Docker Buildx (required for building multi-platform images):**

  ```yaml
  - uses: docker/setup-buildx-action@v3
  ```

- **Log in to Docker Hub using secrets:**

  ```yaml
  - uses: docker/login-action@v2
    with:
      username: ${{ secrets.DOCKER_USERNAME }}
      password: ${{ secrets.DOCKER_PASSWORD }}
  ```

- **Build and push Docker image:**
  ```yaml
  - uses: docker/build-push-action@v6
    with:
      context: ./app
      push: true
      tags: ${{ secrets.DOCKER_USERNAME }}/voting-app:latest
  ```

With this CI pipeline, any updates to the main branch automatically produce a new Docker image that can be deployed to your Kubernetes cluster or used locally.
