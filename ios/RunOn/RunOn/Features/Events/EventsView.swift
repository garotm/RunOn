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
