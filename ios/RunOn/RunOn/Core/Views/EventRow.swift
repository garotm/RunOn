import SwiftUI

struct EventRow: View {
    let event: Event
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(event.name)
                .font(.headline)
            Text(event.formattedDate)
                .font(.subheadline)
                .foregroundColor(.secondary)
            Text(event.location)
                .font(.subheadline)
                .foregroundColor(.secondary)
            Text(event.formattedDistance)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
} 