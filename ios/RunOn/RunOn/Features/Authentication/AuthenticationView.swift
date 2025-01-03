import SwiftUI
import GoogleSignInSwift

struct AuthenticationView: View {
    @EnvironmentObject var viewModel: AuthenticationViewModel
    
    var body: some View {
        VStack(spacing: 24) {
            Spacer()
            
            VStack(spacing: 12) {
                Text("Welcome to RunOn")
                    .font(.system(size: 32, weight: .bold))
                    .multilineTextAlignment(.center)
                
                Text("Sign in to get started")
                    .font(.system(size: 16))
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            GoogleSignInButton(scheme: .dark, style: .wide, state: .normal) {
                print("Sign in button tapped")
                viewModel.signInWithGoogle()
            }
            .frame(height: 48)
            .padding(.horizontal, 24)
            
            Spacer()
                .frame(height: 48)
        }
        .padding()
        .alert("Sign In Error",
               isPresented: Binding(
                get: { viewModel.error != nil },
                set: { if !$0 { viewModel.error = nil } }
               )) {
            Button("OK") {
                viewModel.error = nil
            }
        } message: {
            Text(viewModel.error ?? "An unknown error occurred")
        }
        .onChange(of: viewModel.isAuthenticated) { newValue in
            print("AuthenticationView: isAuthenticated changed to \(newValue)")
        }
    }
} 