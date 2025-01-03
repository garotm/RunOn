import Foundation

struct Event: Identifiable, Codable {
    let id: String
    let name: String
    let date: Date
    let location: String
    let description: String
    let url: String
    
    // Optional fields with default values
    let distance: Double = 0.0 // Will be populated later
    let registrationDeadline: Date // Default to a month from the event date
    
    var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .long
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
    
    var formattedDistance: String {
        return String(format: "%.1f km", distance)
    }
    
    enum CodingKeys: String, CodingKey {
        case id = "id"
        case name = "name"
        case date = "date"
        case location = "location"
        case description = "description"
        case url = "url"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        
        // Decode basic fields
        id = try container.decodeIfPresent(String.self, forKey: .id) ?? UUID().uuidString
        name = try container.decode(String.self, forKey: .name)
        location = try container.decode(String.self, forKey: .location)
        description = try container.decode(String.self, forKey: .description)
        url = try container.decode(String.self, forKey: .url)
        
        // Handle date decoding with ISO8601 format
        let dateString = try container.decode(String.self, forKey: .date)
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        
        if let parsedDate = formatter.date(from: dateString) {
            date = parsedDate
        } else {
            // Fallback to current date if parsing fails
            print("Warning: Failed to parse date string: \(dateString)")
            date = Date()
        }
        
        // Set registrationDeadline to a month before the event date
        registrationDeadline = date.addingTimeInterval(-30 * 24 * 60 * 60)
    }
    
    init(id: String, name: String, date: Date, location: String, description: String, distance: Double, registrationDeadline: Date) {
        self.id = id
        self.name = name
        self.date = date
        self.location = location
        self.description = description
        self.url = "" // Default empty URL for manually created events
        self.registrationDeadline = registrationDeadline
    }
} 