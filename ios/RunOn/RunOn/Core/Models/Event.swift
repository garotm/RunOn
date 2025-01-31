import Foundation

struct Event: Identifiable, Codable {
    let id: String
    let name: String
    let date: Date
    let location: String
    let description: String
    let url: String
    let distance: Double
    let coordinates: Coordinates?
    
    struct Coordinates: Codable {
        let latitude: Double
        let longitude: Double
    }
    
    var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .long
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
    
    var formattedDistance: String {
        return String(format: "%.1f km", distance)
    }
    
    var time: String {
        let formatter = DateFormatter()
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
    
    enum CodingKeys: String, CodingKey {
        case id
        case name
        case date
        case location
        case description
        case url
        case distance
        case coordinates
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        
        // Decode basic fields
        id = try container.decodeIfPresent(String.self, forKey: .id) ?? UUID().uuidString
        name = try container.decode(String.self, forKey: .name)
        location = try container.decode(String.self, forKey: .location)
        description = try container.decode(String.self, forKey: .description)
        url = try container.decode(String.self, forKey: .url)
        distance = try container.decodeIfPresent(Double.self, forKey: .distance) ?? 0.0
        
        // Handle date decoding with ISO8601 format
        let dateString = try container.decode(String.self, forKey: .date)
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        
        if let parsedDate = formatter.date(from: dateString) {
            date = parsedDate
        } else {
            print("Warning: Failed to parse date string: \(dateString)")
            date = Date()
        }
        
        // Decode coordinates if present
        if let coords = try container.decodeIfPresent([String: Double].self, forKey: .coordinates),
           let lat = coords["latitude"],
           let lon = coords["longitude"] {
            coordinates = Coordinates(latitude: lat, longitude: lon)
        } else {
            coordinates = nil
        }
    }
    
    init(id: String = UUID().uuidString,
         name: String,
         date: Date,
         location: String,
         description: String,
         url: String = "",
         distance: Double = 0.0,
         coordinates: Coordinates? = nil) {
        self.id = id
        self.name = name
        self.date = date
        self.location = location
        self.description = description
        self.url = url
        self.distance = distance
        self.coordinates = coordinates
    }
} 