import { defineStore, acceptHMRUpdate } from 'pinia'

const STORAGE_KEY = 'cryptocare.network'

export const useNetworkStore = defineStore('network', {
  state: () => ({
    activeNetwork: localStorage.getItem(STORAGE_KEY) || 'chipnet',
  }),

  getters: {
    isMainnet: (state) => state.activeNetwork === 'mainnet',
    isChipnet: (state) => state.activeNetwork === 'chipnet',
    addressPrefix: (state) => (state.activeNetwork === 'mainnet' ? 'bitcoincash' : 'bchtest'),
    explorerBaseUrl: (state) =>
      state.activeNetwork === 'mainnet'
        ? 'https://bchexplorer.info'
        : 'https://chipnet.bchexplorer.info',
    apiBaseUrl: (state) =>
      state.activeNetwork === 'mainnet'
        ? 'https://watchtower.cash/api'
        : 'https://chipnet.watchtower.cash/api',
    electrumNetwork: (state) => (state.activeNetwork === 'mainnet' ? 'mainnet' : 'chipnet'),
    walletConnectChainId: (state) =>
      state.activeNetwork === 'mainnet' ? 'bch:bitcoincash' : 'bch:bchtest',
    networkLabel: (state) => (state.activeNetwork === 'mainnet' ? 'Mainnet' : 'Chipnet'),
  },

  actions: {
    switchNetwork(network) {
      if (network !== 'chipnet' && network !== 'mainnet') return
      if (network === this.activeNetwork) return
      this.activeNetwork = network
      localStorage.setItem(STORAGE_KEY, network)
      // Reset the ElectrumNetworkProvider singleton so vaultDonation picks up the new network
      window.__cryptocare_resetElectrumProvider?.()
    },
  },
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useNetworkStore, import.meta.hot))
}
