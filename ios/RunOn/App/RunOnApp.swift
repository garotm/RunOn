import SwiftUI
import GoogleSignIn

@main
struct RunOnApp: App {
    @StateObject private var authViewModel = AuthenticationViewModel()
    
    var body: some Scene {
        WindowGroup {
            if authViewModel.isAuthenticated {
                TabView {
                    SearchView()
                        .tabItem {
                            Label("Search", systemImage: "magnifyingglass")
                        }
                    
                    EventsView()
                        .tabItem {
                            Label("Events", systemImage: "calendar")
                        }
                }
            } else {
                AuthenticationView()
                    .environmentObject(authViewModel)
            }
        }
    }
} 