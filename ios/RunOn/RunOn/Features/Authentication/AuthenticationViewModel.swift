import Foundation
import GoogleSignIn
import SwiftUI

@MainActor
class AuthenticationViewModel: ObservableObject {
    @Published var isAuthenticated = false
    @Published var error: String?
    
    func signInWithGoogle() {
        guard let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
              let rootViewController = windowScene.windows.first?.rootViewController else {
            self.error = "Cannot find root view controller"
            return
        }
        
        GIDSignIn.sharedInstance.signIn(withPresenting: rootViewController) { [weak self] result, error in
            guard let self = self else { return }
            
            if let error = error {
                self.error = error.localizedDescription
                return
            }
            
            guard let user = result?.user else {
                self.error = "No user data received"
                return
            }
            
            // Get the access token
            let accessToken = user.accessToken.tokenString
            // Here you would typically send this token to your backend
            print("Access token: \(accessToken)")
            
            // For now, just set isAuthenticated to true
            self.isAuthenticated = true
        }
    }
    
    func signOut() {
        GIDSignIn.sharedInstance.signOut()
        isAuthenticated = false
    }
    
    func checkSignInStatus() {
        if GIDSignIn.sharedInstance.hasPreviousSignIn() {
            GIDSignIn.sharedInstance.restorePreviousSignIn { [weak self] user, error in
                guard let self = self else { return }
                
                if let error = error {
                    self.error = error.localizedDescription
                    return
                }
                
                if user != nil {
                    self.isAuthenticated = true
                }
            }
        }
    }
} 