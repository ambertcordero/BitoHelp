# Paytaca WalletConnect Bug Report: `bch_signTransaction` on Chipnet

## Summary
`bch_signTransaction` requests sent via WalletConnect v2 on chain `bch:bchtest` are published successfully but Paytaca responds immediately with an empty JSON-RPC error object (`{}`), with no error code or message.

## Environment
- App: BiToHelp (Quasar/Vue)
- WalletConnect: v2 (`@walletconnect/sign-client`)
- Wallet: Paytaca
- Chain: `bch:bchtest`
- Network transport: relay

## Proven Request State
All of the following were verified in logs before request submission:
- Session chain: `bch:bchtest`
- Session methods include: `bch_signTransaction`
- Connected account is chipnet cashaddr and matches source output address
- `session_request_sent` is emitted for each request
- Wallet response in history is immediate: `response: { error: {} }`

## Payload Variants Tested
Both variants were published and both rejected with the same empty error:

1. Strict Paytaca-style variant
- `transaction.inputs[*]` without inline `sourceOutput`
- top-level `sourceOutputs`
- `sequenceNumber: 0`
- `broadcast: false`
- `account` included

2. Fallback variant
- same as above, plus inline `input.sourceOutput`

Additional verified details:
- Extended JSON tags used for binary/bigint fields:
  - `<Uint8Array: 0x...>`
  - `<bigint: ...n>`
- Sender/source address matching on chipnet is true (`sameHash: true`, `exactChipnetMatch: true`)

## Actual Behavior
- WalletConnect request is sent (`session_request_sent`)
- Paytaca responds immediately with JSON-RPC error object `{}`
- No code, no message, no structured error payload

## Expected Behavior
- Wallet should either:
  - sign and return `{ signedTransaction, signedTransactionHash }`, or
  - return a structured error with `code` and `message` explaining rejection reason.

## Minimal Example Shape (sanitized)
```json
{
  "method": "bch_signTransaction",
  "params": {
    "account": "bchtest:...",
    "transaction": {
      "version": 2,
      "locktime": 0,
      "inputs": [
        {
          "outpointIndex": 0,
          "outpointTransactionHash": "<Uint8Array: 0x...>",
          "sequenceNumber": 0,
          "unlockingBytecode": "<Uint8Array: 0x>"
        }
      ],
      "outputs": [
        {
          "lockingBytecode": "<Uint8Array: 0x...>",
          "valueSatoshis": "<bigint: 1000n>"
        },
        {
          "lockingBytecode": "<Uint8Array: 0x...>",
          "valueSatoshis": "<bigint: ...n>"
        }
      ]
    },
    "sourceOutputs": [
      {
        "outpointIndex": 0,
        "outpointTransactionHash": "<Uint8Array: 0x...>",
        "sequenceNumber": 0,
        "unlockingBytecode": "<Uint8Array: 0x>",
        "lockingBytecode": "<Uint8Array: 0x...>",
        "valueSatoshis": "<bigint: ...n>"
      }
    ],
    "broadcast": false,
    "userPrompt": "Donate ... BCH to bchtest:..."
  }
}
```

## Notes
This appears to be wallet-side handling for chipnet `bch_signTransaction` because:
- request publication is successful,
- session and account matching are valid,
- multiple payload compatibility variants fail identically,
- and wallet returns opaque `{}` immediately.
