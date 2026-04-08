<template>
  <q-page class="wallet-users-page q-pa-md">
    <h5 class="q-mt-none q-mb-md">Wallet <strong>Users</strong></h5>

    <q-input
      v-model="search"
      outlined
      dense
      placeholder="Search by address or name..."
      class="q-mb-md"
      style="max-width: 400px"
    >
      <template v-slot:prepend><q-icon name="search" /></template>
    </q-input>

    <q-card flat bordered>
      <q-table
        :rows="filteredUsers"
        :columns="columns"
        row-key="id"
        :loading="loading"
        flat
        dense
        :pagination="{ rowsPerPage: 20 }"
      >
        <template v-slot:body-cell-id="props">
          <q-td :props="props">
            <router-link
              :to="`/wallet-users/${props.row.id}`"
              class="text-primary text-weight-bold"
              style="text-decoration: none"
            >
              #{{ props.row.id }}
            </router-link>
          </q-td>
        </template>
        <template v-slot:body-cell-wallet_address="props">
          <q-td :props="props">
            <span class="text-mono" style="font-size: 12px">{{ props.row.wallet_address }}</span>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'

const loading = ref(true)
const users = ref([])
const search = ref('')

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  { name: 'wallet_address', label: 'Wallet Address', field: 'wallet_address', align: 'left' },
  { name: 'display_name', label: 'Display Name', field: 'display_name', align: 'left' },
  {
    name: 'created_at',
    label: 'Created',
    field: (row) => new Date(row.created_at).toLocaleDateString(),
    align: 'left',
    sortable: true,
  },
  {
    name: 'last_connected_at',
    label: 'Last Active',
    field: (row) =>
      row.last_connected_at ? new Date(row.last_connected_at).toLocaleDateString() : '—',
    align: 'left',
  },
]

const filteredUsers = computed(() => {
  const q = search.value.toLowerCase().trim()
  if (!q) return users.value
  return users.value.filter(
    (u) => u.wallet_address.includes(q) || (u.display_name || '').toLowerCase().includes(q),
  )
})

onMounted(async () => {
  try {
    const res = await api.get('users/')
    users.value = res.data
  } catch (err) {
    console.error('Failed to load wallet users:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped lang="scss">
.wallet-users-page {
  max-width: 1100px;
  margin: 0 auto;
}
.text-mono {
  font-family: 'Courier New', monospace;
}
</style>
