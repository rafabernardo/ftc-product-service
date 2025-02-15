resource "kubernetes_deployment" "api-deployment" {
  metadata {
    name = "api-deployment"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "api-deployment"
      }
    }
    template {
      metadata {
        labels = {
          app = "api-deployment"
        }
      }
      spec {
        container {
          image = "${var.api_image}:latest"
          name  = "api-deployment"


          resources {
            limits = {
              cpu    = "1500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "1m"
              memory = "256Mi"
            }
          }

          port {
            container_port = 80
          }
          env {
            name  = "API_PORT"
            value = "80"
          }
          env {
            name  = "MONGO_DATABASE"
            value = "database_test"
          }
          env {
            name  = "MONGO_URI"
            value = var.db_url
          }

        }
      }
    }
  }
}

