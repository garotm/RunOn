import SwiftUI

struct EventsView: View {
    @StateObject private var viewModel = EventsViewModel()
    
    var body: some View {
        NavigationView {
            ZStack {
                List {
                    if viewModel.events.isEmpty {
                        Text("No registered events")
                            .foregroundColor(.secondary)
                    } else {
                        ForEach(viewModel.events) { event in
                            EventRow(event: event)
                                .swipeActions {
                                    Button("Unregister", role: .destructive) {
                                        viewModel.unregisterFromEvent(event)
                                    }
                                }
                        }
                    }
                }
                .refreshable {
                    await viewModel.refreshEvents()
                }
                .overlay {
                    if viewModel.isLoading {
                        ProgressView()
                    }
                }
                
                if let error = viewModel.error {
                    VStack {
                        Text(error)
                            .foregroundColor(.red)
                            .padding()
                            .background(
                                RoundedRectangle(cornerRadius: 8)
                                    .fill(Color(.systemBackground))
                                    .shadow(radius: 2)
                            )
                    }
                    .padding()
                }
            }
            .navigationTitle("My Events")
        }
        .onAppear {
            viewModel.loadEvents()
        }
    }
}

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