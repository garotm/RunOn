import Foundation

struct Event: Identifiable, Codable {
    let id: String
    let name: String
    let date: Date
    let location: String
    let description: String
    let distance: Double // in kilometers
    let registrationDeadline: Date
    
    var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .long
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
    
    var formattedDistance: String {
        return String(format: "%.1f km", distance)
    }
} 