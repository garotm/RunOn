import Foundation
import Alamofire

// Search request models to match Pydantic structure
struct SearchQuery: Encodable {
    let query: String
    let loc: String
}

struct SearchRequest: Encodable {
    let query: SearchQuery
}

protocol EventServiceProtocol {
    func searchEvents(query: String) async throws -> [Event]
    func fetchUserEvents() async throws -> [Event]
    func registerForEvent(eventId: String) async throws
    func unregisterFromEvent(eventId: String) async throws
}

class EventService: EventServiceProtocol {
    private let apiClient: APIClient
    
    init(apiClient: APIClient = APIClient()) {
        self.apiClient = apiClient
    }
    
    func searchEvents(query: String) async throws -> [Event] {
        let parameters = ["query": query]
        // Directly decode the response as [Event]
        return try await apiClient.request("/events/search",
                                         method: .post,
                                         parameters: parameters,
                                         encoding: URLEncoding.queryString)
    }
    
    func fetchUserEvents() async throws -> [Event] {
        return try await apiClient.request("/events/user")
    }
    
    func registerForEvent(eventId: String) async throws {
        let _: EmptyResponse = try await apiClient.request("/events/\(eventId)/register",
                                                       method: .post)
    }
    
    func unregisterFromEvent(eventId: String) async throws {
        let _: EmptyResponse = try await apiClient.request("/events/\(eventId)/unregister",
                                                       method: .delete)
    }
}

// Helper type for endpoints that return no data
private struct EmptyResponse: Decodable {} 