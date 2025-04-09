# ERTH Network Registration Server

## Overview

The ERTH Network Registration Server is a secure and privacy-focused service that enables human verification for the ERTH blockchain network. This server processes identity documents, verifies human uniqueness, and registers Keplr wallet addresses to the ERTH network.

## Key Features

- **Privacy-Preserving Identity Verification**: Uses SecretAI vision model to verify identity documents without storing raw personal data
- **Blockchain Integration**: Securely registers verified wallets on the ERTH blockchain
- **Fraud Detection**: Advanced counterfeit detection for identity documents
- **Analytics**: Tracks registration metrics while maintaining privacy

## Architecture

The registration server consists of several key components:

- **API Server**: Flask-based REST API for handling registration requests
- **Verification Service**: Processes ID documents using SecretAI vision model
- **Blockchain Service**: Interacts with ERTH smart contracts to register verified users
- **Analytics Service**: Tracks usage statistics and operational metrics

## Verification Flow

1. User submits their valid ID document and Keplr wallet address
2. Server processes the ID image using SecretAI's vision model
3. The AI extracts and verifies identity information (name, DOB, ID number, etc.)
4. Advanced fraud detection algorithms verify document authenticity
5. If verification succeeds, a privacy-preserving hash of the identity is generated
6. The hash and wallet address are registered on the blockchain
7. Transaction hash and verification status are returned to the user

## Security Considerations

- ID verification occurs in a secure Trusted Execution Environment (TEE)
- Raw identity data is never stored; only cryptographic hashes are used
- All blockchain transactions use Secret Network's privacy-preserving features
- CORS protection limits origins to official websites

## Deployment Requirements

- Python 3.8+
- Secret Network node access
- SecretAI API credentials
- Secure environment variable management
- HTTPS-enabled endpoint

## Configuration

The server is configured through environment variables:

- `SECRET_AI_API_KEY`: API key for SecretAI vision model
- `SECRET_NETWORK_RPC`: RPC endpoint for Secret Network
- `CONTRACT_ADDRESS`: ERTH registration contract address
- `SERVER_WALLET_KEY`: Path to server wallet keyfile
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

## Future Development

- Additional biometric verification methods
- Decentralized identity integration
- Enhanced privacy features
- Support for additional blockchain wallets

---

ERTH Network - Secure, Private, Human