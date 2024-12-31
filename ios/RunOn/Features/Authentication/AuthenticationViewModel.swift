import SwiftUI
import GoogleSignIn

class AuthenticationViewModel: ObservableObject {
    @Published var isAuthenticated = false
    
    func signInWithGoogle() {
        guard let clientID = Bundle.main.object(forInfoDictionaryKey: "GIDClientID") as? String else {
            print("Error: No Google Sign In client ID found")
            return
        }
        
        let config = GIDConfiguration(clientID: clientID)
        
        guard let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
              let window = windowScene.windows.first,
              let rootViewController = window.rootViewController else {
            print("Error: No root view controller found")
            return
        }
        
        GIDSignIn.sharedInstance.signIn(with: config, presenting: rootViewController) { [weak self] user, error in
            if let error = error {
                print("Error signing in with Google: \(error.localizedDescription)")
                return
            }
            
            self?.isAuthenticated = true
        }
    }
} 