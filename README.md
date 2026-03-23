# BitoHelp

BiToHelp donation app (Quasar + WalletConnect), with real BCH Chipnet donation support.

## Install

```bash
npm install
```

## Run

```bash
npm run dev
```

## BCH Chipnet Donations (Paytaca)

Configure environment before running the app:

```bash
BCH_NETWORK=chipnet
BCH_CHIPNET_API_URL=https://chipnet.watchtower.cash/api/
# optional
BCH_EXPLORER_BASE_URL=https://chipnet.imaginary.cash/tx/
# optional, default 1.2 sats/byte
BCH_FEE_RATE_SATS_PER_BYTE=1.2
```

### Manual Test Checklist

- [ ] WalletConnect QR pairing works with Paytaca on Chipnet.
- [ ] Donating BCH creates a real signed + broadcasted txid.
- [ ] Txid is visible on Chipnet explorer/provider endpoint.
- [ ] UI status updates from pending to confirmed (>= 1 confirmation).
- [ ] Invalid non-chipnet addresses are rejected.
- [ ] Insufficient funds is handled with clear error.
- [ ] Wallet signature rejection is handled with clear error.
- [ ] Broadcast/API failure is handled with clear error.
- [ ] Confirmation timeout is handled and shown as pending timeout.
