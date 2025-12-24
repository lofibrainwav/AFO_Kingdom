variable "cloudflare_api_token" {
  type      = string
  sensitive = true
}

variable "cloudflare_account_id" {
  type        = string
  description = "Cloudflare Account ID"
}

variable "cloudflare_zone_id" {
  type        = string
  description = "Zone ID for brnestrm.com"
}

variable "tunnel_id" {
  type        = string
  description = "Tunnel ID from Cloudflare dashboard (manual creation)"
}

variable "base_domain" {
  type    = string
  default = "brnestrm.com"
}

variable "tunnel_name" {
  type    = string
  default = "afo-kingdom-tunnel"
}

variable "metrics_hostname" {
  type    = string
  default = "afo-metrics"
}

variable "grafana_hostname" {
  type    = string
  default = "afo-grafana"
}

variable "metrics_service" {
  type    = string
  default = "http://localhost:9091"
}

variable "grafana_service" {
  type    = string
  default = "http://localhost:3100"
}

variable "allowed_emails" {
  type        = list(string)
  description = "Email addresses allowed to access services"
  default     = ["your-email@brnestrm.com"]
}