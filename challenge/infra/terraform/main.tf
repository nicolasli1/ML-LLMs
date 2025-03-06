terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file("festive-bazaar-452803-c1-9e321ca98eef.json")
}


# Bucket para almacenar imágenes Docker
resource "google_artifact_registry_repository" "docker_repo" {
  provider      = google
  location      = var.region
  repository_id = "ml-llms-api"
  format        = "DOCKER"
}

# Cloud Run Service
resource "google_cloud_run_service" "api_service" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = "${var.image_name}:latest"
        ports {
          container_port = 8080
        }
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
}


# Hacer la API pública
resource "google_cloud_run_service_iam_policy" "public_access" {
  location    = google_cloud_run_service.api_service.location
  service     = google_cloud_run_service.api_service.name
  policy_data = <<EOT
{
  "bindings": [
    {
      "role": "roles/run.invoker",
      "members": ["allUsers"]
    }
  ]
}
EOT
}

# Salida con la URL de la API
output "api_url" {
  value = google_cloud_run_service.api_service.status[0].url
}
