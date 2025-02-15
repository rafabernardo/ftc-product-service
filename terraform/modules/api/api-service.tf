resource "kubernetes_service" "fastapi_service" {
  metadata {
    name      = "api-service"
  }

  spec {
    selector = {
      app = "api-deployment"
    }

    port {
      port        = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}