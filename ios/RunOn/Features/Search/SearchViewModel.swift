import Foundation

@MainActor
class SearchViewModel: ObservableObject {
    @Published var searchResults: [Event] = []
    @Published var isLoading = false
    @Published var error: String?
    
    private let eventService: EventServiceProtocol
    
    init(eventService: EventServiceProtocol = EventService()) {
        self.eventService = eventService
    }
    
    func search(query: String) {
        guard !query.isEmpty else {
            searchResults = []
            return
        }
        
        isLoading = true
        error = nil
        
        Task {
            do {
                searchResults = try await eventService.searchEvents(query: query)
            } catch let error as APIError {
                self.error = error.message
            } catch {
                self.error = "An unexpected error occurred"
            }
            isLoading = false
        }
    }
    
    func registerForEvent(_ event: Event) {
        Task {
            do {
                try await eventService.registerForEvent(eventId: event.id)
                // Optionally update UI or show success message
            } catch let error as APIError {
                self.error = error.message
            } catch {
                self.error = "Failed to register for event"
            }
        }
    }
} 