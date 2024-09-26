/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

var CACHE_NAME = 'odoo-website-pwa-cache-vWEB12.1';
var urlsToCache = [
    '/',
    '/odoo_ecommerce_pwa/static/src/img/offline_page.png',
    '/odoo_ecommerce_pwa/static/src/img/offline.png',
    '/odoo_ecommerce_pwa/static/src/img/online.png',
    '/pwa/offline',
];

// Service worker installation event, prefetch some data
// during installation of service worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

// override request fetch event so that we can manipulate it and respond data from cache
self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request) // Request from network
        .then(function(response) {
            return response;
        })
        .catch(function(err) {
            return caches.open(CACHE_NAME) // Search request from cache
            .then(function(cache) {
                return cache.match('/pwa/offline') || Promise.resolve()
            });
        })
    );
});