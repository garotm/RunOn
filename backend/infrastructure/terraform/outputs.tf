output "function_urls" {
  description = "URLs of deployed Cloud Functions"
  value = {
    event_discovery = google_cloudfunctions_function.event_discovery.https_trigger_url
    user_management = google_cloudfunctions_function.user_management.https_trigger_url
    calendar_sync   = google_cloudfunctions_function.calendar_sync.https_trigger_url
  }
} 