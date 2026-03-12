# Paytaca BCH WalletConnect Chipnet Repro

## Summary

`bch_signTransaction` is published successfully from BitoHelp to Paytaca over WalletConnect v2 on `bch:bchtest`, but Paytaca immediately responds with an empty JSON-RPC error object:

```json
{ "error": {} }
```

This happens for both of the BCH payload variants tested:

1. Strict Paytaca-style payload
2. Fallback payload with inline `transaction.inputs[0].sourceOutput`

The request reaches the wallet, the session is valid, and the sender/source output address matches exactly on chipnet.

## Environment

- App: BitoHelp
- Frontend: Quasar SPA / Vue 3
- WalletConnect chain: `bch:bchtest`
- Wallet: Paytaca
- Network: BCH chipnet

## Verified Session State

- `walletSession.chain = "bch:bchtest"`
- `walletSession.transportType = "relay"`
- `walletSession.sessionConfig.disableDeepLink = true`
- `walletSession.methods = ["bch_signTransaction", "bch_signMessage"]`
- `walletSession.accounts = ["bch:bchtest:qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy3hx3gpye"]`

## Verified Address Matching

Compatibility log before signing:

```json
{
  "walletAddress": "bchtest:qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy3hx3gpye",
  "walletHashOnly": "qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy3hx3gpye",
  "sourceAddressMainnet": "bitcoincash:qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy49zk2kr9",
  "sourceAddressChipnet": "bchtest:qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy3hx3gpye",
  "sourceHashOnly": "qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy3hx3gpye",
  "sameHash": true,
  "exactChipnetMatch": true
}
```

This rules out sender/source-output address mismatch in the dapp payload.

## Attempt 1: Strict Payload

Pre-send summary:

```json
{
  "inputCount": 1,
  "outputCount": 2,
  "sourceOutputCount": 1,
  "everyInputHasInlineSourceOutput": false,
  "hasAccount": true,
  "account": "bchtest:qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy3hx3gpye",
  "broadcast": false,
  "locktime": 0,
  "version": 2
}
```

Published WalletConnect request shape:

```json
{
  "method": "bch_signTransaction",
  "params": {
    "broadcast": false,
    "userPrompt": "Donate 0.00001 BCH to bchtest:qz52lge5xnwug9y7h4vu9f9rt0jalv4mpqfe0mvyhp",
    "account": "bchtest:qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy3hx3gpye",
    "sourceOutputs": [
      {
        "outpointIndex": 0,
        "outpointTransactionHash": "<Uint8Array: 0x2e187eb59831c1c614c615a601cb3d9400415e183edb014aef702d965f16c86a>",
        "sequenceNumber": 0,
        "unlockingBytecode": "<Uint8Array: 0x>",
        "lockingBytecode": "<Uint8Array: 0x76a914ade3f06dd9d350ca93bfc34c2f842521c13ec0c188ac>",
        "valueSatoshis": "<bigint: 9998419n>"
      }
    ],
    "transaction": {
      "version": 2,
      "locktime": 0,
      "inputs": [
        {
          "outpointIndex": 0,
          "outpointTransactionHash": "<Uint8Array: 0x2e187eb59831c1c614c615a601cb3d9400415e183edb014aef702d965f16c86a>",
          "sequenceNumber": 0,
          "unlockingBytecode": "<Uint8Array: 0x>"
        }
      ],
      "outputs": [
        {
          "lockingBytecode": "<Uint8Array: 0x76a914a8afa33434ddc4149ebd59c2a4a35be5dfb2bb0888ac>",
          "valueSatoshis": "<bigint: 1000n>"
        },
        {
          "lockingBytecode": "<Uint8Array: 0x76a914ade3f06dd9d350ca93bfc34c2f842521c13ec0c188ac>",
          "valueSatoshis": "<bigint: 9997147n>"
        }
      ]
    }
  }
}
```

WalletConnect history for the published request contains:

```json
{
  "response": {
    "error": {}
  }
}
```

## Attempt 2: Fallback Payload

Pre-send summary:

```json
{
  "inputCount": 1,
  "outputCount": 2,
  "sourceOutputCount": 1,
  "everyInputHasInlineSourceOutput": true,
  "hasAccount": true,
  "account": "bchtest:qzk78urdm8f4pj5nhlp5ctuyy5suz0kqcy3hx3gpye",
  "broadcast": false,
  "locktime": 0,
  "version": 2
}
```

Difference from attempt 1:

- `transaction.inputs[0].sourceOutput` is included inline in addition to top-level `sourceOutputs`

Result is the same:

```json
{
  "response": {
    "error": {}
  }
}
```

## Conclusion

At this point the dapp has verified all of the following:

- WalletConnect session is valid for `bch:bchtest`
- `bch_signTransaction` is allowed by the session
- Request is published successfully to Paytaca
- Paytaca responds immediately, so this is not a transport timeout
- Sender/source-output address matches exactly on chipnet
- Both known parameter shapes were tested:
  - strict payload
  - inline `input.sourceOutput` fallback
- `account` is included in the signing params

The remaining issue appears to be inside Paytaca's WalletConnect BCH chipnet signing flow, which is rejecting the request internally without exposing a message/code/reason.

## Suggested Upstream Checks

1. Add diagnostic logging around Paytaca's `respondToSignTransactionRequest` catch path so the original error is preserved instead of returning `{ error: {} }`.
2. Confirm Paytaca's chipnet BCH signer accepts `bch_signTransaction` on `bch:bchtest` with P2PKH inputs built from extended JSON tags.
3. Confirm no internal validation requires mainnet-only cashaddr handling or a hidden field beyond:
   - `transaction`
   - `sourceOutputs`
   - `broadcast`
   - `userPrompt`
   - optional `account`
4. Confirm both parser/signer paths behave consistently when `input.sourceOutput` is absent vs present.

## Current BitoHelp Status

BitoHelp should treat this as an external wallet limitation/bug unless Paytaca documents an additional required field for chipnet `bch_signTransaction`.
