# Voting App

A simple two-tier voting application where users can vote for either Cat or Dog. Votes are stored in a database. This project demonstrates DevOps practices such as containerization, orchestration, and deployment on a local Kubernetes cluster using Kind.

## Prerequisites

Before starting, ensure you have the following tools installed:

- **Git**: [Download Git](https://git-scm.com/downloads)
- **Docker & Docker Compose**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Kind** (Kubernetes IN Docker): [Kind Installation Guide](https://kind.sigs.k8s.io/docs/user/quick-start/)
- **kubectl**: [kubectl Installation Guide](https://kubernetes.io/docs/tasks/tools/)

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
