import Foundation

@MainActor
class EventsViewModel: ObservableObject {
    @Published var events: [Event] = []
    @Published var isLoading = false
    @Published var error: String?
    
    private let eventService: EventServiceProtocol
    
    init(eventService: EventServiceProtocol = EventService()) {
        self.eventService = eventService
    }
    
    func loadEvents() {
        isLoading = true
        error = nil
        
        Task {
            do {
                events = try await eventService.fetchUserEvents()
            } catch let error as APIError {
                self.error = error.message
            } catch {
                self.error = "Failed to load events"
            }
            isLoading = false
        }
    }
    
    func unregisterFromEvent(_ event: Event) {
        Task {
            do {
                try await eventService.unregisterFromEvent(eventId: event.id)
                // Remove the event from the list
                events.removeAll { $0.id == event.id }
            } catch let error as APIError {
                self.error = error.message
            } catch {
                self.error = "Failed to unregister from event"
            }
        }
    }
    
    func refreshEvents() async {
        isLoading = true
        error = nil
        
        do {
            events = try await eventService.fetchUserEvents()
        } catch let error as APIError {
            self.error = error.message
        } catch {
            self.error = "Failed to refresh events"
        }
        
        isLoading = false
    }
} 