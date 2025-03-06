variable "project_id" {
  description = "ID del proyecto en GCP"
  type        = string
}

variable "region" {
  description = "Región de despliegue en GCP"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Nombre del servicio de Cloud Run"
  type        = string
  default     = "ml-llms-api"
}

variable "image_name" {
  description = "Nombre de la imagen en Artifact Registry"
  type        = string
  default     = "gcr.io/festive-bazaar-452803-c1/ml-api"
}
