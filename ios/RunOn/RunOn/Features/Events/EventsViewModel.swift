import Foundation
import CoreLocation

@MainActor
class EventsViewModel: ObservableObject {
    @Published var events: [Event] = []
    @Published var isLoading = false
    @Published var error: String?
    @Published var userLocation: CLLocation?
    
    private let eventService: EventServiceProtocol
    private let locationManager: CLLocationManager
    
    init(eventService: EventServiceProtocol = EventService()) {
        self.eventService = eventService
        self.locationManager = CLLocationManager()
        setupLocationManager()
    }
    
    private func setupLocationManager() {
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.requestWhenInUseAuthorization()
    }
    
    func loadEvents() {
        isLoading = true
        error = nil
        
        // Start location updates if we don't have a location
        if userLocation == nil {
            locationManager.startUpdatingLocation()
        }
        
        Task {
            do {
                // If we have a location, use it for search
                if let location = userLocation {
                    let coordinate = location.coordinate
                    let query = "near:\(coordinate.latitude),\(coordinate.longitude)"
                    events = try await eventService.searchEvents(query: query)
                } else {
                    // Fallback to fetching all events
                    events = try await eventService.searchEvents(query: "running events")
                }
            } catch let error as APIError {
                self.error = error.message
            } catch {
                self.error = "Failed to load events"
            }
            isLoading = false
        }
    }
    
    func searchEvents(query: String) {
        isLoading = true
        error = nil
        
        Task {
            do {
                events = try await eventService.searchEvents(query: query)
            } catch let error as APIError {
                self.error = error.message
            } catch {
                self.error = "Failed to search events"
            }
            isLoading = false
        }
    }
    
    func refreshEvents() async {
        isLoading = true
        error = nil
        
        do {
            if let location = userLocation {
                let coordinate = location.coordinate
                let query = "near:\(coordinate.latitude),\(coordinate.longitude)"
                events = try await eventService.searchEvents(query: query)
            } else {
                events = try await eventService.fetchUserEvents()
            }
        } catch let error as APIError {
            self.error = error.message
        } catch {
            self.error = "Failed to refresh events"
        }
        
        isLoading = false
    }
}

// MARK: - CLLocationManagerDelegate

extension EventsViewModel: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        userLocation = location
        manager.stopUpdatingLocation()
        
        // Reload events with the new location
        loadEvents()
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("Location manager failed with error: \(error.localizedDescription)")
        // Continue loading events without location
        loadEvents()
    }
    
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        switch manager.authorizationStatus {
        case .authorizedWhenInUse, .authorizedAlways:
            manager.startUpdatingLocation()
        case .denied, .restricted:
            // Load events without location
            loadEvents()
        case .notDetermined:
            // Wait for user decision
            break
        @unknown default:
            loadEvents()
        }
    }
} 