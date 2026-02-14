<template>
  <q-page>

    <!-- HERO ini !!!-->
    <section class="hero-section">
      <div class="row items-center justify-between q-pa-xl full-width">

        <div class="col-12 col-md-6 hero-content">
          <h1 class="hero-title">
            Donate Bitcoin<br />
            <span class="highlight">Change Lives</span>
          </h1>
          

          <p class="hero-subtitle">
            Helping the world with fast, transparent blockchain-powered donations.
          </p>

          <q-btn
            label="Start Donating"
            color="primary"
            size="lg"
            unelevated
            class="hero-btn q-mt-lg"
            to="/donate"
            @click="$router.push('/donate')"
          />
        </div>

        <div class="col-12 col-md-5">
          <q-img src="Donaciones.gif" />
        </div>

      </div>
    </section>

    <!-- MISSION ini!!! -->
    <section class="q-pa-xl bg-grey-1">
      <div class="row q-col-gutter-lg items-center">
        <div class="col-12 col-md-6">
          <div class="section-title">Our Mission</div>
        </div>
        <div class="col-12 col-md-6">
          <p>
            We empower donors and nonprofits by providing a transparent,
            blockchain-based donation platform where every transaction is verifiable.
          </p>
        </div>
      </div>

      <q-carousel
        animated
        infinite
        navigation
        arrows
        class="q-mt-xl"
        v-model="slide"
        :autoplay="autoplay"
        @mouseenter="autoplay = false"
        @mouseleave="autoplay = true"
      >
        <q-carousel-slide :name="1" img-src="https://cdn.quasar.dev/img/mountains.jpg" />
        <q-carousel-slide :name="2" img-src="https://cdn.quasar.dev/img/parallax1.jpg" />
        <q-carousel-slide :name="3" img-src="https://cdn.quasar.dev/img/parallax2.jpg" />
      </q-carousel>
    </section>

    <!-- TESTIMONIALS ini!!!-->
    <section class="q-pa-xl">
      <div class="section-title q-mb-lg">Testimonials</div>

      <div class="row q-col-gutter-lg">
        <div class="col-12 col-md-4" v-for="t in testimonials" :key="t.name">
          <q-card class="testimonial-card">
            <q-img :src="t.image" />
            <q-card-section>
              <q-avatar :src="t.avatar" size="56px" />
              <div class="text-subtitle1 q-mt-sm">{{ t.name }}</div>
              <div class="text-caption">{{ t.role }}</div>
              <div class="q-mt-sm">{{ t.text }}</div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </section>

    <!-- ABOUT ini!!!-->
    <section class="q-pa-xl bg-grey-2">
      <div class="row q-col-gutter-lg">
        <div class="col-12 col-md-6">
          <q-card>
            <q-card-section>
              <div class="text-h6">About Us</div>
              <p>We provide blockchain-powered crypto donations for social impact.<br>Established in 2026, Inspired to Learn empowers individuals and transforms communities through education, made accessible and transparent through crypto donations.
              </p>
            </q-card-section>
            <q-card-actions>
              <q-btn label="Learn more" flat color="primary" />
            </q-card-actions>
          </q-card>
        </div>

        <div class="col-12 col-md-6">
          <q-card>
            <q-card-section>
              <div class="text-h6">Our Impact</div>
              <p>Education, disaster relief and healthcare funded with crypto.<br>Look back on our recent projects from tutoring programs and school supply distributions to community classes—made possible through crypto donations.</p>
            </q-card-section>
            <q-card-actions>
              <q-btn label="Explore" flat color="primary" />
            </q-card-actions>
          </q-card>
        </div>
      </div>
    </section>

  </q-page>
</template>

<script setup>
import { ref } from 'vue'

const slide = ref(1)
const autoplay = ref(true)


const testimonials = [
  {
    name: "Maria",
    role: "Typhoon Relief",
    text: "Crypto donations reached us instantly when we needed it.",
    image: "https://cdn.quasar.dev/img/parallax2.jpg",
    avatar: "../assets/image.png"
  },
  {
    name: "Jose",
    role: "Scholarship Student",
    text: "My education was funded through blockchain donations.",
    image: "https://cdn.quasar.dev/img/mountains.jpg",
    avatar: "/avatars/jose.jpg"
  },
  {
    name: "James",
    role: "Donor",
    text: "I trust crypto because every donation is transparent.",
    image: "https://cdn.quasar.dev/img/mountains.jpg",
    avatar: "/avatars/james.jpg"
  },

]
</script>
