output "metrics_fqdn" {
  value = "${var.metrics_hostname}.${var.base_domain}"
}

output "grafana_fqdn" {
  value = "${var.grafana_hostname}.${var.base_domain}"
}

output "tunnel_config_id" {
  value = cloudflare_zero_trust_tunnel_cloudflared_config.afo.id
}