<template>
  <!-- Floating chat bubble -->
  <div class="krypto-chat-head" :class="{ 'is-open': isOpen }">
    <!-- Chat Window -->
    <transition name="krypto-window">
      <div v-if="isOpen" class="krypto-window" :class="{ 'krypto-light': !isDark }">
        <!-- Header -->
        <div class="krypto-header">
          <div class="krypto-header-left">
            <q-avatar size="36px" class="krypto-header-avatar">
              <img :src="KryptoAvatar" alt="Krypto" />
            </q-avatar>
            <div class="krypto-header-info">
              <div class="krypto-header-name">Krypto</div>
              <div class="krypto-header-sub">CrypToCare AI Assistant</div>
            </div>
          </div>
          <q-btn flat round dense icon="close" color="white" size="sm" @click="isOpen = false" />
        </div>

        <!-- Messages -->
        <div ref="messagesContainer" class="krypto-messages">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="krypto-msg"
            :class="msg.role === 'user' ? 'krypto-msg--user' : 'krypto-msg--bot'"
          >
            <q-avatar v-if="msg.role === 'assistant'" size="28px" class="krypto-msg-avatar">
              <img :src="KryptoAvatar" alt="Krypto" />
            </q-avatar>
            <div class="krypto-msg-body">
              <!-- eslint-disable-next-line vue/no-v-html -->
              <div class="krypto-bubble" v-html="formatMessage(msg.content)"></div>
              <div v-for="(chart, ci) in msg.charts || []" :key="ci" class="krypto-chart-wrap">
                <canvas :ref="(el) => mountChart(el, `${i}-${ci}`, chart)"></canvas>
              </div>
            </div>
          </div>

          <!-- Typing indicator -->
          <div v-if="isTyping" class="krypto-msg krypto-msg--bot">
            <q-avatar size="28px" class="krypto-msg-avatar">
              <img :src="KryptoAvatar" alt="Krypto" />
            </q-avatar>
            <div class="krypto-bubble krypto-typing">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="krypto-input-area">
          <textarea
            ref="inputEl"
            v-model="userInput"
            class="krypto-input"
            placeholder="Ask Krypto anything..."
            rows="1"
            @keydown="onKeyDown"
          ></textarea>
          <q-btn
            flat
            round
            dense
            icon="send"
            color="green"
            :disable="!userInput.trim() || isTyping"
            @click="sendMessage"
          />
        </div>
      </div>
    </transition>

    <!-- Draggable Bubble -->
    <button
      ref="bubbleEl"
      class="krypto-bubble-btn"
      :class="{ 'krypto-bubble-btn--open': isOpen }"
      :style="bubbleStyle"
      @pointerdown="onDragStart"
      @click.capture="onBubbleClick"
    >
      <img :src="KryptoAvatar" alt="Krypto" class="krypto-bubble-img" />
      <span class="krypto-online-dot"></span>
    </button>
  </div>
</template>

<script setup>
import { ref, reactive, computed, nextTick, watch, onMounted, onBeforeUnmount } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'src/boot/axios'
import KryptoAvatar from 'src/assets/Krypto.png'
import Chart from 'chart.js/auto'

const $q = useQuasar()
const isDark = computed(() => $q.dark.isActive)

const isOpen = ref(false)
const isTyping = ref(false)
const userInput = ref('')
const messages = ref([])
const messagesContainer = ref(null)
const inputEl = ref(null)
const bubbleEl = ref(null)

// ── Chart instances map (for cleanup) ──
const chartInstances = new Map()

// ── Drag state ──
const BUBBLE_SIZE = 60
const drag = reactive({ x: 0, y: 0, startX: 0, startY: 0, pointerId: null, moved: false })

const bubbleStyle = computed(() => {
  if (drag.x === 0 && drag.y === 0) return {}
  return {
    position: 'fixed',
    left: `${drag.x}px`,
    top: `${drag.y}px`,
    bottom: 'auto',
    right: 'auto',
  }
})

function clamp(val, min, max) {
  return Math.min(Math.max(val, min), max)
}

function initBubblePos() {
  drag.x = window.innerWidth - BUBBLE_SIZE - 24
  drag.y = window.innerHeight - BUBBLE_SIZE - 24
}

onMounted(() => {
  initBubblePos()
  window.addEventListener('resize', snapToEdge)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', snapToEdge)
  chartInstances.forEach((c) => c.destroy())
  chartInstances.clear()
})

// ── Chart rendering ──
const CHART_COLORS = [
  '#4caf50',
  '#2196f3',
  '#ff9800',
  '#e91e63',
  '#9c27b0',
  '#00bcd4',
  '#ff5722',
  '#607d8b',
]

function mountChart(el, key, chartData) {
  if (!el || chartInstances.has(key)) return
  nextTick(() => {
    const type = chartData.type || 'bar'
    const isPieish = type === 'pie' || type === 'doughnut'
    const datasets = (chartData.datasets || []).map((ds, i) => ({
      ...ds,
      backgroundColor:
        ds.backgroundColor ||
        (isPieish
          ? CHART_COLORS.slice(0, ds.data?.length || 0)
          : CHART_COLORS[i % CHART_COLORS.length]),
      borderColor:
        ds.borderColor || (type === 'line' ? CHART_COLORS[i % CHART_COLORS.length] : undefined),
    }))
    const dark = isDark.value
    const textColor = dark ? '#e0e8f0' : '#2c3e50'
    const gridColor = dark ? '#8eaccd' : '#999'
    const config = {
      type,
      data: { labels: chartData.labels || [], datasets },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          title: {
            display: !!chartData.title,
            text: chartData.title || '',
            color: textColor,
            font: { size: 13 },
          },
          legend: { labels: { color: textColor, font: { size: 11 } } },
        },
        ...(isPieish
          ? {}
          : { scales: { x: { ticks: { color: gridColor } }, y: { ticks: { color: gridColor } } } }),
      },
    }
    chartInstances.set(key, new Chart(el, config))
  })
}

function onDragStart(e) {
  drag.pointerId = e.pointerId
  drag.startX = e.clientX - drag.x
  drag.startY = e.clientY - drag.y
  drag.moved = false
  bubbleEl.value?.setPointerCapture(e.pointerId)
  window.addEventListener('pointermove', onDragMove)
  window.addEventListener('pointerup', onDragEnd)
}

function onDragMove(e) {
  if (e.pointerId !== drag.pointerId) return
  const nx = e.clientX - drag.startX
  const ny = e.clientY - drag.startY
  if (!drag.moved && Math.abs(nx - drag.x) + Math.abs(ny - drag.y) > 5) {
    drag.moved = true
  }
  drag.x = clamp(nx, 0, window.innerWidth - BUBBLE_SIZE)
  drag.y = clamp(ny, 0, window.innerHeight - BUBBLE_SIZE)
}

function onDragEnd(e) {
  if (e.pointerId !== drag.pointerId) return
  window.removeEventListener('pointermove', onDragMove)
  window.removeEventListener('pointerup', onDragEnd)
  bubbleEl.value?.releasePointerCapture(e.pointerId)
  drag.pointerId = null
  snapToEdge()
}

function snapToEdge() {
  const mid = window.innerWidth / 2
  drag.x = drag.x + BUBBLE_SIZE / 2 < mid ? 12 : window.innerWidth - BUBBLE_SIZE - 12
  drag.y = clamp(drag.y, 12, window.innerHeight - BUBBLE_SIZE - 12)
}

function onBubbleClick(e) {
  if (drag.moved) {
    e.stopImmediatePropagation()
    e.preventDefault()
    return
  }
  isOpen.value = !isOpen.value
}

// ── Chat logic ──
const WELCOME_MESSAGE =
  "Hey there! 👋 I'm Krypto, your CrypToCare AI assistant. Ask me anything about donating BCH, our nonprofits, or how the platform works!"

let welcomed = false
watch(isOpen, (val) => {
  if (val && !welcomed) {
    welcomed = true
    messages.value.push({ role: 'assistant', content: WELCOME_MESSAGE })
    nextTick(scrollToBottom)
  }
  if (val) {
    nextTick(() => inputEl.value?.focus())
  }
})

function scrollToBottom() {
  const el = messagesContainer.value
  if (el) el.scrollTop = el.scrollHeight
}

function formatMessage(text) {
  // Escape HTML
  let s = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

  // Convert markdown-style links [text](url) to <a>
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, label, href) => {
    const safeHref = href.replace(/"/g, '&quot;')
    return `<a href="${safeHref}" class="krypto-link">${label}</a>`
  })

  // Auto-link bare dApp hash routes: /#/something
  s = s.replace(/(^|[\s(])(\/[#][/][^\s)]*)/g, (_m, pre, route) => {
    const safeHref = route.replace(/"/g, '&quot;')
    return `${pre}<a href="${safeHref}" class="krypto-link">${route}</a>`
  })

  // Auto-link https:// URLs
  s = s.replace(/(https?:\/\/[^\s<)]+)/g, (url) => {
    const safeUrl = url.replace(/"/g, '&quot;')
    return `<a href="${safeUrl}" class="krypto-link" target="_blank" rel="noopener">${url}</a>`
  })

  // Bold: **text** or __text__
  s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  s = s.replace(/__(.+?)__/g, '<strong>$1</strong>')

  // Italic: *text* or _text_ (but not inside URLs/words with underscores)
  s = s.replace(/(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)/g, '<em>$1</em>')
  s = s.replace(/(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)/g, '<em>$1</em>')

  // Newlines to <br>
  s = s.replace(/\n/g, '<br>')
  return s
}

function onKeyDown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

async function sendMessage() {
  const text = userInput.value.trim()
  if (!text || isTyping.value) return

  messages.value.push({ role: 'user', content: text })
  userInput.value = ''
  isTyping.value = true
  await nextTick(scrollToBottom)

  const history = messages.value.slice(0, -1).map((m) => ({
    role: m.role,
    content: m.content,
  }))

  try {
    const { data } = await api.post('chat/', { message: text, history })
    const msg = { role: 'assistant', content: data.reply }
    if (data.charts?.length) msg.charts = data.charts
    messages.value.push(msg)
  } catch {
    messages.value.push({
      role: 'assistant',
      content: "Oops! I'm having trouble connecting right now. Please try again in a moment. 🔧",
    })
  } finally {
    isTyping.value = false
    await nextTick(scrollToBottom)
  }
}
</script>

<style scoped>
.krypto-chat-head {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  pointer-events: none;
}
.krypto-chat-head > * {
  pointer-events: auto;
}

/* ── Bubble button ── */
.krypto-bubble-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  padding: 0;
  cursor: grab;
  position: fixed;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
  transition: box-shadow 0.25s ease;
  background: #1a1a2e;
  overflow: visible;
  touch-action: none;
  z-index: 10000;
}
.krypto-bubble-btn:active {
  cursor: grabbing;
}
.krypto-bubble-btn:hover {
  box-shadow: 0 6px 24px rgba(76, 175, 80, 0.4);
}
.krypto-bubble-btn--open {
  transform: scale(0.9);
}
.krypto-bubble-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  pointer-events: none;
}
.krypto-online-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 14px;
  height: 14px;
  background: #4caf50;
  border-radius: 50%;
  border: 2.5px solid #1a1a2e;
  animation: krypto-pulse 2s infinite;
}
@keyframes krypto-pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.5);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(76, 175, 80, 0);
  }
}

/* ══════════════════ DARK (default) ══════════════════ */
.krypto-window {
  width: 360px;
  height: 500px;
  background: #16213e;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
  margin-bottom: 12px;
  position: fixed;
  bottom: 96px;
  right: 24px;
  z-index: 9999;
}

.krypto-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  background: #0f3460;
  flex-shrink: 0;
}
.krypto-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.krypto-header-avatar {
  border: 2px solid #4caf50;
}
.krypto-header-name {
  color: #fff;
  font-weight: 600;
  font-size: 15px;
  line-height: 1.2;
}
.krypto-header-sub {
  color: #8eaccd;
  font-size: 11px;
  line-height: 1.2;
}

.krypto-messages {
  flex: 1;
  overflow-y: auto;
  padding: 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.krypto-messages::-webkit-scrollbar {
  width: 5px;
}
.krypto-messages::-webkit-scrollbar-thumb {
  background: #0f3460;
  border-radius: 4px;
}

.krypto-msg {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  max-width: 88%;
}
.krypto-msg--user {
  align-self: flex-end;
  flex-direction: row-reverse;
}
.krypto-msg--bot {
  align-self: flex-start;
}
.krypto-msg-avatar {
  flex-shrink: 0;
}
.krypto-msg-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.krypto-chart-wrap {
  margin-top: 8px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  padding: 10px;
  max-width: 300px;
}
.krypto-light .krypto-chart-wrap {
  background: rgba(0, 0, 0, 0.04);
}

.krypto-bubble {
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 13.5px;
  line-height: 1.5;
  word-break: break-word;
}
.krypto-msg--user .krypto-bubble {
  background: #1b8c4e;
  color: #fff;
  border-bottom-right-radius: 4px;
}
.krypto-msg--bot .krypto-bubble {
  background: #1a2744;
  color: #d4e4f7;
  border-bottom-left-radius: 4px;
}

/* Links inside bubbles */
.krypto-bubble :deep(.krypto-link) {
  color: #66bb6a;
  text-decoration: underline;
  cursor: pointer;
}
.krypto-bubble :deep(.krypto-link:hover) {
  color: #81c784;
}

/* Typing indicator */
.krypto-typing {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 18px;
}
.krypto-typing .dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #8eaccd;
  animation: krypto-dot 1.2s infinite;
}
.krypto-typing .dot:nth-child(2) {
  animation-delay: 0.2s;
}
.krypto-typing .dot:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes krypto-dot {
  0%,
  60%,
  100% {
    opacity: 0.3;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-4px);
  }
}

/* Input */
.krypto-input-area {
  display: flex;
  align-items: flex-end;
  gap: 6px;
  padding: 10px 12px;
  background: #0f3460;
  flex-shrink: 0;
}
.krypto-input {
  flex: 1;
  background: #1a2744;
  border: 1px solid #233a5c;
  border-radius: 12px;
  color: #e0e8f0;
  padding: 10px 14px;
  font-size: 13.5px;
  line-height: 1.4;
  resize: none;
  outline: none;
  font-family: inherit;
  max-height: 80px;
  overflow-y: auto;
}
.krypto-input::placeholder {
  color: #5a7da8;
}
.krypto-input:focus {
  border-color: #4caf50;
}

/* ══════════════════ LIGHT MODE ══════════════════ */
.krypto-window.krypto-light {
  background: #f5f7fa;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}
.krypto-light .krypto-header {
  background: #ffffff;
  border-bottom: 1px solid #e0e4ea;
}
.krypto-light .krypto-header-name {
  color: #1a1a2e;
}
.krypto-light .krypto-header-sub {
  color: #6b7b8d;
}
.krypto-light .krypto-header .q-btn {
  color: #555 !important;
}

.krypto-light .krypto-messages::-webkit-scrollbar-thumb {
  background: #c8cdd4;
}

.krypto-light .krypto-msg--user .krypto-bubble {
  background: #1b8c4e;
  color: #fff;
}
.krypto-light .krypto-msg--bot .krypto-bubble {
  background: #ffffff;
  color: #2c3e50;
  border: 1px solid #e0e4ea;
}
.krypto-light .krypto-bubble :deep(.krypto-link) {
  color: #1b8c4e;
}
.krypto-light .krypto-bubble :deep(.krypto-link:hover) {
  color: #14693a;
}

.krypto-light .krypto-typing .dot {
  background: #9ca3ad;
}

.krypto-light .krypto-input-area {
  background: #ffffff;
  border-top: 1px solid #e0e4ea;
}
.krypto-light .krypto-input {
  background: #f0f2f5;
  border-color: #dde1e6;
  color: #2c3e50;
}
.krypto-light .krypto-input::placeholder {
  color: #8e99a6;
}
.krypto-light .krypto-input:focus {
  border-color: #4caf50;
}

/* ── Transitions ── */
.krypto-window-enter-active,
.krypto-window-leave-active {
  transition:
    transform 0.3s ease,
    opacity 0.3s ease;
  transform-origin: bottom right;
}
.krypto-window-enter-from,
.krypto-window-leave-to {
  transform: scale(0.75) translateY(20px);
  opacity: 0;
}

/* ── Mobile ── */
@media (max-width: 600px) {
  .krypto-window {
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    border-radius: 0;
    margin-bottom: 0;
    position: fixed;
  }
  .krypto-bubble-btn {
    width: 52px;
    height: 52px;
  }
  .krypto-chat-head.is-open .krypto-bubble-btn {
    display: none;
  }
}
</style>
