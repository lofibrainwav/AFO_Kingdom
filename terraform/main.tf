# Tunnel Configuration (IaC 관리)
resource "cloudflare_zero_trust_tunnel_cloudflared_config" "afo" {
  account_id = var.cloudflare_account_id
  tunnel_id  = var.tunnel_id

  config {
    ingress_rule {
      hostname = "${var.metrics_hostname}.${var.base_domain}"
      service  = var.metrics_service
    }

    ingress_rule {
      hostname = "${var.grafana_hostname}.${var.base_domain}"
      service  = var.grafana_service
    }

    ingress_rule {
      service = "http_status:404"
    }
  }
}

# DNS Records
resource "cloudflare_record" "metrics" {
  zone_id = var.cloudflare_zone_id
  name    = var.metrics_hostname
  type    = "CNAME"
  value   = "${var.tunnel_id}.cfargotunnel.com"
  proxied = true
}

resource "cloudflare_record" "grafana" {
  zone_id = var.cloudflare_zone_id
  name    = var.grafana_hostname
  type    = "CNAME"
  value   = "${var.tunnel_id}.cfargotunnel.com"
  proxied = true
}

# Zero Trust Access Applications
resource "cloudflare_zero_trust_access_application" "metrics" {
  zone_id          = var.cloudflare_zone_id
  name             = "AFO Metrics Access"
  domain           = "${var.metrics_hostname}.${var.base_domain}"
  session_duration = "24h"
}

resource "cloudflare_zero_trust_access_application" "grafana" {
  zone_id          = var.cloudflare_zone_id
  name             = "AFO Grafana Access"
  domain           = "${var.grafana_hostname}.${var.base_domain}"
  session_duration = "24h"
}

# Zero Trust Access Policies
resource "cloudflare_zero_trust_access_policy" "metrics" {
  application_id = cloudflare_zero_trust_access_application.metrics.id
  zone_id        = var.cloudflare_zone_id
  name           = "Metrics Access Policy"
  precedence     = 1
  decision       = "allow"

  include {
    email = var.allowed_emails
  }
}

resource "cloudflare_zero_trust_access_policy" "grafana" {
  application_id = cloudflare_zero_trust_access_application.grafana.id
  zone_id        = var.cloudflare_zone_id
  name           = "Grafana Access Policy"
  precedence     = 1
  decision       = "allow"

  include {
    email = var.allowed_emails
  }
}